import axios from 'axios'

const API_URL = 'http://localhost:8010' // Adjust the URL as needed

const getBddScenarios = async () => {
  const response = await axios.get(API_URL + '/bdd_scenarios')
  console.log(response)
}

export { getBddScenarios }
