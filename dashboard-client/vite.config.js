import { defineConfig, loadEnv } from 'vite'
import { fileURLToPath, URL } from 'url'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default ({mode}) => {
  // Load app-level env vars to node-level env vars.
  process.env = {...process.env, ...loadEnv(mode, process.cwd() + '/../')}

  return defineConfig({
    plugins: [vue()],
    base: 'http://localhost:8088',
    build: {
      outDir: './../staticfiles/dashboard/dist',
      rollupOptions: {
        output: {
            // Prevent vendor.js being created
            manualChunks: undefined,
            entryFileNames: "assets/[name].js",
            // this got rid of the hash on style.css
            assetFileNames: "assets/[name].[ext]",
        },
      },
      // Prevent vendor.css being created
      cssCodeSplit: false,
      // prevent some warnings
      chunkSizeWarningLimit: 60000,
    },
    resolve: {
      alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url))
      },
      dedupe: ['vue']
    }
  })
}