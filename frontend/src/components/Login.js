import React, { useState } from "react";
import "../styles.css";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (event) => {
        event.preventDefault();
        setError("");

        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/login/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login successful!");
                window.location.href = "/dashboard";
            } else {
                setError(data.error || "Login failed.");
            }
        } catch (error) {
            setError("Something went wrong.");
        }
    };

    const handleGoogleLogin = () => {
        window.location.href = `${process.env.REACT_APP_API_URL}/accounts/google/login/`;
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <button type="submit">Login</button>
            </form>

            <div className="divider">OR</div>

            <button className="google-btn" onClick={handleGoogleLogin}>
                Login with Google
            </button>

            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

export default Login;
