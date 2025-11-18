import axios from 'axios'

const API_URL = 'http://localhost:8010' // Adjust the URL as needed

const getBddScenarios = async (feature_id) => {
  try {
    const response = await axios.get(API_URL + '/bdd_scenarios?feature_id=' + feature_id)

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

const startLocator = async (id: number) => {
  try {
    const response = await axios.post(`${API_URL}/scraper/start?feature_id=` + id)

    if (response.status === 200) {
      return 'success'
    } else {
      return response.data.message
    }
  } catch (e) {
    throw e
  }
}

const getLocatorStatus = async (id: number) => {
  try {
    const response = await axios.get(`${API_URL}/scraper/fetch_all_locator_data?feature_id=` + id)

    return response.data.body[0] ? response.data.body[0].locator_element.status : 'ongoing'
  } catch (e) {
    throw e
  }
}

const createTests = async (id: number) => {
  try {
    const response = await axios.post(`${API_URL}/test_scripts/generate?feature_id=` + id)

    return response.data
  } catch (e) {
    throw e
  }
}

const getTests = async (feature_id: number) => {
  try {
    const response = await axios.get(`${API_URL}/test_scripts?feature_id=` + feature_id)

    return response.data.body
  } catch (e) {
    throw e
  }
}

export { getBddScenarios, postBddScenarios, createTests, getTests, startLocator, getLocatorStatus }
