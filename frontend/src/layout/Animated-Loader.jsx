import { motion, AnimatePresence } from "framer-motion";
import { useLocation, useOutlet } from "react-router-dom";
import { useEffect, useState } from "react";
import "../styles/loader.css"

const AnimatedLoader = () => {
  const location = useLocation();
  const outlet = useOutlet();

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);

    const timer = setTimeout(() => {
      setLoading(false);
    }, 800); 

    return () => clearTimeout(timer);
  }, [location.pathname]);

  return (
    <AnimatePresence mode="wait">

      {loading ? (
        <motion.div
          key="loader"
          className="flex items-center justify-center h-screen bg-[#020617]"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="container">
            <div className="ball">
              <div className="inner">
                <div className="line"></div>
                <div className="line line--two"></div>
                <div className="oval"></div>
                <div className="oval oval--two"></div>
              </div>
            </div>
            <div className="shadow"></div>
          </div>
        </motion.div>
      ) : (
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {outlet}
        </motion.div>
      )}

    </AnimatePresence>
  );
};

export default AnimatedLoader;