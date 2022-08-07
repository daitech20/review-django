import axios from "axios";
import authService from '../services/review_app/auth.service';
import { authStore } from '../store/auth.store';
import { mapActions, mapState } from 'pinia';
const apiUrl = import.meta.env.VITE_API_BASE_URL.trimEnd('/')+'/api/';

export default {
    ...mapActions(authStore, ['setAccessToken', 'clearAccessToken', 'clearRefreshToken', 'clearUser']),
    ...mapState(authStore, ['user', 'accessToken', 'refreshToken']),

    getHeaders() {
        if (this.user() === null) {
            return {}
        }

        return authService.checkExpriedToken(this.user().username)
        .then(response => {
            return { Authorization: 'Bearer ' + this.accessToken() }
        })
        .catch(error => {
            return authService.refreshToken(this.refreshToken())
            .then(response => {
                this.setAccessToken(response.data.access)
                return { Authorization: 'Bearer ' + response.data.access }
            })
            .catch(error => {
                this.clearAccessToken()
                this.clearRefreshToken()
                this.clearUser()
                return {}
            })
            
        })

    },

    async get(url) {
        const header = await this.getHeaders()
        return axios.get(
            apiUrl + url,
            { headers: header}
        );
    },

    async post(url, data) {
        const header = await this.getHeaders()
        return axios.post(
            apiUrl + url,
            data,
            { headers: header }
        );
    },

    async put(url, data) {
        const header = await this.getHeaders()
        return axios.put(
            apiUrl + url,
            data,
            { headers: header }
        );
    },

    async delete(url) {
        const header = await this.getHeaders()
        return axios.delete(
            apiUrl + url,
            { headers: header }
        );
    }
}