import http from './http.service'

export default {
    login(username, password) {
        return http.post('/api/token', {
            username: username,
            password: password
        });
    },

    logout() {
        return http.post('/api/logout');
    }
}
