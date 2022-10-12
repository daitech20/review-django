import { createRouter, createWebHistory } from "vue-router"
import { authStore } from "./store/auth.store"
import LoginPage from './views/login/LoginPage.vue'
import DashboardPage from './views/DashboardPage.vue'
import ReviewListPage from './views/reviews/ReviewListPage.vue'
import StoreListPage from './views/store/StoreListPage.vue'
import StoreDetailPage from './views/store/StoreDetailPage.vue'
import StoreCreatePage from './views/store/StoreCreatePage.vue'
import SupportCenterPage from './views/support/SupportCenterPage.vue'
import AppearanceSettingPage from './views/settings/AppearanceSettingPage.vue'
import GoogleAPISettingPage from './views/settings/GoogleAPISettingPage.vue'
import AccountListPage from './views/accounts/AccountListPage.vue'
import AccountCreatePage from './views/accounts/AccountCreatePage.vue'
import AccountDetailPage from './views/accounts/AccountDetailPage.vue'
import AccountResetPasswordPage from './views/accounts/AccountResetPasswordPage.vue'
import AccountChangePasswordPage from './views/accounts/AccountChangePasswordPage.vue'
import CustomerListPage from './views/customers/CustomerListPage.vue'
import MessagesListPage from './views/service/MessagesListPage.vue'

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
        params: true
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
        name: 'account.detail',
        path: '/dashboard/account/:username',
        component: AccountDetailPage,
        params: true
    },
    {
        name: 'account.resetpassword',
        path: '/dashboard/account/resetpassword/:username',
        component: AccountResetPasswordPage,
        params: true
    },
    {
        name: 'account.changepassword',
        path: '/dashboard/account/changepassword/:username',
        component: AccountChangePasswordPage,
        params: true
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
    {
        name: 'service.messages.list',
        path: '/dashboard/service/messages',
        component: MessagesListPage
    }
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