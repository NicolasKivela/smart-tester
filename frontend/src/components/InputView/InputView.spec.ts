import { mount, flushPromises } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import InputView from '@/components/InputView/InputView.vue'
import * as service from '@/services/requirementService'

vi.mock('@/services/requirementService', () => ({
  postRequirements: vi.fn(),
  getTopics: vi.fn(),
  postSelectedTopic: vi.fn(),
}))

describe('InputView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  const mountComponent = () =>
    mount(InputView, {
      global: {
        stubs: {
          ErrorPopup: {
            template:
              '<div><button data-testid="error-close" @click="$emit(\'close\')">Close</button></div>',
          },
          ProcessDataPopup: {
            template: `<div v-if="visible" data-testid="processdata-popup">
              <button data-testid="popup-close" @click="$emit('close')">Close</button>
              <button data-testid="popup-continue-test" @click="$emit('continue', options[0]?.id ?? null)">
                Continue (test)
              </button>
            </div>`,
            props: ['visible', 'options'],
            emits: ['close', 'continue'],
          },
        },
      },
    })

  const setValidInputs = (wrapper: ReturnType<typeof mountComponent>) => {
    wrapper.vm.file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
    wrapper.vm.url = 'http://example.com'
  }

  it('clicking Process Data button calls processdata when enabled', async () => {
    const wrapper = mountComponent()

    setValidInputs(wrapper)

    await wrapper.vm.$nextTick() // Ensure button state updates
    vi.mocked(service.postRequirements).mockResolvedValue({})
    vi.mocked(service.getTopics).mockResolvedValue([])

    const processBtn = wrapper.get('[data-testid="process-data-btn"]')
    expect((processBtn.element as HTMLButtonElement).disabled).toBe(false)

    await processBtn.trigger('click')

    // Wait for async calls to resolve
    await flushPromises()

    expect(service.postRequirements).toHaveBeenCalledWith(expect.any(File), {
      url: 'http://example.com',
      username: '',
      password: '',
    })
    expect(service.getTopics).toHaveBeenCalled()
    expect(wrapper.vm.showPopup).toBe(true)

    expect(processBtn.text()).toContain('Select a different feature')
  })

  it('Process Data button is disabled/enabled correctly', async () => {
    const wrapper = mountComponent()
    wrapper.vm.file = null
    wrapper.vm.url = ''
    await wrapper.vm.$nextTick()

    const processBtn = wrapper.get('[data-testid="process-data-btn"]')
    expect((processBtn.element as HTMLButtonElement).disabled).toBe(true)

    // Check that button is enabled if inputs are valid
    setValidInputs(wrapper)
    await wrapper.vm.$nextTick()

    expect((processBtn.element as HTMLButtonElement).disabled).toBe(false)

    // Check that button is disabled if only one input is provided
    wrapper.vm.url = ''
    await wrapper.vm.$nextTick()

    expect((processBtn.element as HTMLButtonElement).disabled).toBe(true)
  })

  it('clicking Reset Inputs button clears fields', async () => {
    const wrapper = mountComponent()
    setValidInputs(wrapper)

    const resetBtn = wrapper.get('[data-testid="reset-inputs-btn"]')
    await resetBtn.trigger('click')

    expect(wrapper.vm.file).toBeNull()
    expect(wrapper.vm.url).toBe('')
  })

  it('invalid URL shows error popup and does not call backend', async () => {
    const wrapper = mountComponent()
    wrapper.vm.file = new File(['content'], 'test.pdf', { type: 'application/pdf' })
    wrapper.vm.url = 'not-a-valid-url'

    await wrapper.vm.$nextTick()
    await wrapper.get('[data-testid="process-data-btn"]').trigger('click')
    await flushPromises()

    expect(wrapper.vm.showError).toBe(true)
    expect(wrapper.vm.errorMessage).toBe('Please enter a valid URL!')
    expect(service.postRequirements).not.toHaveBeenCalled()
    expect(service.getTopics).not.toHaveBeenCalled()
    // URL is reset by component
    expect(wrapper.vm.url).toBe('')
  })

  it('handles ProcessDataPopup continue emit by calling postSelectedTopic and emitting events', async () => {
    const wrapper = mountComponent()
    setValidInputs(wrapper)

    service.postRequirements.mockResolvedValue({})
    service.getTopics.mockResolvedValue([
      { id: 1, name: 'Feature A' },
      { id: 2, name: 'Feature B' },
    ])
    service.postSelectedTopic.mockResolvedValue({})

    await wrapper.vm.$nextTick()
    await wrapper.get('[data-testid="process-data-btn"]').trigger('click')
    await flushPromises()

    // Emit continue from the stub with option id 1
    await wrapper.get('[data-testid="popup-continue-test"]').trigger('click')
    await flushPromises()

    expect(service.postSelectedTopic).toHaveBeenCalledWith(1)

    // Parent emits loader and scenario events
    const startLoaderMsg = wrapper.emitted()['start-loader']?.pop()?.[0]
    expect(startLoaderMsg).toContain('Generating BDD scenarios')

    expect(wrapper.emitted()['reset-code-block']).toBeTruthy()
    expect(wrapper.emitted()['chosen-feature-updated']?.[0]?.[0]).toBe(1)
    expect(wrapper.emitted()['bddScenariosUpdated']).toBeTruthy()
    expect(wrapper.emitted()['stop-loader']).toBeTruthy()

    // Popup should be closed
    expect(wrapper.vm.showPopup).toBe(false)
  })

  it('postRequirements failure shows error and stops loader', async () => {
    const wrapper = mountComponent()
    setValidInputs(wrapper)

    service.postRequirements.mockRejectedValue(new Error('fail'))

    await wrapper.vm.$nextTick()
    await wrapper.get('[data-testid="process-data-btn"]').trigger('click')
    await flushPromises()

    const startLoader = wrapper.emitted()['start-loader']?.[0]?.[0]
    expect(startLoader).toContain('Processing requirements')

    const stopLoader = wrapper.emitted()['stop-loader']?.[0]
    expect(stopLoader).toBeDefined()

    expect(wrapper.vm.showError).toBe(true)
    expect(wrapper.vm.errorMessage).toBe('Failed to POST requirements!')
    expect(wrapper.vm.showPopup).toBe(false)
  })

  it('getTopics failure shows error and stops loader', async () => {
    const wrapper = mountComponent()
    setValidInputs(wrapper)

    service.postRequirements.mockResolvedValue({})
    service.getTopics.mockRejectedValue(new Error('fail'))

    await wrapper.vm.$nextTick()
    await wrapper.get('[data-testid="process-data-btn"]').trigger('click')
    await flushPromises()

    const stopLoader = wrapper.emitted()['stop-loader']?.[0]
    expect(stopLoader).toBeDefined()

    expect(wrapper.vm.showError).toBe(true)
    expect(wrapper.vm.errorMessage).toBe('Failed to GET topics!')
    expect(wrapper.vm.showPopup).toBe(false)

    //Check that clicking close button hides error
    const closeBtn = wrapper.get('[data-testid="error-close"]')
    await closeBtn.trigger('click')

    expect(wrapper.vm.showError).toBe(false)
  })
})
