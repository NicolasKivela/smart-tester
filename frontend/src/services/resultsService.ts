import axios from 'axios'

const API_URL = 'http://localhost:8010' // Adjust the URL as needed

const getBddScenarios = async () => {
  try {
    const response = await axios.get(API_URL + '/bdd_scenarios')
    return response.data
  } catch (e) {
    throw e
  }
}

const postBddScenarios = async (scenarios) => {
  try {
    const response = await axios.post(API_URL + '/bdd_scenarios', scenarios)

    return response.data
  } catch (e) {
    throw e
  }
}

const postBddIds = async (id: number) => {
  try {
    const response = await axios.post(`${API_URL}/test_scripts/generate`, null, {
      params: { bdd_item_id: id },
    })

    return response.data
  } catch (e) {
    throw e
  }
}

export { getBddScenarios, postBddScenarios, postBddIds }
