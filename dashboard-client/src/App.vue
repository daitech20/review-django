<template>
    <a-layout v-if="isLoginIn" style="min-height: 100vh">
        <SideBar :user="user" />
        <a-layout>
            <Header :user="user" />
            <a-layout-content class="content">
                <router-view v-slot="{ Component }">
                    <!-- <transition> -->
                        <component :is="Component" />
                    <!-- </transition> -->
                </router-view>
            </a-layout-content>
            <Footer/>
        </a-layout>
    </a-layout>

    <div v-if="!isLoginIn">
        <router-view v-slot="{ Component }">
            <!-- <transition> -->
                <component :is="Component" />
            <!-- </transition> -->
        </router-view>
    </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import { asset } from './helpers'
import SideBar from './components/SideBar.vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import BaseRequest from './core/BaseRequest.js'

export default {
    data() {
        return {
            logo: asset("logo.png"),
            isLoginIn: false,
            user: {

            }
        }
    },

    components: {
        SideBar, HelloWorld, Header, Footer
    },

    mounted() {
        this.checkLoggedIn()
    },

    watch: {
        '$route': 'checkLoggedIn'
    },

    methods: {
        checkLoggedIn: function() {
            if (window.localStorage.getItem('isLoginIn') == 'true') {
                this.isLoginIn = true
            }
            else {
                this.isLoginIn = false
            }
            if (this.isLoginIn == null || this.isLoginIn == false) {
                this.$router.push({name: 'login'})
            }

            let user = window.localStorage.getItem('user');
            BaseRequest.get('user/' + user)
            .then(response => {
                this.user = response.data
            })
            .catch(error=> {
                console.log(error.response.data);
                this.isLoginIn = false
                this.$router.push({name: 'login'})
            });
        }
    },

}
</script>

<style scoped>
.content {
    margin: 0 16px;
}
</style>
