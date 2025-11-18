export type BddScenario = {
  id?: number
  feature_id: number
  content: string
  scenario: string
  locator_element_id?: number
  test_script_id?: number
}

// export type Feature = {
//   id: number
//   feature: string
//   summary: string
//   requirements: string[]
//   bdd_scenarios: BddScenario[]
// }
