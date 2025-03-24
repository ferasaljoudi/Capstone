import React, { useState, useEffect, useRef, useCallback } from "react";
import "./How.css";

function How() {
    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [showParagraph, setShowParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    // State for header visibility
    const [headerVisible, setHeaderVisible] = useState(false);
    const howRef = useRef(null);

    // Scroll handler to adjust font size and show paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && howRef.current) {
            const element = howRef.current;
            const bounding = element.getBoundingClientRect();
            const elementTop = bounding.top;

            // Higher value slows down the decrease
            const scrollFactor = 10;
            const newFontSize = Math.max(
                40,
                Math.min(80, 80 - (window.innerHeight - elementTop) / scrollFactor)
            );

            setFontSize(newFontSize);

            // Show paragraph when font size hits 40
            if (newFontSize <= 40) {
                setShowParagraph(true);
            } else {
                setShowParagraph(false);
            }
        }
    }, [startDecreasing]);

    useEffect(() => {
        const handleScrollVisibility = () => {
            if (howRef.current) {
                const bounding = howRef.current.getBoundingClientRect();
                const sectionVisible = bounding.top < window.innerHeight && bounding.bottom > 0;

                setHeaderVisible(sectionVisible);
                if (sectionVisible) {
                    setStartDecreasing(true);
                }
            }
        };

        window.addEventListener("scroll", handleScrollVisibility);
        return () => {
            window.removeEventListener("scroll", handleScrollVisibility);
        };
    }, []);

    useEffect(() => {
        window.addEventListener("scroll", handleScroll);
        return () => {
            window.removeEventListener("scroll", handleScroll);
        };
    }, [handleScroll]);

    return (
        <section className="how" ref={howRef}>
            <h1 className={`how_header ${headerVisible ? "slide-in" : "slide-out"}`} style={{ fontSize: `${fontSize}px` }}>
                Implementation Approach
            </h1>
            <div className={`how_content ${showParagraph ? "visible" : ""}`}>
            <ul>
                <li>📷 A camera captures real-time video of the driver's face.</li>
                <li>🧠 MediaPipe and OpenCV are used to detect eye closure, yawning, and looking away.</li>
                <li>🔊 When signs of drowsiness or distraction are detected, a progressive audio alert is played through a speaker.</li>
                <li>⚡ The system is powered by the car's 12V outlet using a step-down converter to provide 5V to the Raspberry Pi 5.</li>
                <li>🛰️ A NEO-6M GPS module monitors vehicle speed to enable Auto mode.</li>
                <li>🚗 In Auto mode, detection only runs when the car speed is at least 20km/h, reducing power and avoiding false alerts when parked.</li>
                <li>🛑 In Manual (On) mode, detection runs continuously, useful in areas like tunnels where GPS may not work.</li>
                <li>🔁 An audio reminder plays every 10 minutes if Auto mode is active but speed is not detected, prompting the driver to manually turn detection on.</li>
                <li>🔐 The system operates entirely offline, with no data storage or transmission, ensuring privacy and low power usage.</li>
            </ul>
            </div>
        </section>
    );
}

export default How;
