import React, { useState, useEffect, useRef, useCallback } from "react";
import "./Solution.css";

function Solution() {
    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [ssolutionParagraph, setSsolutionParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    const solutionRef = useRef(null);

    // Scroll handler to adjust font size and ssolution paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && solutionRef.current) {
            const element = solutionRef.current;
            const bounding = element.getBoundingClientRect();
            const elementTop = bounding.top; // Distance from top of viewport to element

            // Higher value slows down the decrease
            const scrollFactor = 10;
            const newFontSize = Math.max(
                40,
                Math.min(80, 80 - (window.innerHeight - elementTop) / scrollFactor)
            );

            setFontSize(newFontSize);

            // Ssolution paragraph when font size hits 40
            if (newFontSize <= 40) {
            setSsolutionParagraph(true);
            } else {
            setSsolutionParagraph(false);
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

        const currentRef = solutionRef.current; // Store ref in a variable to avoid stale closure
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
        <section className="solution" ref={solutionRef}>
            <h1 className="solution_header" style={{ fontSize: `${fontSize}px` }}>Our Solution</h1>
            <div className={`solution_content ${ssolutionParagraph ? "visible" : ""}`}>
                <div className="solution_content_text">
                    <p>
                    The IFS DriverAlert delivers a cost-effective, offline, and user-friendly solution for drowsiness detection. It enhances road safety by reliably detecting eye closures and promptly alerting drivers, making it a practical and accessible alternative for any vehicle. This system ensures privacy by processing data locally without storing any images or video.
                    </p>
                    <p>
                    ...
                    </p>
                </div>
            </div>
        </section>
    );
}

export default Solution;
