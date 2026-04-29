import "./Navbar.css";

const Navbar = () => {
  return (
    <form className="form">
      <button type="submit">
        <svg width="17" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M7.667 12.667A5.333 5.333 0 107.667 2a5.333 5.333 0 000 10.667zM14.334 14l-2.9-2.9"
            stroke="currentColor"
            strokeWidth="1.333"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      <input
        className="input"
        placeholder="Buscar..."
        required
        type="text"
      />

      <button className="reset" type="reset">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </form>
  );
};

export default Navbar;