import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'   // ← add this

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),   // ← this fixes @ alias on Windows
    },
  },
  optimizeDeps: {
    disabled: true,   // ← keeps skipping the buggy scan
  },
})
