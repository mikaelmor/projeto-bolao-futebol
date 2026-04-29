export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins : ["Arial", "sans-serif", "mono", "Monaco", "Monospace"]
      }
    },
  },
  plugins: [],
};

module.exports = {
  theme: {
    extend: {
      keyframes: {
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-8px)' },
          '50%': { transform: 'translateX(8px)' },
          '75%': { transform: 'translateX(-8px)' },
        }
      },
      animation: {
        shake: 'shake 0.4s ease-in-out',
      }
    },
  },
}