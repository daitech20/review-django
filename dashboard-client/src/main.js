import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import { createPinia } from 'pinia'
import fakeAuth from './services/review_app/_fake.service'

import router from './routes'

const app = createApp(App)
app.use(createPinia())
app.use(Antd)
//app.component('a-icon', AntdIcon)
app.use(router)

if (parseInt(import.meta.env.VITE_ENABLE_MOCKING) === 1) {
    fakeAuth().enableMocking(true);
}

app.mount('#app')
