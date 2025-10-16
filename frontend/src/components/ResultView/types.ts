export type BddScenario = {
  id: number
  feature: string
  scenario: string
  given: string[]
  when: string[]
  then: string[]
}
