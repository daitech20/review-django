import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import AntdIcon from './components/icon/AntdIcon.vue'
import { createPinia } from 'pinia'

import router from './routes'

const app = createApp(App)
app.use(createPinia())
app.use(Antd)
app.component('a-icon', AntdIcon)
app.use(router)
app.mount('#app')
