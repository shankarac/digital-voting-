import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    proxy: {
      "/auth": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/proposals": { target: "http://127.0.0.1:8000", changeOrigin: true },
      "/votes": { target: "http://127.0.0.1:8000", changeOrigin: true },
    },
  },
});
