const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
	extend: {
		keyframes: {
			'fade-in-down': {
				'0%': {
					opacity: '0',
					transform: 'translateY(100%)'
				},
				'100%': {
					opacity: '1',
					transform: 'translateY(-50%)'
				},
			}
		},
		animation: {
			'fade-in-down': 'fade-in-down 0.5s ease-out'
		}
	}
  },
  plugins: [],
}
