import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mount, VueWrapper } from '@vue/test-utils'
import { nextTick } from 'vue'
import CodeView from './CodeView.vue'

let wrapper: VueWrapper<typeof CodeView>

const mountWith = (props: Partial<{ scripts: string; resetValue: number }> = {}) =>
  mount(CodeView, { props: { scripts: '', resetValue: 0, ...props } })

describe('CodeView', () => {
  it('parses JSON with test_script property', async () => {
    wrapper = mountWith({
      scripts: JSON.stringify({ test_script: 'parsed test script content' }),
    })
    await nextTick()
    const codeElement = wrapper.find('[data-testid="code-view-code-text"]')
    expect(codeElement.text()).toContain('parsed test script content')
  })

  it('updates code when scripts prop changes', async () => {
    wrapper = mountWith({ scripts: 'initial code' })
    await nextTick()
    expect(wrapper.find('[data-testid="code-view-code-text"]').text()).toContain('initial code')

    await wrapper.setProps({ scripts: 'updated code' })
    await nextTick()
    expect(wrapper.find('[data-testid="code-view-code-text"]').text()).toContain('updated code')
  })

  it('clears code block when resetValue prop changes', async () => {
    wrapper = mountWith({ scripts: 'test code' })
    await nextTick()
    expect(wrapper.find('[data-testid="code-view-code-text"]').text()).toBeTruthy()

    await wrapper.setProps({ resetValue: 1 })
    await nextTick()
    expect(wrapper.find('[data-testid="code-view-code-text"]').text()).toBe('')
  })

  it('calls copy to clipboard with correct content', async () => {
    Object.assign(navigator, {
      clipboard: {
        writeText: vi.fn().mockResolvedValue(undefined),
      },
    })

    wrapper = mountWith({ scripts: 'test script\\nwith newlines' })
    await nextTick()
    await wrapper.find('[data-testid="code-view-copy-btn"]').trigger('click')
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('test script\nwith newlines')
  })
})

describe('session reset', () => {
  let reloadSpy: ReturnType<typeof vi.fn>

  beforeEach(() => {
    reloadSpy = vi.fn()
    vi.stubGlobal('location', { reload: reloadSpy })
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('resets the session when reset button is clicked', async () => {
    wrapper = mountWith({ scripts: 'test code' })
    await wrapper.find('[data-testid="code-view-reset-session-btn"]').trigger('click')
    expect(reloadSpy).toHaveBeenCalled()
  })
})
