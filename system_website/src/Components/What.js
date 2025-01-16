import React, { useState, useEffect, useRef, useCallback } from "react";
import "./What.css";

function What() {
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
            <h1 className="what_header" style={{ fontSize: `${fontSize}px` }}>What is IFS-DriverAlert</h1>
            <div className={`what_content ${showParagraph ? "visible" : ""}`}>
                <p>
                The IFS DriverAlert System is a standalone device that uses a Raspberry Pi 5, a camera, and a speaker to detect driver drowsiness. It monitors the driver’s eyes and mouth to detect closed eyes or yawning in real-time. The system operates offline, processes data locally, and is compact enough to be installed in any vehicle.
                </p>
                <p>
                ...
                </p>
            </div>
        </section>
    );
}

export default What;
