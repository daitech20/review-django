function addRouteMeta(route, name, value) {
    route.meta = route.meta || {}
    route.meta[name] = value
}

export function loadModule(module, context) {
    // Load routes
    (module.routes || []).map(route => {
        addRouteMeta(route, 'moduleName', module.name)
        context.router.addRoute(route)
    })

    const routerHooks = module.routerHooks || {};
    for (let hook in routerHooks) {
        context.router[hook](routerHooks[hook]);
    }

    /*
    const i18nMessages = module.i18nMessages || {}
    context.registerModuleMessages(module.name, i18nMessages)
    */

    const install = module.install || (() => {});
    install();
}

export function loadModules(modules, context) {
    for (let i = 0; i < modules.length; i++) {
        loadModule(modules[i], context)
    }
}