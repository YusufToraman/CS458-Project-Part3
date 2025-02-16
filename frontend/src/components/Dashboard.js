import React, { useState, useEffect } from "react";

const Dashboard = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/auth/profile/", {
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setUser(data))
            .catch((error) => console.error("Error fetching user:", error));
    }, []);

    return (
        <div className="dashboard-container">
            <h2>Welcome to Dashboard</h2>
            {user ? (
                <div>
                    <img src={user.profile_picture} alt="Profile" width="50" />
                    <p>Username: {user.username}</p>
                    <p>Email: {user.email}</p>
                </div>
            ) : (
                <p>Loading user data...</p>
            )}
        </div>
    );
};

export default Dashboard;
