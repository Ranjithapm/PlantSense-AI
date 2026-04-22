import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/predict': 'http://127.0.0.1:5001',
      '/static':  'http://127.0.0.1:5001',
      '/status':  'http://127.0.0.1:5001',
    },
  },
})
