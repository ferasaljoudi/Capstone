import React, { useState, useEffect, useRef, useCallback } from "react";
import "./Why.css";

function Why() {
    // Initial font size
    const [fontSize, setFontSize] = useState(80);
    // Control paragraph visibility
    const [showParagraph, setShowParagraph] = useState(false);
    // Start decreasing font size
    const [startDecreasing, setStartDecreasing] = useState(false);
    // State for header visibility
    const [headerVisible, setHeaderVisible] = useState(false);
    const whyRef = useRef(null);

    // Scroll handler to adjust font size and show paragraph
    const handleScroll = useCallback(() => {
        if (startDecreasing && whyRef.current) {
            const element = whyRef.current;
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
            if (whyRef.current) {
                const bounding = whyRef.current.getBoundingClientRect();
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
        <section className="why" ref={whyRef}>
            <h1 className={`why_header ${headerVisible ? "slide-in" : "slide-out"}`} style={{ fontSize: `${fontSize}px` }}>
                Why the System Matters
            </h1>
            <div className={`why_content ${showParagraph ? "visible" : ""}`}>
                <p>
                    In Saskatchewan, Canada, driver fatigue causes over 145 injuries and 7 deaths every year on average, according to <a href="https://sgi.sk.ca/pro-driver/-/knowledge_base/pro-drivers/driver-condition" title="SGI" target="_blank" rel="noopener noreferrer">SGI</a>. Drowsy driving is treated as seriously as impaired driving due to its impact on reaction time and judgment.
                </p>
                <p>
                    In the United States, the <a href="https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6326a1.htm?s_cid=mm6326a1_w" title="Centers for Disease Control and Prevention" target="_blank" rel="noopener noreferrer">CDC</a> reports that up to 7,500 fatal crashes annually (about 25% of all fatal crashes) involve drowsy driving. Nearly 1 in 25 adults admitted to falling asleep while driving in the past month.
                </p>
                <p>
                    These numbers show the urgent need for an affordable and effective drowsiness detection system. Although drowsiness detection systems are available in high-end and premium vehicles, they are often too expensive for most drivers. IFS-DriverAlert offers a low-cost, offline alternative that brings this life-saving technology to any standard vehicle.
                </p>
            </div>
        </section>
    );
}

export default Why;
