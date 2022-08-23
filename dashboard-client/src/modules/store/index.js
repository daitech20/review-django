import { routes, routerHooks } from './routes'

export default {
    name: 'store',
    routes: routes,
    routerHooks: routerHooks,
    install: () => {
        console.log("Installed module store")
    }
}
