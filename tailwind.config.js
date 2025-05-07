module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './theme/static/src/**/*.css',
    './**/*.js',
    './**/*.py',
  ],
  safelist:[
    'text-3xl', 'font-bold', 'tracking-tight', 'text-heading-text',
    'text-link', 'text-link-hover',
    'bg-button', 'bg-button-hover', 'bg-secondary-button',
    'border', 'border-button',
    'text-white', 'rounded', 'rounded-xl',
    'tracking-tight', 'card', 'fade-in',
    'py-2', 'py-3', 'px-3', 'px-4', 'text-sm', 'font-semibold'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [...defaultTheme.fontFamily.sans],
      },
      ringColor: {
        primary: '#B28538',
      },
      colors: {
        'heading-text': '#2D2814',  // drab-dark-brown
        'paragraph-text': '#666D4B',  // reseda-green
        'subheading': '#7F4B30',  // russet
        'secondary-subheading': '#424C21', // dark-moss-green
        'link': '#B2682C',  // tigers-eye
        'link-hover': '#B28538',  // dark-goldenrod
        'warning': '#E6B44A',   //hunyadi-yellow
        'success': '#424C21', // dark-moss-green
        'danger': '#B00020',  //dark red for errors
        'background': '#EBDDC1',  // pearl
        'page-background': '#beccc0',  //sames as background
        'container-background': '#FAF8F3', // lighter pearl for cards
        'surface': '#FAF8F3',  // card/modals (lighter)
        'border-color': '#D7CBB3',  // subtle version of pearl
        'button': '#7F4B30',  //russet
        'button-hover': '#B2682C',  // tigers-eye
        'secondary-button': '#424C21',  // dark-moss-green
        'overlay': '#173125',  // dark overlay
        'primary': '#B28538',  // dark- goldenrod
        'accent': '#E6B44A',  // hunyadi-yellow
      },
    },
  },
  plugins: [],
};