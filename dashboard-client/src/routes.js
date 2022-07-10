import { createRouter, createWebHistory } from "vue-router"
import DashboardPage from './views/DashboardPage.vue'
import ReviewListPage from './views/ReviewListPage.vue'
import SupportCenterPage from './views/SupportCenterPage.vue'
import AppearanceSettingPage from './views/settings/AppearanceSettingPage.vue'
import GoogleAPISettingPage from './views/settings/GoogleAPISettingPage.vue'

const routes = [
    {
        name: 'dashboard',
        path: '/dashboard',
        component: DashboardPage
    },
    {
        name: 'review.list',
        path: '/dashboard/reviews',
        component: ReviewListPage
    },
    {
        name: 'support_center',
        path: '/dashboard/support-center',
        component: SupportCenterPage
    },
    {
        name: 'setting.appearance',
        path: '/dashboard/settings/appearance',
        component: AppearanceSettingPage
    },
    {
        name: 'setting.google_api',
        path: '/dashboard/settings/google-api',
        component: GoogleAPISettingPage
    },
]

const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHistory(),
    routes // short for `routes: routes`
})

router.beforeEach(async(to) => {
    // Always redirect to dashboard
    if (! /^\/dashboard\/(.*)/.test(to.path)) {
        return "/dashboard/"
    }
})

export default router