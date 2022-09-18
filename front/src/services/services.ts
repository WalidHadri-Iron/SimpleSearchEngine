import axios from "axios"

export const getToken = (url: string): void => {
    axios.get(url, { headers: { 'Access-Control-Allow-Origin' : '*'}}).then((res) => {
        const token = res.data.token;
        console.log(token);
        localStorage.setItem("TOKEN", token);
    }).catch((err) => console.log(err));
}

export const getSuggestions = async (url: string, input_sentence: string): Promise<any> => {
    const token = localStorage.getItem("TOKEN");

    if (!token) return;

    const response = await axios.post(url, { input_sentence }, { headers: { 'Authorization': `Bearer ${token}`} });

    const suggestions = response.data;

    return suggestions;
}

export const getDetails = async (url: string, index: number): Promise<any> => {
    const token = localStorage.getItem("TOKEN");

    if (!token) return;

    const response = await axios.get(url, { params: { index }, headers: { 'Authorization': `Bearer ${token}`} });

    return response.data;
}

export const setRelevance = async (url: string, data: number[]): Promise<void> => {
    const token = localStorage.getItem("TOKEN");

    if (!token) return;

    await axios.post(url, { relevant_suggestions: data }, { headers: { 'Authorization': `Bearer ${token}`} });
}


export const sendMail = async (url: string): Promise<void> => {
    const token = localStorage.getItem("TOKEN");

    if (!token) return;

    await axios.post(url, { headers: { 'Authorization': `Bearer ${token}`} });
}