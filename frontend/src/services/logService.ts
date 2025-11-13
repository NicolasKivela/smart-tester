import axios from 'axios'

const API_URL = 'http://localhost:8010' // Adjust the URL as needed

// Get AI logs from backend
const getLogs = async () => {
  try {
    const response = await axios.get(API_URL + '/logs/ai-agent')

    return response.data
  } catch (error: Error) {
    throw error
  }
}

export { getLogs }
