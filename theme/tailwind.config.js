/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../artshop/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        button: "#7f5af0",
        "button-hover": "#624bd2",
        "secondary-button": "#fca311",
        "secondary-button-hover": "#e69400",
        "container-background": "#fffffe",
        "page-background": "#f9f9f9",
        "heading-text": "#2b2c34",
        "paragraph-text": "#555",
        link: "#3b82f6",
        "link-hover": "#2563eb",
        "border-color": "#d1d5db",
        "secondary-border-color": "#e5e7eb",
        "secondary-background": "#fafafa",
        subheading: "#3f3f46",
        "secondary-subheading": "#71717a",
        "secondary-container": "#f3f4f6",
        "secondary-heading": "#1f2937",
        "secondary-paragraph-text": "#6b7280",
        icon: "#4b5563",
        "icon-hover": "#374151",
        "secondary-icon": "#9ca3af",
        "secondary-icon-hover": "#6b7280",
      },
    },
  },
  plugins: [],
}