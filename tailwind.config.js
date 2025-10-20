/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './language_listening_practice_app/templates/**/*.html',
    './language_listening_practice_app/**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
