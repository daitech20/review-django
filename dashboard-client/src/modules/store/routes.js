export const routes = [
    {
        name: 'store.list',
        path: '/dashboard/stores',
        component: () => import('./views/StoreListPage.vue')
    },
    {
        name: 'store.detail',
        path: '/dashboard/store/:store_slug',
        component: () => import('./views/StoreDetailPage.vue'),
        props: true
    },
    {
        name: 'store.create',
        path: '/dashboard/stores/create',
        component: () => import('./views/StoreDetailPage.vue')
    },
];

export const routerHooks = {};