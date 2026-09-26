import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17211b",
        paper: "#f5f6f0",
        signal: "#d86a3d",
        moss: "#59715d",
      },
    },
  },
  plugins: [],
};

export default config;
