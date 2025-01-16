import React, { useState, useEffect, useRef, useCallback } from "react";
import "./How.css";

function How() {
    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [showParagraph, setShowParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    const howRef = useRef(null);

    // Scroll handler to adjust font size and show paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && howRef.current) {
            const element = howRef.current;
            const bounding = element.getBoundingClientRect();
            const elementTop = bounding.top; // Distance from top of viewport to element

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

    // Intersection observer to detect when the section is in view
    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
            if (entry.isIntersecting) {
                setStartDecreasing(true); // Start decreasing font size when visible
            }
            },
            { threshold: 0.1 } // Trigger when at least 10% of the section is visible
        );

        const currentRef = howRef.current; // Store ref in a variable to avoid stale closure
        if (currentRef) {
            observer.observe(currentRef);
        }

        return () => {
            if (currentRef) {
            observer.unobserve(currentRef);
            }
        };
    }, []);

    // Scroll event listener
    useEffect(() => {
        window.addEventListener("scroll", handleScroll);
        return () => {
        window.removeEventListener("scroll", handleScroll);
        };
    }, [handleScroll]);

    return (
        <section className="how" ref={howRef}>
            <h1 className="how_header" style={{ fontSize: `${fontSize}px` }}>Implementation Approach</h1>
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
