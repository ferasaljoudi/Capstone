import React, { useState, useEffect, useRef, useCallback } from "react";
import "./What.css";

function What() {
    // Download handler to download the manual PDF
    const handleDownload = () => {
        const link = document.createElement('a');
        link.href = '/IFS_UserManual.pdf';
        link.download = 'IFS_UserManual.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [showParagraph, setShowParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    const whatRef = useRef(null);

    // Scroll handler to adjust font size and show paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && whatRef.current) {
            const element = whatRef.current;
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
        const observer = new IntersectionObserver(
            ([entry]) => {
            if (entry.isIntersecting) {
                setStartDecreasing(true);
            }
            },
            { threshold: 0.1 }
        );

        const currentRef = whatRef.current;
        if (currentRef) {
            observer.observe(currentRef);
        }

        return () => {
            if (currentRef) {
            observer.unobserve(currentRef);
            }
        };
    }, []);

    useEffect(() => {
        window.addEventListener("scroll", handleScroll);
        return () => {
        window.removeEventListener("scroll", handleScroll);
        };
    }, [handleScroll]);

    return (
        <section className="what" ref={whatRef}>
            {/* <button className="download-btn desktop-download" onClick={handleDownload}>⤓ Download User Manual</button>
            <button className="download-btn mobile-download" onClick={() => window.open("/IFS_UserManual.pdf", "_blank")}>⤓ Download User Manual</button> */}
            <button className="download-btn" onClick={() => window.open("/IFS_UserManual.pdf", "_blank")}>⤓ Download User Manual</button>
            <h1 className="what_header" style={{ fontSize: `${fontSize}px` }}>What is IFS-DriverAlert</h1>
            <div className={`what_content ${showParagraph ? "visible" : ""}`}>
                <p>
                IFS-DriverAlert is a safety system designed to monitor a driver's face in real time and detect signs of drowsiness or distraction, such as eye closure, yawning, and looking away. It uses a camera, a Raspberry Pi 5, and MediaPipe AI models to analyze facial features and trigger alerts through a speaker. The goal is to reduce accidents caused by fatigue and inattention, especially in regular vehicles that don't have built-in driver monitoring systems.
                </p>
                <p>
                The system has an Auto and a Manual modes. In Auto mode, the detection system activates only when the car speed is at least 20km/h, which is done using a NEO-6M GPS module to monitor the speed. This prevents unnecessary alerts when the car is stopped. In Manual mode, detection runs continuously regardless of speed, which is useful in cases like tunnels where GPS signals may be weak. An audio reminder also plays every 10 minutes if Auto mode is on but speed is not detected, recommending the driver to switch to Manual mode.
                </p>
            </div>
        </section>
    );
}

export default What;
