import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import AntdIcon from './components/icon/AntdIcon.vue'
import { createPinia } from 'pinia'
import { loadModules } from './module'
import module_registries from './module_registries'
import router from './routes'

import 'ant-design-vue/dist/antd.css'

const app = createApp(App)
app.use(createPinia())
app.use(Antd)
app.component('a-icon', AntdIcon)

loadModules(module_registries, {
    router: router
})

app.use(router)
app.mount('#app')
