import React, { useState, useEffect, useRef, useCallback } from "react";
import "./Why.css";

function Why() {
    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [showParagraph, setShowParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    const whyRef = useRef(null);

    // Scroll handler to adjust font size and show paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && whyRef.current) {
            const element = whyRef.current;
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

        const currentRef = whyRef.current; // Store ref in a variable to avoid stale closure
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
        <section className="why" ref={whyRef}>
            <h1 className="why_header" style={{ fontSize: `${fontSize}px` }}>Why the System Matters</h1>
            <div className={`why_content ${showParagraph ? "visible" : ""}`}>
                <p>
                Drowsy driving significantly increases the risk of accidents, causing injuries and fatalities. Current solutions are expensive and integrated into high-end vehicles, making them inaccessible to many drivers. The IFS DriverAlert addresses this gap by providing an affordable, easy-to-install, and effective way to alert drivers when they show signs of drowsiness, thus improving road safety.
                </p>
                <p>
                ...
                </p>
            </div>
        </section>
    );
}

export default Why;
