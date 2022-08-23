import { createRouter, createWebHistory } from "vue-router"
import { authStore } from "./store/auth.store"
import LoginPage from './views/LoginPage.vue'
import DashboardPage from './views/DashboardPage.vue'
import ReviewListPage from './views/ReviewListPage.vue'
import SupportCenterPage from './views/SupportCenterPage.vue'
import AppearanceSettingPage from './views/settings/AppearanceSettingPage.vue'
import GoogleAPISettingPage from './views/settings/GoogleAPISettingPage.vue'
import CreateAccountPage from './views/CreateAccountPage.vue'
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
        path: '/dashboard/reviews/:store_slug',
        component: ReviewListPage,
        props:true
    },
    {
        name: 'customer.list',
        path: '/dashboard/customers',
        component: CustomerListPage,
        props:true
    },
    {
        name: 'account',
        path: '/dashboard/account',
        component: CreateAccountPage
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

    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['login'];
    const authRequired = !publicPages.includes(to.name);
    const auth = authStore();

    if (authRequired && !auth.isLoggedIn) {
        auth.returnUrl = to.fullPath;
        return '/dashboard/login';
    }
})

export default router