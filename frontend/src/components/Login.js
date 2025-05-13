import React, { useEffect, useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import "../styles.css";
import { useNavigate } from "react-router-dom";
import CookieUtil from "../util/cookieUtil";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const user = CookieUtil.getCookie("user");
    if (user) {
      navigate("/dashboard");
    }
  }, []);

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/auth/login/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        storeUser(data.user);
        window.location.href = "/Dashboard";
      } else {
        setError(data.error || "Login failed.");
      }
    } catch (error) {
      setError("Something went wrong.");
    }
  };

  const responseGoogle = (response) => {
    if (!response.credential) {
      setError("Google Login Failed.");
      return;
    }

    const decodedToken = jwtDecode(response.credential);
    console.log("Decoded Google Token:", decodedToken);

    fetch(`${process.env.REACT_APP_API_URL}/auth/google-login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_token: response.credential }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.message) {
          storeUser(data.user);
          window.location.href = "/surveyPage";
        } else {
          setError(data.error || "Google Login Failed.");
        }
      })
      .catch(() => setError("Something went wrong."));
  };

  const storeUser = (data) => {
    CookieUtil.saveUser(data);
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>

      <div className="divider">OR</div>

      <div name="google-login">
        <GoogleLogin
          onSuccess={responseGoogle}
          onError={() => setError("Google Login Failed")}
        />
      </div>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Login;
