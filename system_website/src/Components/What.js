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

        const currentRef = whatRef.current; // Store ref in a variable to avoid stale closure
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
        <section className="what" ref={whatRef}>
        <h1 style={{ fontSize: `${fontSize}px` }}>What is IFS-DriverAlert</h1>
        <p className={`what-paragraph ${showParagraph ? "visible" : ""}`}>
            This what provides what are we doing.
        </p>
        </section>
    );
}

export default What;
