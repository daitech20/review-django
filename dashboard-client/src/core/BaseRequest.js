import axios from "axios";
const apiUrl = import.meta.env.VITE_API_BASE_URL.trimEnd('/')+'/api/';

export default {
    getHeaders() {
        let token = window.localStorage.getItem('token');
        if (token == null) {
            return {}
        }
        return { Authorization: 'Bearer ' + token }
    },

    get(url) {
        return axios.get(
            apiUrl + url,
            { headers: this.getHeaders() }
        );
    },

    post(url, data) {
        return axios.post(
            apiUrl + url,
            data,
            { headers: this.getHeaders() }
        );
    },

    put(url, data) {
        return axios.put(
            apiUrl + url,
            data,
            { headers: this.getHeaders() }
        );
    },

    delete(url) {
        return axios.delete(
            apiUrl + url,
            { headers: this.getHeaders() }
        );
    }
}