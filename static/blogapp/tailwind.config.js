// tailwind.config.js
const plugin = require("tailwindcss/plugin");

module.exports = {
  theme: { 
    colors: {
      transparent: 'transparent',
      white: '#FFFFFF',
      black: '#000000',
      nav: '#0D0D0E',
      button: '#495052',
      ph: '#AFB0BF',
      gray: '#6C6E73',
      faint: '#858697',
      blue: {
        '100': '#63B3ED',
        '500': '#2F80ED'
      },
      body: {
        '100': '#262629',
        '500': '#19191C'
      },
      red: {
        '100': '#F16D6D',
        '500': '#EB5757'
      },
      green: {
        '100': '#6FCF97',
        '300': '#27AE60',
        '500': '#219653'
      },
      orange: {
        '100': '#F2994A',
        '500': '#E47716'
      },
    },
    extend: {
      screens: {
        'landscape': {'raw': '(orientation: landscape)'},
      },
      boxShadow: {
        'white': '0 1px 3px 0 rgba(255, 255, 255, 0.1), 0 1px 2px 0 rgba(255, 255, 255, 0.06)',
        'white-xs':	'0 0 0 1px rgba(255, 255, 255, 0.05)',
        'white-sm':	'0 1px 2px 0 rgba(255, 255, 255, 0.05)',
        'white-md': '0 4px 6px -1px rgba(255, 255, 255, 0.1), 0 2px 4px -1px rgba(255, 255, 255, 0.06)',
        'white-lg': '0 10px 15px -3px rgba(255, 255, 255, 0.1), 0 4px 6px -2px rgba(255, 255, 255, 0.05)',
        'white-xl': '0 20px 25px -5px rgba(255, 255, 255, 0.1), 0 10px 10px -5px rgba(255, 255, 255, 0.04)',
        'white-2xl': '0 25px 50px -12px rgba(255, 255, 255, 0.25)',
      },
      spacing: {
        '65': '20rem',
        '66': '25rem',
        '67': '30rem',
        '68': '35rem',
        '69': '40rem',
      },
      inset: {
        'px': '1px',
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '5': '1.25rem',
        '6': '1.5rem',
        '8': '2rem',
        '10': '2.5rem',
        '12': '3rem',
        '16': '4rem',
        '20': '5rem',
        '24': '6rem',
        '32': '8rem',
        '40': '10rem',
        '48': '12rem',
        '56': '14rem',
        '64': '16rem',
        '-px': '-1px',
        '-1': '-0.25rem',
        '-2': '-0.5rem',
        '-3': '-0.75rem',
        '-4': '-1rem',
        '-5': '-1.25rem',
        '-6': '-1.5rem',
        '-8': '-2rem',
        '-10': '-2.5rem',
        '-12': '-3rem',
        '-16': '-4rem',
        '-20': '-5rem',
        '-24': '-6rem',
        '-32': '-8rem',
        '-40': '-10rem',
        '-48': '-12rem',
        '-56': '-14rem',
        '-64': '-16rem',
      }
    },
  },
  variants: [
    'responsive', 'group-hover', 'focus-within',
    'first', 'last', 'odd', 'even', 'hover',
    'focus', 'active', 'visited', 'disabled'
  ],
  plugins: [],
};
