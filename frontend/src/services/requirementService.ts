import axios from 'axios'

const API_URL = 'http://localhost:8010' // Adjust the URL as needed

// Post inputs to backend
const postRequirements = async (file: File, jsonItem: object) => {

    // Construck the formdata to send to backend
    const formData = new FormData();
    formData.append("file", file);
    formData.append("json_item", JSON.stringify(jsonItem));
    
    // Post requirements to backend
    try {
        const response = await axios.post(API_URL + '/requirements', formData);

        console.log(response.data);
        return response.data;
    } catch (error: any) {
        throw error;
    }
}

// Get topics from backend
const getTopics = async () =>{

    try {
        const response = await axios.get(API_URL + '/requirements');
        console.log(response.data);

        return response.data;
    }
    catch (error: any) {
        throw error;
    }
}

// Post the selected topic to backend
const postSelectedTopic = async (selected: string) => {

    try {
        const response = await axios.post(API_URL + '/bdd_scenarios/generate', selected);

        return response.data;
    } catch (error: any) {
        throw error;
    }

}

export { postRequirements , getTopics, postSelectedTopic}
