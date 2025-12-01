import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ProcessDataPopup from '@/components/InputView/ProcessDataPopup.vue'

const options = [
  { id: 1, name: 'Feature A' },
  { id: 2, name: 'Feature B' },
  { id: 3, name: 'Feature C' },
]

describe('ProcessDataPopup', () => {
  let wrapper: ReturnType<typeof mount>

  const mountPopup = (visible = true, opts = options) =>
    mount(ProcessDataPopup, {
      props: {
        visible,
        options: opts,
      },
    })

  it('renders nothing when visible=false', () => {
    wrapper = mountPopup(false)

    expect(wrapper.find('[data-testid="process-popup-overlay"]').exists()).toBe(false)
    expect(wrapper.find('[data-testid="processdata-popup"]').exists()).toBe(false)
  })

  it('renders overlay, title, instruction when visible=true', () => {
    wrapper = mountPopup(true)
    expect(wrapper.get('[data-testid="process-popup-overlay"]').exists()).toBe(true)
    expect(wrapper.get('[data-testid="processdata-popup"]').exists()).toBe(true)

    expect(wrapper.get('[data-testid="processdata-popup-title"]').text()).toBe(
      'Requirements have been processed',
    )
    expect(wrapper.get('[data-testid="processdata-popup-instruction-text"]').text()).toContain(
      'Choose the feature you want to continue',
    )
  })

  it('Continue is disabled initially and becomes enabled after selecting a radio', async () => {
    wrapper = mountPopup(true)
    const continueBtn = wrapper.get('[data-testid="processdata-popup-continue-btn"]')

    expect((continueBtn.element as HTMLButtonElement).disabled).toBe(true)

    // Select id=2
    const radio2 = wrapper.get('[data-testid="radio-input-2"]')
    await radio2.setValue()

    // Now Continue should be enabled
    expect((continueBtn.element as HTMLButtonElement).disabled).toBe(false)
  })

  it('emits close on X button and on Cancel button', async () => {
    wrapper = mountPopup(true)

    // Close (X) button
    const closeX = wrapper.get('[data-testid="processdata-popup-close-btn"]')
    await closeX.trigger('click')
    const closeEvents1 = wrapper.emitted('close')
    expect(closeEvents1).toBeTruthy()
    expect(closeEvents1![0]).toEqual([])

    // Cancel button
    const cancelBtn = wrapper.get('[data-testid="processdata-popup-cancel-btn"]')
    await cancelBtn.trigger('click')
    const closeEvents2 = wrapper.emitted('close')
    expect(closeEvents2).toBeTruthy()
    expect(closeEvents2!.length).toBeGreaterThan(1) // second emission
    expect(closeEvents2![1]).toEqual([])
  })

  it('emits continue with the selected option id', async () => {
    wrapper = mountPopup(true)

    // Select id=3
    await wrapper.get('[data-testid="radio-input-3"]').setValue()

    // Click Continue
    const continueBtn = wrapper.get('[data-testid="processdata-popup-continue-btn"]')
    await continueBtn.trigger('click')

    const continueEvents = wrapper.emitted('continue')
    expect(continueEvents).toBeTruthy()
    expect(continueEvents!.length).toBe(1)

    expect(continueEvents![0][0]).toBe(3)
  })
})
