<template>
    <a-layout-header class="navbar-header">
        <a-row type="flex" justify="end" align="bottom">
            <a-col class="right-menu-header">
                <a-space :size="15">
                    <a-dropdown placement="bottomRight">
                        <a class="ant-dropdown-link" @click.prevent>
                            <a-icon name="AppstoreOutlined" />
                        </a>

                        <template #overlay>
                            <a-menu>
                                <a-menu-item>1st menu item</a-menu-item>
                                <a-menu-item>2st menu item</a-menu-item>
                                <a-menu-item>3st menu item</a-menu-item>
                            </a-menu>
                        </template>
                    </a-dropdown>

                    <a-dropdown placement="bottomRight">
                        <a class="ant-dropdown-link" @click.prevent>
                            <a-icon name="BellOutlined" />
                        </a>

                        <template #overlay>
                            BellOutlined
                        </template>
                    </a-dropdown>

                    <a-dropdown placement="bottomRight">
                        <a class="ant-dropdown-link" @click.prevent>
                            <a-icon name="MailOutlined" />
                        </a>

                        <template #overlay>
                            MailOutlined
                        </template>
                    </a-dropdown>

                    <a-dropdown placement="bottomRight">
                        <a class="ant-dropdown-link" @click.prevent>
                            <a-avatar style="color: #f56a00; background-color: #fde3cf">U</a-avatar>
                        </a>

                        <template #overlay>
                            <a-menu>
                                <a-menu-item>Hi, {{ user.username }}</a-menu-item>
                                <a-menu-item>
                                    <router-link :to="{ name: 'account.detail', params: { username: user.username }}" >
                                        Profile
                                    </router-link>
                                </a-menu-item>
                                <a-menu-item @click="handleLogout">Logout</a-menu-item>
                            </a-menu>
                        </template>
                    </a-dropdown>
                </a-space>
            </a-col>
        </a-row>
    </a-layout-header>
</template>

<script>
import { authStore } from '../store/auth.store'
import { mapActions, mapState } from 'pinia'

export default {

    computed: {
        ...mapState(authStore, ['user'])
    },

    methods: {
        ...mapActions(authStore, ['clearAccessToken', 'clearUser', 'clearRefreshToken']),
        handleLogout: function() {
            this.clearAccessToken()
            this.clearRefreshToken()
            this.clearUser()
            this.$router.push({path: 'login'})
        }
    }
}
</script>

<style scoped>
.navbar-header {
    background-color: #fff;
    padding: 0 16px;
}
</style>