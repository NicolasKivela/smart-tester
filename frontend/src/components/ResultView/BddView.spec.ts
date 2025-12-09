import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import BddView from './BddView.vue'
import * as resultsService from '@/services/resultsService'

// Mock the resultsService used inside BddView
vi.mock('@/services/resultsService', () => ({
  createTests: vi.fn(),
  getTests: vi.fn(),
  startLocator: vi.fn(),
  getLocatorStatus: vi.fn(),
}))

describe('BddView', () => {
  const baseScenario = {
    id: 1,
    feature_id: 10,
    content:
      'Given I am on the login page\nWhen I enter valid credentials\nThen I should be logged in',
    scenario: 'Scenario 1',
  }

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('renders a BddCard for each provided scenario (stubs BddCard)', () => {
    const wrapper = mount(BddView, {
      props: {
        bddScenarios: [baseScenario, { ...baseScenario, id: 2 }],
        featureId: 10,
      },
      global: {
        // stub BddCard to avoid rendering child internals
        stubs: { BddCard: true },
      },
    })

    const cards = wrapper.findAll('[data-testid^="bdd-view-bdd-card-"]')
    expect(cards.length).toBe(2)
  })

  it('generate button is disabled initially (locators not fetched)', () => {
    const wrapper = mount(BddView, {
      props: {
        bddScenarios: [baseScenario],
        featureId: 10,
      },
      global: { stubs: { BddCard: true } },
    })

    const generateBtn = wrapper.find('[data-testid="bdd-view-generate-tests-btn"]')
    expect(generateBtn.attributes('disabled')).toBeDefined()
  })

  it('fetch locators flow: starts locator and polls until ready', async () => {
    vi.mocked(resultsService.startLocator).mockResolvedValue('success')
    vi.mocked(resultsService.getLocatorStatus).mockResolvedValue('ready')

    const wrapper = mount(BddView, {
      props: {
        bddScenarios: [baseScenario],
        featureId: 10,
      },
      global: { stubs: { BddCard: true } },
    })

    const fetchBtn = wrapper.find('[data-testid="bdd-view-fetch-locators-btn"]')
    await fetchBtn.trigger('click')
    await flushPromises()

    expect(resultsService.startLocator).toHaveBeenCalledWith(10)
    expect(resultsService.getLocatorStatus).toHaveBeenCalledWith(10)
  })

  it('generate tests flow: calls createTests, getTests and emits updateTests', async () => {
    const fakeTests = [{ id: 1, name: 't1' }]
    vi.mocked(resultsService.startLocator).mockResolvedValue('success')
    vi.mocked(resultsService.getLocatorStatus).mockResolvedValue('ready')
    vi.mocked(resultsService.createTests).mockResolvedValue('ok')
    vi.mocked(resultsService.getTests).mockResolvedValue(fakeTests)

    const wrapper = mount(BddView, {
      props: {
        bddScenarios: [baseScenario],
        featureId: 10,
      },
      global: { stubs: { BddCard: true } },
    })

    // First fetch locators so Generate Tests becomes enabled
    await wrapper.find('[data-testid="bdd-view-fetch-locators-btn"]').trigger('click')
    await flushPromises()

    // Now click Generate Tests button
    await wrapper.find('[data-testid="bdd-view-generate-tests-btn"]').trigger('click')
    await flushPromises()

    expect(resultsService.createTests).toHaveBeenCalledWith(10)
    expect(resultsService.getTests).toHaveBeenCalledWith(10)

    // updateTests emitted with the result of getTests
    const emitted = wrapper.emitted('updateTests')
    expect(emitted).toBeTruthy()
    expect(emitted![0]).toEqual([fakeTests])

    // loader events should have been emitted for the generation phase
    expect(wrapper.emitted('start-tests-loader')).toBeTruthy()
    expect(wrapper.emitted('stop-tests-loader')).toBeTruthy()
  })

  it('updates mutatedBddScenarios when prop changes', async () => {
    const wrapper = mount(BddView, {
      props: {
        bddScenarios: [baseScenario],
        featureId: 10,
      },
      global: { stubs: { BddCard: true } },
    })

    expect(wrapper.findAll('[data-testid^="bdd-view-bdd-card-"]').length).toBe(1)

    const newScenarios = [baseScenario, { ...baseScenario, id: 2 }]
    await wrapper.setProps({ bddScenarios: newScenarios })

    // mutatedBddScenarios is watched and should update the rendered list
    expect(wrapper.findAll('[data-testid^="bdd-view-bdd-card-"]').length).toBe(2)
  })
})
