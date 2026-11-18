/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#0A1128',
          blue: '#1E3A8A',
          royal: '#2563EB',
          cyan: '#06B6D4',
          mint: '#10B981',
          violet: '#8B5CF6',
          amber: '#F59E0B',
          rose: '#F43F5E',
          darkbg: '#0B1120',
          darkcard: '#111827',
          darkborder: '#1E293B',
          lightbg: '#F8FAFC',
          lightcard: '#FFFFFF',
          lightborder: '#E2E8F0'
        }
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans Tamil', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
