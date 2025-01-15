import React from "react";
import { motion } from "framer-motion";
import "./Header.css";

function Header() {
    const text = "Drowsy driving is one of the leading causes of road accidents, but with IFS DriverAlert, you can drive smarter and safer. Discover how this innovative system monitors your focus in real-time and ensures you're always alert behind the wheel. Scroll down to learn more about what makes this solution essential for road safety!".split(" ");

    return (
        <header className="header">
            <div className="header-background"></div>
            <h1 className="header_heading">IFS-DriverAlert</h1>
            <h2 className="header_subheading">Intelligent Focus System</h2>
            <div className="header_text">
                {text.map((word, index) => (
                    <motion.span
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{
                            duration: 2,
                            delay: 1.5 + index * 0.1
                        }}
                        key={index}
                    >
                        {word}{" "}
                    </motion.span>
                ))}
            </div>
        </header>
    );
}

export default Header;
