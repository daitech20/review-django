import { createRouter, createWebHistory } from "vue-router"
import LoginPage from './views/LoginPage.vue'
import DashboardPage from './views/DashboardPage.vue'
import ReviewListPage from './views/ReviewListPage.vue'
import StoreListPage from './views/StoreListPage.vue'
import StoreDetailPage from './views/StoreDetailPage.vue'
import StoreCreatePage from './views/StoreCreatePage.vue'
import SupportCenterPage from './views/SupportCenterPage.vue'
import AppearanceSettingPage from './views/settings/AppearanceSettingPage.vue'
import GoogleAPISettingPage from './views/settings/GoogleAPISettingPage.vue'
import AccountListPage from './views/AccountListPage.vue'
import AccountCreatePage from './views/AccountCreatePage.vue'
import CustomerListPage from './views/CustomerListPage.vue'

const routes = [
    {
        name: 'dashboard',
        path: '/dashboard',
        component: DashboardPage
    },
    {
        name: 'login',
        path: '/dashboard/login',
        component: LoginPage
    },
    {
        name: 'review.list',
        path: '/dashboard/reviews',
        component: ReviewListPage
    },
    {
        name: 'store.list',
        path: '/dashboard/stores',
        component: StoreListPage
    },
    {
        name: 'store.detail',
        path: '/dashboard/store/:store_slug',
        component: StoreDetailPage,
        props: true
    },
    {
        name: 'store.create',
        path: '/dashboard/stores/create',
        component: StoreCreatePage
    },
    {
        name: 'customer.list',
        path: '/dashboard/customers',
        component: CustomerListPage
    },
    {
        name: 'account.create',
        path: '/dashboard/account/create',
        component: AccountCreatePage
    },
    {
        name: 'account.list',
        path: '/dashboard/account',
        component: AccountListPage
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