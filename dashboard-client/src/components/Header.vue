<template>
    <a-layout-header class="navbar-header">
        <a-row type="flex" justify="end" align="bottom">
            <a-col class="right-menu-header">
                <a-space :size="15">
                    <a-dropdown placement="bottomRight">
                        <a class="ant-dropdown-link" @click.prevent>
                            <a-icon name="AppstoreOutlined" :style="rightMenuIconStyle"/>
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
                            <a-icon name="BellOutlined" :style="rightMenuIconStyle"/>
                        </a>

                        <template #overlay>
                            BellOutlined
                        </template>
                    </a-dropdown>

                    <a-dropdown placement="bottomRight">
                        <a class="ant-dropdown-link" @click.prevent>
                            <a-icon name="MailOutlined" :style="rightMenuIconStyle"/>
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
                                <a-menu-item>Profile</a-menu-item>
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
export default {
    setup() {
        
    },

    props: ['user'],

    methods: {
        handleLogout: function() {
            window.localStorage.clear()
            this.$router.push({name: 'login'})
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