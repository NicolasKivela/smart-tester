import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import BddCard from './BddCard.vue'
import * as resultsService from '@/services/resultsService'
import type { BddScenario } from './types'

vi.mock('@/services/resultsService', () => ({
  updateBddScenario: vi.fn(),
  deleteBddScenario: vi.fn(),
}))

describe('BddCard', () => {
  const mockBddScenario: BddScenario = {
    id: 1,
    feature_id: 10,
    content:
      'Given I am on the login page\nWhen I enter valid credentials\nThen I should be logged in',
    scenario: 'Login with valid credentials',
  }

  afterEach(() => {
    vi.resetAllMocks()
  })

  describe('Rendering', () => {
    it('renders BDD card with correct content', () => {
      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      expect(wrapper.text()).toContain(mockBddScenario.content)
    })

    it('renders edit button when not in edit mode', () => {
      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      const editButton = wrapper.find('[data-testid="bdd-card-edit-btn"]')
      expect(editButton.exists()).toBe(true)
    })

    it('renders delete button', () => {
      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      const deleteButton = wrapper.find('[data-testid="bdd-card-delete-btn"]')
      expect(deleteButton.exists()).toBe(true)
    })
  })

  describe('Edit Scenario', () => {
    it('toggles to edit mode when edit button is clicked', async () => {
      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      const editButton = wrapper.find('[data-testid="bdd-card-edit-btn"]')
      await editButton.trigger('click')

      const textarea = wrapper.find('[data-testid="bdd-card-edit-textarea"]')
      expect(textarea.exists()).toBe(true)
    })

    it('displays textarea with correct initial value in edit mode', async () => {
      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-edit-btn"]').trigger('click')

      const textarea = wrapper.find('[data-testid="bdd-card-edit-textarea"]')
      expect(textarea.element.value).toBe(mockBddScenario.content)
    })

    it('hides edit button when in edit mode', async () => {
      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-edit-btn"]').trigger('click')

      const editButton = wrapper.find('[data-testid="bdd-card-edit-btn"]')
      expect(editButton.exists()).toBe(false)
    })

    it('emits updateScenario event on successful save', async () => {
      vi.mocked(resultsService.updateBddScenario).mockResolvedValue('success')

      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-edit-btn"]').trigger('click')

      const updatedContent = 'Updated BDD content'
      const textarea = wrapper.find('[data-testid="bdd-card-edit-textarea"]')
      await textarea.setValue(updatedContent)

      await wrapper.find('[data-testid="bdd-card-save-btn"]').trigger('click')
      await flushPromises()

      expect(wrapper.emitted('updateScenario')).toBeTruthy()
    })

    it('exits edit mode after successful save', async () => {
      vi.mocked(resultsService.updateBddScenario).mockResolvedValue('success')

      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-edit-btn"]').trigger('click')
      await wrapper.find('[data-testid="bdd-card-save-btn"]').trigger('click')
      await flushPromises()

      const editButton = wrapper.find('[data-testid="bdd-card-edit-btn"]')
      expect(editButton.exists()).toBe(true)
    })

    it('logs error when save fails', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      vi.mocked(resultsService.updateBddScenario).mockResolvedValue('error')

      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-edit-btn"]').trigger('click')
      await wrapper.find('[data-testid="bdd-card-save-btn"]').trigger('click')
      await flushPromises()

      expect(consoleErrorSpy).toHaveBeenCalledWith(
        expect.stringContaining('Failed to update BDD scenario'),
        'error',
      )

      consoleErrorSpy.mockRestore()
    })

    it('textarea blur event triggers save', async () => {
      vi.mocked(resultsService.updateBddScenario).mockResolvedValue('success')

      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-edit-btn"]').trigger('click')
      await wrapper.find('[data-testid="bdd-card-edit-textarea"]').trigger('blur')
      await flushPromises()

      expect(resultsService.updateBddScenario).toHaveBeenCalled()
    })
  })

  describe('Delete Functionality', () => {
    it('emits delete event on successful deletion', async () => {
      vi.mocked(resultsService.deleteBddScenario).mockResolvedValue('success')

      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-delete-btn"]').trigger('click')
      await flushPromises()

      expect(wrapper.emitted('delete')).toBeTruthy()
      expect(wrapper.emitted('delete')[0]).toEqual([mockBddScenario])
    })

    it('logs error when delete fails', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      vi.mocked(resultsService.deleteBddScenario).mockResolvedValue('error')

      const wrapper = mount(BddCard, {
        props: {
          modelValue: mockBddScenario,
        },
      })

      await wrapper.find('[data-testid="bdd-card-delete-btn"]').trigger('click')
      await flushPromises()

      expect(consoleErrorSpy).toHaveBeenCalledWith(
        expect.stringContaining('Failed to delete BDD scenario'),
        'error',
      )

      consoleErrorSpy.mockRestore()
    })
  })

  describe('Props Watching', () => {
    it('updates internal state when modelValue prop changes', async () => {
      const initialScenario: BddScenario = {
        id: 1,
        feature_id: 10,
        content: 'Initial content',
        scenario: 'Initial scenario',
      }

      const updatedScenario: BddScenario = {
        id: 1,
        feature_id: 10,
        content: 'Updated content',
        scenario: 'Updated scenario',
      }

      const wrapper = mount(BddCard, {
        props: {
          modelValue: initialScenario,
        },
      })

      expect(wrapper.text()).toContain('Initial content')

      await wrapper.setProps({
        modelValue: updatedScenario,
      })

      expect(wrapper.text()).toContain('Updated content')
    })
  })
})
