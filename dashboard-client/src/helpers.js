export function asset(uri) {
    return import.meta.env.VITE_WEB_STATIC_URL + uri
}