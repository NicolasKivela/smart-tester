import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BddCard from './BddCard.vue'

describe('BddCard tests', () => {
  it('renders BDD card with correct props', () => {
    const wrapper = mount(BddCard, {
      props: {
        modelValue: {
          id: 1,
          feature: 'Login',
          scenario: 'Login with valid credentials',
          given: ['User is on login page'],
          when: ['User enters valid username and password'],
          then: ['App logs user in'],
        },
      },
    })

    expect(wrapper.text()).toContain('Feature: Login')
  })
})
