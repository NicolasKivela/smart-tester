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

const updateBddScenario = async (scenario) => {
  try {
    const updatedScenario = {
      content: scenario.content,
      scenario: scenario.scenario,
    }

    const params = {
      feature_id: scenario.feature_id,
      bdd_id: scenario.id,
    }

    const response = await axios.put(`${API_URL}/bdd_scenarios`, updatedScenario, {
      params: params,
    })

    if (response.status === 200) {
      return 'success'
    } else {
      return response
    }
  } catch (e) {
    throw e
  }
}

const deleteBddScenario = async (feature_id: number, bdd_id: number) => {
  try {
    const params = {
      feature_id: feature_id,
      bdd_id: bdd_id,
    }
    const response = await axios.delete(`${API_URL}/bdd_scenarios`, { params: params })

    if (response.status === 200) {
      return 'success'
    } else {
      return response
    }
  } catch (e) {
    throw e
  }
}

const addBddScenario = async (scenario) => {
  try {
    const data = {
      content: scenario.content,
      scenario: scenario.scenario,
    }
    const response = await axios.post(
      `${API_URL}/bdd_scenarios?feature_id=${scenario.feature_id}`,
      data,
    )

    if (response.status === 200) {
      return 'success'
    } else {
      return response
    }
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

export { getBddScenarios, createTests, updateBddScenario, deleteBddScenario, addBddScenario }
