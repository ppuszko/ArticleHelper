/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#d1ccbf',
          raised: '#e6e0d5',
          border: '#b5ae9f',
        },
        accent: {
          DEFAULT: '#5d7a51',
          hover: '#455b3c',
          muted: '#384930',
        },
        text: {
          primary: '#2b3027',
          secondary: '#5d6659',
          placeholder: '#919b8d',
        },
        status: {
          error: '#a24b43',
          success: '#466b4c',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
