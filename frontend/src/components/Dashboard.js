import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import CookieUtil from '../util/cookieUtil';

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const user = CookieUtil.getCookie('user');
        if (!user) {
            navigate('/');
        }

        fetch('http://127.0.0.1:8000/auth/profile/', {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => setUser(data))
            .catch((error) => console.error('Error fetching user:', error));
    }, []);

    const handleLogout = () => {
        CookieUtil.removeUser();
        navigate('/');
    };

    return (
        <div style={{ padding: '32px', backgroundColor: '#f3f4f6', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 style={{ fontSize: '32px', fontWeight: 'bold', marginRight: '16px' }}>Dashboard</h2>
                <button 
                    onClick={handleLogout} 
                    style={{ 
                        backgroundColor: 'red', 
                        color: 'white', 
                        padding: '8px 12px', 
                        borderRadius: '6px', 
                        fontSize: '16px', 
                        transition: 'background-color 0.3s' 
                    }}
                >
                    Logout
                </button>
            </div>


            {user ? (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
                    <div>
                        <p style={{ fontSize: '20px' }}><strong>Username:</strong> {user.username}</p>
                        <p style={{ fontSize: '20px' }}><strong>Email:</strong> {user.email}</p>
                    </div>
                </div>
            ) : (
                <p style={{ color: '#6b7280', fontSize: '20px' }}> Welcome ! </p>
            )}

            <div style={{ marginTop: '32px', display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                <button 
                    onClick={() => navigate('/surveyPage')} 
                    style={{ backgroundColor: '#3b82f6', color: 'white', fontSize: '20px', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', transition: 'background-color 0.3s' }}>
                    Fill Survey Page
                </button>
                <button 
                    onClick={() => navigate('/surveyBuilder')} 
                    style={{ backgroundColor: '#10b981', color: 'white', fontSize: '20px', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', transition: 'background-color 0.3s' }}>
                    Survey Builder
                </button>
                
            </div>
        </div>
    );
};

export default Dashboard;
