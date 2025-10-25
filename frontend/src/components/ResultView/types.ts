export type BddScenario = {
  id: number
  feature: string
  scenario: string
  given: string[]
  when: string[]
  then: string[]
}

export type Feature = {
  id: number,
  feature: string,
  summary: string,
  requirements: string[],
  bdd_scenarios: BddScenario[]
}