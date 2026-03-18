import { motion, AnimatePresence } from "framer-motion";
import { useLocation, useOutlet } from "react-router-dom";

const AnimatedLayout = () => {
  const location = useLocation();
  const outlet = useOutlet();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        {outlet}
      </motion.div>
    </AnimatePresence>
  );
};

export default AnimatedLayout;