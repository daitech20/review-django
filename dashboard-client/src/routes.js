import { createRouter, createWebHistory } from "vue-router"

const routes = [

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