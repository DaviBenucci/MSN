/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#1f2933',
        msn: {
          green: '#1f8a5f',
          blue: '#2563eb',
          amber: '#b7791f',
          red: '#c2410c',
        },
      },
      boxShadow: {
        panel: '0 18px 45px rgba(31, 41, 51, 0.08)',
      },
    },
  },
  plugins: [],
}
