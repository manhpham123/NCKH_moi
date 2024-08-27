import { defineConfig } from "vite";
import solidPlugin from "vite-plugin-solid";

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    port: 3001,
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
  build: {
    target: "esnext",
    sourcemap: true,
  },
  base: "./",
});
