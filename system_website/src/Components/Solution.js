import React, { useState, useEffect, useRef, useCallback } from "react";
import "./Solution.css";

function Solution() {
    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [showParagraph, setShowParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    // State for header visibility
    const [headerVisible, setHeaderVisible] = useState(false);
    const solutionRef = useRef(null);

    // Scroll handler to adjust font size and show paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && solutionRef.current) {
            const element = solutionRef.current;
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
            if (solutionRef.current) {
                const bounding = solutionRef.current.getBoundingClientRect();
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
        <section className="solution" ref={solutionRef}>
            <h1 className={`solution_header ${headerVisible ? "slide-in" : "slide-out"}`} style={{ fontSize: `${fontSize}px` }}>
            Our Solution
            </h1>
            <div className={`solution_content ${showParagraph ? "visible" : ""}`}>
                <div className="solution_content_text">
                    <p>
                    The IFS DriverAlert delivers a cost-effective, offline, and user-friendly solution for drowsiness detection. It enhances road safety by reliably detecting eye closures and promptly alerting drivers, making it a practical and accessible alternative for any vehicle. This system ensures privacy by processing data locally without storing any images or video.
                    </p>
                </div>
                <div className="video_container">
                    <iframe
                        width="560"
                        height="315"
                        src="https://www.youtube.com/embed/bguCP2fWp50"
                        title="YouTube video player"
                        frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                    ></iframe>
                </div>
            </div>
        </section>
    );
}

export default Solution;
