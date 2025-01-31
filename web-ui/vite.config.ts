import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/benchcompress/', // Base URL for GitHub Pages deployment
  define: {
    __BUILD_DATE__: JSON.stringify(new Date().toLocaleDateString())
  }
})
