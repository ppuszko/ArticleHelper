/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#0f1117',
          raised: '#161b27',
          border: '#1e2535',
        },
        accent: {
          DEFAULT: '#6c8cff',
          hover: '#8aa3ff',
          muted: '#3d5299',
        },
        text: {
          primary: '#e8eaf0',
          secondary: '#8b92a5',
          placeholder: '#4a5168',
        },
        status: {
          error: '#ff6b6b',
          success: '#4ecdc4',
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
