import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
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
  }
})
