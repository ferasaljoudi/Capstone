import React, { useCallback, useEffect, useRef, useState } from "react";
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
                        IFS-DriverAlert provides an affordable, standalone, and offline drowsiness detection system that can be added to any standard vehicle. It uses AI-powered facial monitoring to detect signs of fatigue and responds with progressive audio alerts to help keep drivers safe. This system ensures privacy by processing data locally without storing any images or video.
                    </p>
                    <p>
                        The below video shows the system components and operation.
                    </p>
                </div>
                <div className="video_container">
                    <div className="responsive_iframe">
                        <iframe
                        src="https://www.youtube.com/embed/o84s45abvUQ"
                        title="YouTube video player"
                        frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                        ></iframe>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Solution;
