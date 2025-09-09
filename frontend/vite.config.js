import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // IMPORTANT : on prépare la sortie pour Django
  build: {
    outDir: 'dist_django',
    assetsDir: 'assets',
    manifest: false,
    sourcemap: false,
    rollupOptions: {
      output: {
        entryFileNames: 'assets/index.js',
        chunkFileNames: 'assets/chunk-[name].js',
        assetFileNames: 'assets/[name][extname]',
      },
    },
  },
  // Les assets seront servis par Django sous /static/react/
  base: '/static/react/',
})
