/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#5a8a72',
          light: '#edf5f0',
          dark: '#3a6b51',
        },
        text: {
          DEFAULT: '#212529',
          light: '#e9ecef',
        },
        background: {
          DEFAULT: '#fcfaf5',
          dark: '#121212',
        },
        link: {
          DEFAULT: '#2d5d7b',
          hover: '#1c3d5a',
          light: '#81b0d1',
        },
        border: {
          DEFAULT: '#e9ecef',
          dark: '#2c2c2c',
        },
      },
      fontFamily: {
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
        'serif': ['EB Garamond', 'Georgia', 'Times New Roman', 'serif'],
        'mono': ['Fira Code', 'monospace'],
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '70ch',
            color: '#212529',
            a: {
              color: '#2d5d7b',
              '&:hover': {
                color: '#1c3d5a',
              },
            },
            h1: {
              color: '#111827',
              fontWeight: '500',
            },
            h2: {
              color: '#111827',
              fontWeight: '500',
            },
            h3: {
              color: '#111827',
              fontWeight: '500',
            },
            strong: {
              color: '#111827',
            },
            blockquote: {
              borderLeftColor: '#5a8a72',
              backgroundColor: '#edf5f0',
              color: '#495057',
              fontStyle: 'italic',
            },
            code: {
              color: '#111827',
            },
            pre: {
              backgroundColor: '#f8f9fa',
              color: '#212529',
            },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
  darkMode: 'media',
}