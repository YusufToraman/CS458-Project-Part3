import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"
import CookieUtil from "../util/cookieUtil";

const Dashboard = () => {
    const [user, setUser] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        const user = CookieUtil.getCookie("user");
        if (!user) {
            navigate("/");
        }

        fetch("http://127.0.0.1:8000/auth/profile/", {
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setUser(data))
            .catch((error) => console.error("Error fetching user:", error));
    }, []);

    const handleLogout = () => {
        CookieUtil.removeUser();
        navigate("/");
    };

    return (
        <div className="dashboard-container p-4">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl">Welcome to Dashboard</h2>
                <button 
                    onClick={handleLogout} 
                    className="bg-red-500 text-white px-4 py-2 rounded"
                >
                    Logout
                </button>
            </div>
            
            {user ? (
                <div className="flex items-center gap-4">
                    <img 
                        src={user.profile_picture} 
                        alt="Profile" 
                        width="50" 
                        className="rounded-full"
                    />
                    <div>
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                    </div>
                </div>
            ) : (
                <p>Loading user data...</p>
            )}
        </div>
    );
};

export default Dashboard;
