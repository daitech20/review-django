<template>
    <a-layout style="min-height: 100vh">
        <SideBar/>
        <a-layout>
            <Header/>
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
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import { asset } from './helpers'
import SideBar from './components/SideBar.vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

export default {
    data() {
        return {
            logo: asset("logo.png")
        }
    },

    components: {
        SideBar, HelloWorld, Header, Footer
    }
}
</script>

<style scoped>
.content {
    margin: 0 16px;
}
</style>
