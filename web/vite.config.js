import { defineConfig } from 'vite';

export default defineConfig({
    type: 'module',
    server: {
        proxy: {
            "/api": {
                target: "http://192.168.137.8:8000",
                changeOrigin: true,
                secure: false
            },
        },
    },
    // some other configuration
})
