import React from "react";
import "./Footer.css";

function Footer() {
    // Download handler to download the manual PDF
    const handleDownload = () => {
        const link = document.createElement("a");
        link.href = "/IFS_UserManual.pdf";
        link.download = "IFS_UserManual.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
    return (
        <footer className="footer">
        <div className="footer-top">
            <div className="footer-left">
                <p className="footer-title">Core Technologies</p>
                <a href="https://www.raspberrypi.com/products/raspberry-pi-5/" target="_blank" rel="noopener noreferrer">Raspberry Pi 5</a>
                <a href="https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker" target="_blank" rel="noopener noreferrer">MediaPipe</a>
                <a href="https://opencv.org/" target="_blank" rel="noopener noreferrer">OpenCV</a>
            </div>
            <div className="footer-right">
                <p className="footer-title">Resources</p>
                <a href="https://github.com/ferasaljoudi/Capstone" target="_blank" rel="noopener noreferrer">GitHub</a>
                {/* <a href="/IFS_UserManual.pdf" target="_blank" rel="noopener noreferrer" className="mobile-download">⤓ Download Manual</a>
                <a href="#download" onClick={handleDownload} className="desktop-download">⤓ Download Manual</a> */}
                <a href="/IFS_UserManual.pdf" target="_blank" rel="noopener noreferrer">⤓ Download Manual</a>
            </div>
        </div>
        <div className="footer-bottom">
            ©2025 IFS-DriverAlert. All rights reserved.
        </div>
        </footer>
    );
}

export default Footer;
