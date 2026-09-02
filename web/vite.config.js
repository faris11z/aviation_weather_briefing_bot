import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/aviation_weather_briefing_bot/",
  server: {
    port: 3000,
  },
});
