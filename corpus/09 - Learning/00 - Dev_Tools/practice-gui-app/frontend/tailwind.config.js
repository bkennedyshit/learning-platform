/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        gh: {
          bg: "#0d1117",
          panel: "#161b22",
          text: "#c9d1d9",
          accent: "#58a6ff",
          border: "#30363d",
          muted: "#8b949e",
        },
      },
      fontFamily: {
        serif: ['"Source Serif 4"', "Merriweather", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
};
