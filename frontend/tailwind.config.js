/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary': '#1f4e78',
        'secondary': '#2e5c8a',
        'accent': '#4a90e2',
      },
    },
  },
  plugins: [],
}
