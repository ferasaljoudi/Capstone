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
                <div className="how_content_text">
                    <p>
                    The system captures real-time video of the driver's face using a camera and processes it with OpenCV and MediaPipe to monitor the driver's eyes and mouth. If closed eyes or yawning is detected, an audible alert is triggered through a speaker to alert the driver. The system is powered via the vehicle’s 12V supply, uses a step-down converter for the Raspberry Pi, and runs Python-based software optimized for the Raspberry Pi 5's resources.
                    </p>
                    <p>
                    The system includes an audio reminder that plays every 10 minutes when the detection system is disabled. This feature ensures the driver is consistently reminded to activate the drowsiness detection system, enhancing overall safety.
                    </p>
                </div>
                <div className="how_content_box">
                    <div className="overlay camera-overlay"></div>
                    <div className="overlay cooler-overlay"></div>
                    <div className="overlay speaker-overlay"></div>
                </div>
            </div>
        </section>
    );
}

export default How;
