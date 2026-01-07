import { use, useState } from "react";
import axios from "axios";

function Shortener() {
    const [longUrl, setLongUrl] = useState("");
    const [shortUrl, setShortUrl] = useState("");
    const [error, setError] = useState("");
    const [copied, setCopied] = useState(false);
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";


    const handleShorten = async () => {
        setError("");
        setShortUrl("");

        if (!longUrl) {
            setError("Please enter a URL");
            return
        }

        try {
            const response = await axios.post(
                `${API_BASE_URL}/api/shorten/`,
                { url: longUrl }
            );

            setShortUrl(response.data.short_url);

        } catch (err) {
            setError("Something went wrong !!");
            console.error(err)
        }

    };


    return (
        <>
            <div className="shortener">
                <h2 className="title">URL SHORTENER</h2>
                <input
                    type="text"
                    className="url-input"
                    placeholder="Enter long URL"
                    value={longUrl}
                    onChange={(e) => setLongUrl(e.target.value)}
                />
                <button className="submit-button" onClick={handleShorten}>Shorten</button>

                {error && <p className="error-text" style={{ color: "red" }}>{error}</p>}

                {shortUrl && (
                    <div>
                        <hr className="line" />
                        <div className="result">
                            <a className="url-link" href={shortUrl} target="_blank" rel="noopener noreferrer">
                                {shortUrl}
                            </a>
                            <button
                                className="copy-button"
                                onClick={() => {
                                    navigator.clipboard.writeText(shortUrl);
                                    setCopied(true);

                                    setTimeout(() => {
                                        setCopied(false);
                                    }, 3000);
                                }}
                            >
                                <i className={copied ? "fa-solid fa-check" : "fa-regular fa-copy"}></i>
                            </button>

                        </div>

                    </div>
                )}
            </div>
            <div className="footer">
                Made with <span className="heart">❤️</span> by Akki
            </div>

        </>
    );
}

export default Shortener;