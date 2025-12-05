import axios from 'axios'

const API_URL = 'http://localhost:8010' // Adjust the URL as needed

// Post inputs to backend
const postRequirements = async (file: File, jsonItem: object) => {
  // Construck the formdata to send to backend
  const formData = new FormData()
  formData.append('file', file)
  formData.append('url', jsonItem['url'])
  formData.append('username', jsonItem['username'])
  formData.append('password', jsonItem['password'])

  // Post requirements to backend
  try {
    const response = await axios.post(API_URL + '/requirements', formData)

    return response.data
  } catch (error: any) {
    throw error
  }
}

// Get topics from backend
const getTopics = async () => {
  try {
    const response = await axios.get(API_URL + '/requirements')

    return response.data
  } catch (error: any) {
    throw error
  }
}

// Post the selected topic to backend
const postSelectedTopic = async (id: number) => {
  try {
    const response = await axios.post(`${API_URL}/bdd_scenarios/generate/${id}`, null, {
      params: { item_id: id },
    })

    return response.data
  } catch (error: any) {
    throw error
  }
}

const resetDatabase = async () => {
  try {
    console.log("RESETTING DATABASE")
    const response = await axios.post(`${API_URL}/database/reset`)
    console.log(response)
    if (response.status === 200) {
      return 'success'
    } else {
      return response.data.message
    }
  } catch (e) {
    throw e
  }

}

export { postRequirements, getTopics, postSelectedTopic,resetDatabase }
