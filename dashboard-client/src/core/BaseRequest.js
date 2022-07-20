import axios from "axios";
const apiUrl = 'http://localhost:8088/api/';

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