<template>
    <a-layout-sider v-model:collapsed="collapsed" collapsible @collapse="setSidebarCollapsed">
        <div class="logo">
            <img :src="logoImage" class="logo-image"/>
        </div>
        <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
            <a-menu-item key="dashboard">
                <a-icon name="PieChartOutlined"></a-icon>
                <router-link class="menu-link" :to="{name: 'dashboard'}">Dashboard</router-link>
            </a-menu-item>
            <a-menu-item key="review.list">
                <a-icon name="MessageOutlined"></a-icon>
                <router-link class="menu-link" :to="{name: 'review.list'}">Review</router-link>
            </a-menu-item>
            <a-sub-menu key="setting">
                <template #title>
                    <span>
                        <a-icon name="SettingOutlined"></a-icon>
                        <span>Settings</span>
                    </span>
                </template>
                <a-menu-item key="setting.appearance">
                    <router-link class="menu-link" :to="{name: 'setting.appearance'}">Appearance</router-link>
                </a-menu-item>
                <a-menu-item key="setting.google_api">
                    <router-link class="menu-link" :to="{name: 'setting.google_api'}">Google APIs</router-link>
                </a-menu-item>
            </a-sub-menu>
            <a-menu-item key="support_center">
                <a-icon name="WhatsAppOutlined"></a-icon>
                <router-link class="menu-link" :to="{name: 'support_center'}">Support Center</router-link>
            </a-menu-item>
        </a-menu>
    </a-layout-sider>
</template>

<script>
import { mapActions } from 'pinia'
import { appearance } from '../store/appearance'
import { asset } from '../helpers'

export default {
    data() {
        return {
            selectedKeys: [],
            collapsed: false,
            logoImage: asset('logo.png')
        }
    },

    mounted() {
        this.collapsed = this.isSidebarCollapased()
    },

    methods: {
        ...mapActions(appearance, ['isSidebarCollapased', 'setSidebarCollapsed'])
    }

}
</script>

<style scoped>

.logo {
    width: 100%;
    padding: 16px 16px;
}
.logo-image {
   width: 100%;
   background-color: #fff;
}

.ant-menu-item .anticon + .menu-link {
    margin-left: 10px;
}

.ant-menu.ant-menu-inline-collapsed > .ant-menu-item .anticon + .menu-link {
    display: inline-block;
    opacity: 0;
}
</style>