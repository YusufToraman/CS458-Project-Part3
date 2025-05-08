import React from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import Login from "./components/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import SurveyPage from "./components/SurveyPage";

function App() {
    console.log("Google Client ID:", process.env.REACT_APP_GOOGLE_CLIENT_ID);

    return (
        <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
            <Router>
                <Routes>
                    <Route path="/" element={<Login />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="*" element={<h1>Not Found</h1>} />
                    <Route path="/surveyPage" element={<SurveyPage />} />
                </Routes>
            </Router>
        </GoogleOAuthProvider>
    );
}

export default App;
