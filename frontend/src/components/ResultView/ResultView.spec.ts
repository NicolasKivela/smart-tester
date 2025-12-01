import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ResultView from '@/components/ResultView/ResultView.vue'

describe('ResultView', () => {
  const bddScenariosMock = [
    { id: 1, name: 'Scenario 1' },
    { id: 2, name: 'Scenario 2' },
  ]
  const featureIdMock = 123
  const resetValueMock = 0

  it('renders BddView and CodeView with correct props', () => {
    const wrapper = mount(ResultView, {
      props: {
        bddScenarios: bddScenariosMock,
        featureId: featureIdMock,
        resetValue: resetValueMock,
      },
    })

    const bddView = wrapper.findComponent({ name: 'BddView' })
    const codeView = wrapper.findComponent({ name: 'CodeView' })

    expect(bddView.exists()).toBe(true)
    expect(codeView.exists()).toBe(true)

    expect(bddView.props('bddScenarios')).toEqual(bddScenariosMock)
    expect(bddView.props('featureId')).toBe(featureIdMock)
    expect(codeView.props('resetValue')).toBe(resetValueMock)
  })

  it('updates testScripts when handleTests is called via updateTests event', async () => {
    const wrapper = mount(ResultView, {
      props: {
        bddScenarios: bddScenariosMock,
        featureId: featureIdMock,
        resetValue: resetValueMock,
      },
    })

    const bddView = wrapper.findComponent({ name: 'BddView' })
    const testScriptMock = [{ script_code: 'console.log("test")' }]

    await bddView.vm.$emit('updateTests', testScriptMock)
    await wrapper.vm.$nextTick()

    const codeView = wrapper.findComponent({ name: 'CodeView' })
    expect(codeView.props('scripts')).toBe('console.log("test")')
  })

  it('emits start-loader and stop-loader when loaderStart and loaderStop are triggered', async () => {
    const wrapper = mount(ResultView, {
      props: {
        bddScenarios: bddScenariosMock,
        featureId: featureIdMock,
        resetValue: resetValueMock,
      },
    })

    const bddView = wrapper.findComponent({ name: 'BddView' })

    await bddView.vm.$emit('start-tests-loader', 'Loading tests...')
    await bddView.vm.$emit('stop-tests-loader')

    const emitted = wrapper.emitted()
    expect(emitted['start-loader']).toBeTruthy()
    expect(emitted['start-loader'][0]).toEqual(['Loading tests...'])
    expect(emitted['stop-loader']).toBeTruthy()
  })
})
