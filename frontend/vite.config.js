import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/login': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/forgot-password': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/reset-password': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
