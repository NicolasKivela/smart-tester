import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BddCard from './BddCard.vue'

describe('BddCard tests', () => {
  it('renders BDD card with correct props', () => {
    const wrapper = mount(BddCard, {
      props: {
        modelValue: {
          id: 1,
          content: 'Login with valid credentials',
        },
      },
    })

    expect(wrapper.text()).toContain('Login with valid credentials')
  })
})
