const { useState, useEffect, useRef } = React;

const App = () => {
    const [user, setUser] = useState(null);
    const [authMode, setAuthMode] = useState('signin'); // 'signin' or 'signup'
    const [showAuth, setShowAuth] = useState(true);
    const [showOtpInput, setShowOtpInput] = useState(false);
    const [otpData, setOtpData] = useState({ otp: '', sentTo: null });
    const [authData, setAuthData] = useState({
        username: '',
        email: '',
        phone: '',
        password: ''
    });
    const [formData, setFormData] = useState({
        brand: 'HP',
        processor_speed: '',
        ram_size: '',
        storage_capacity: '',
        screen_size: '',
        weight: ''
    });
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState([]);
    const [error, setError] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [authError, setAuthError] = useState(null);

    // NEW: Dashboard State
    const [viewMode, setViewMode] = useState('history'); // 'history' or 'analytics'
    const brandChartRef = useRef(null);
    const priceChartRef = useRef(null);
    const brandCanvasRef = useRef(null);
    const priceCanvasRef = useRef(null);

    useEffect(() => {
        checkAuth();
        createParticles();
    }, []);

    useEffect(() => {
        if (user) {
            fetchHistory();
        }
    }, [user]);

    // NEW: Initialize Charts when viewMode changes to analytics
    useEffect(() => {
        if (viewMode === 'analytics' && history.length > 0) {
            // Wait for DOM to update
            setTimeout(initCharts, 100);
        }
        return () => {
            destroyCharts();
        };
    }, [viewMode, history]);

    const destroyCharts = () => {
        if (brandChartRef.current) {
            brandChartRef.current.destroy();
            brandChartRef.current = null;
        }
        if (priceChartRef.current) {
            priceChartRef.current.destroy();
            priceChartRef.current = null;
        }
    };

    const initCharts = () => {
        destroyCharts();

        if (!brandCanvasRef.current || !priceCanvasRef.current) return;

        // Process Data for Brand Chart (Pie)
        const brandCounts = {};
        history.forEach(item => {
            brandCounts[item.brand] = (brandCounts[item.brand] || 0) + 1;
        });

        const brandCtx = brandCanvasRef.current.getContext('2d');
        brandChartRef.current = new Chart(brandCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(brandCounts),
                datasets: [{
                    data: Object.values(brandCounts),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(168, 85, 247, 0.8)',
                        'rgba(6, 182, 212, 0.8)',
                        'rgba(244, 63, 94, 0.8)',
                        'rgba(234, 179, 8, 0.8)'
                    ],
                    borderColor: 'rgba(15, 23, 42, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#cbd5e1' }
                    },
                    title: {
                        display: true,
                        text: 'Brands You Scouted',
                        color: '#fff',
                        font: { size: 16 }
                    }
                }
            }
        });

        // Process Data for Price vs RAM Chart (Bar)
        // Group by RAM size and calculate average price
        const ramGroups = {};
        history.forEach(item => {
            if (!ramGroups[item.ram_size]) {
                ramGroups[item.ram_size] = { total: 0, count: 0 };
            }
            ramGroups[item.ram_size].total += item.predicted_price;
            ramGroups[item.ram_size].count += 1;
        });

        const sortedRam = Object.keys(ramGroups).sort((a, b) => Number(a) - Number(b));
        const avgPrices = sortedRam.map(ram => ramGroups[ram].total / ramGroups[ram].count);

        const priceCtx = priceCanvasRef.current.getContext('2d');
        priceChartRef.current = new Chart(priceCtx, {
            type: 'bar',
            data: {
                labels: sortedRam.map(r => `${r}GB`),
                datasets: [{
                    label: 'Avg Price (₹)',
                    data: avgPrices,
                    backgroundColor: 'rgba(99, 102, 241, 0.6)',
                    borderColor: 'rgba(99, 102, 241, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                },
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: 'Price vs RAM Analysis',
                        color: '#fff',
                        font: { size: 16 }
                    }
                }
            }
        });
    };

    const checkAuth = async () => {
        try {
            const res = await fetch('/api/check-auth', {
                credentials: 'include'
            });
            const data = await res.json();
            if (data.authenticated) {
                setUser(data.user);
                setShowAuth(false);
            }
        } catch (err) {
            console.error('Auth check failed', err);
        }
    };

    const createParticles = () => {
        const existing = document.querySelector('.particles');
        if (existing) return;

        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles';
        document.body.appendChild(particlesContainer);

        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.animationDelay = `${Math.random() * 20}s`;
            particle.style.animationDuration = `${15 + Math.random() * 10}s`;
            particlesContainer.appendChild(particle);
        }
    };

    const handleAuthSubmit = async (e) => {
        e.preventDefault();
        setAuthError(null);
        setLoading(true);

        try {
            const endpoint = authMode === 'signin' ? '/api/signin' : '/api/signup';
            const payload = authMode === 'signin'
                ? { username: authData.username, password: authData.password }
                : authData;

            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || 'Authentication failed');
            }

            if (data.requires_otp) {
                setShowOtpInput(true);
                setOtpData({ otp: '', sentTo: data.otp_sent_to });
                setAuthError(null);
            } else {
                setUser(data.user);
                setShowAuth(false);
                setAuthData({ username: '', email: '', phone: '', password: '' });
            }
        } catch (err) {
            setAuthError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleOtpSubmit = async (e) => {
        e.preventDefault();
        setAuthError(null);
        setLoading(true);

        try {
            const res = await fetch('/api/verify-otp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ otp: otpData.otp })
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || 'OTP verification failed');
            }

            setUser(data.user);
            setShowAuth(false);
            setShowOtpInput(false);
            setAuthData({ username: '', email: '', phone: '', password: '' });
            setOtpData({ otp: '', sentTo: null });
        } catch (err) {
            setAuthError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleResendOtp = async () => {
        setAuthError(null);
        setLoading(true);

        try {
            const res = await fetch('/api/resend-otp', {
                method: 'POST',
                credentials: 'include'
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || 'Failed to resend OTP');
            }

            setOtpData({ ...otpData, otp: '' });
            setAuthError('✓ OTP resent successfully!');
        } catch (err) {
            setAuthError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleBackToLogin = () => {
        setShowOtpInput(false);
        setOtpData({ otp: '', sentTo: null });
        setAuthError(null);
    };

    const handleLogout = async () => {
        try {
            await fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            });
            setUser(null);
            setShowAuth(true);
            setHistory([]);
            setPrediction(null);
            setFormData({
                brand: 'HP',
                processor_speed: '',
                ram_size: '',
                storage_capacity: '',
                screen_size: '',
                weight: ''
            });
            setViewMode('history');
        } catch (err) {
            console.error('Logout failed', err);
        }
    };

    const fetchHistory = async () => {
        try {
            const res = await fetch('/history', {
                credentials: 'include'
            });
            const data = await res.json();
            if (res.ok) {
                setHistory(data);
            }
        } catch (err) {
            console.error('Failed to fetch history', err);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

        e.target.style.transform = 'scale(1.02)';
        setTimeout(() => {
            e.target.style.transform = 'scale(1)';
        }, 200);
    };

    const handleAuthChange = (e) => {
        setAuthData({
            ...authData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setPrediction(null);
        setShowResult(false);

        try {
            const res = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(formData)
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || 'Prediction failed');
            }

            setTimeout(() => {
                setPrediction(data.price);
                setShowResult(true);
            }, 500);

            fetchHistory();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const formatPrice = (price) => {
        return new Intl.NumberFormat('en-IN', {
            maximumFractionDigits: 2,
            minimumFractionDigits: 2
        }).format(price);
    };

    if (showAuth) {
        if (showOtpInput) {
            return (
                <div className="auth-container">
                    <div className="auth-card glass-card">
                        <h1>🔐 Enter OTP</h1>
                        <p className="subtitle">
                            We've sent a 6-digit verification code to:
                        </p>
                        <div style={{
                            background: 'rgba(102, 126, 234, 0.1)',
                            padding: '1rem',
                            borderRadius: '8px',
                            margin: '1rem 0',
                            textAlign: 'center'
                        }}>
                            {otpData.sentTo?.email && (
                                <div style={{ marginBottom: '0.5rem' }}>
                                    📧 <strong>{otpData.sentTo.email}</strong>
                                </div>
                            )}
                            {otpData.sentTo?.phone && (
                                <div>
                                    📱 <strong>{otpData.sentTo.phone}</strong>
                                </div>
                            )}
                        </div>

                        <form onSubmit={handleOtpSubmit}>
                            <div className="form-group">
                                <label>🔢 Enter 6-Digit OTP</label>
                                <input
                                    type="text"
                                    name="otp"
                                    value={otpData.otp}
                                    onChange={(e) => setOtpData({ ...otpData, otp: e.target.value })}
                                    placeholder="Enter OTP"
                                    required
                                    maxLength="6"
                                    pattern="[0-9]{6}"
                                    style={{
                                        fontSize: '1.5rem',
                                        textAlign: 'center',
                                        letterSpacing: '0.5rem'
                                    }}
                                />
                            </div>

                            <button type="submit" className="btn-primary" disabled={loading}>
                                {loading ? '⏳ Verifying...' : '✓ Verify OTP'}
                            </button>

                            <div style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                marginTop: '1rem',
                                gap: '1rem'
                            }}>
                                <button
                                    type="button"
                                    onClick={handleResendOtp}
                                    disabled={loading}
                                    style={{
                                        flex: 1,
                                        padding: '0.75rem',
                                        background: 'transparent',
                                        border: '2px solid #667eea',
                                        borderRadius: '12px',
                                        color: '#667eea',
                                        cursor: 'pointer',
                                        fontWeight: '600',
                                        transition: 'all 0.3s'
                                    }}
                                >
                                    🔄 Resend OTP
                                </button>
                                <button
                                    type="button"
                                    onClick={handleBackToLogin}
                                    style={{
                                        flex: 1,
                                        padding: '0.75rem',
                                        background: 'transparent',
                                        border: '2px solid #94a3b8',
                                        borderRadius: '12px',
                                        color: '#94a3b8',
                                        cursor: 'pointer',
                                        fontWeight: '600',
                                        transition: 'all 0.3s'
                                    }}
                                >
                                    ← Back to Login
                                </button>
                            </div>

                            {authError && (
                                <div style={{
                                    color: authError.includes('✓') ? '#10b981' : '#ef4444',
                                    marginTop: '1rem',
                                    padding: '1rem',
                                    background: authError.includes('✓') ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                    border: authError.includes('✓') ? '2px solid rgba(16, 185, 129, 0.3)' : '2px solid rgba(239, 68, 68, 0.3)',
                                    borderRadius: '12px',
                                    fontWeight: '600'
                                }}>
                                    {authError}
                                </div>
                            )}
                        </form>

                        <div style={{
                            marginTop: '1.5rem',
                            padding: '1rem',
                            background: 'rgba(148, 163, 184, 0.1)',
                            borderRadius: '8px',
                            fontSize: '0.85rem',
                            color: '#64748b'
                        }}>
                            💡 <strong>Tip:</strong> Check your email inbox (and spam folder) for the OTP code. The code expires in 10 minutes.
                        </div>
                    </div>
                </div>
            );
        }

        return (
            <div className="auth-container">
                <div className="auth-card glass-card">
                    <h1>💻 Laptop Price Predictor</h1>
                    <p className="subtitle">
                        {authMode === 'signin' ? 'Welcome back! Sign in to continue' : 'Create your account to get started'}
                    </p>

                    <div className="auth-tabs">
                        <button
                            className={`auth-tab ${authMode === 'signin' ? 'active' : ''}`}
                            onClick={() => {
                                setAuthMode('signin');
                                setAuthError(null);
                            }}
                        >
                            Sign In
                        </button>
                        <button
                            className={`auth-tab ${authMode === 'signup' ? 'active' : ''}`}
                            onClick={() => {
                                setAuthMode('signup');
                                setAuthError(null);
                            }}
                        >
                            Sign Up
                        </button>
                    </div>

                    <form onSubmit={handleAuthSubmit}>
                        <div className="form-group">
                            <label>👤 Username</label>
                            <input
                                type="text"
                                name="username"
                                value={authData.username}
                                onChange={handleAuthChange}
                                placeholder="Enter your username"
                                required
                            />
                        </div>

                        {authMode === 'signup' && (
                            <>
                                <div className="form-group">
                                    <label>📧 Email</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={authData.email}
                                        onChange={handleAuthChange}
                                        placeholder="Enter your email"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>📱 Phone Number (Optional)</label>
                                    <input
                                        type="tel"
                                        name="phone"
                                        value={authData.phone}
                                        onChange={handleAuthChange}
                                        placeholder="+1234567890 (optional for SMS OTP)"
                                    />
                                </div>
                            </>
                        )}

                        <div className="form-group">
                            <label>🔒 Password</label>
                            <input
                                type="password"
                                name="password"
                                value={authData.password}
                                onChange={handleAuthChange}
                                placeholder="Enter your password"
                                required
                                minLength="6"
                            />
                        </div>

                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? '⏳ Please wait...' : authMode === 'signin' ? '🚀 Sign In' : '✨ Create Account'}
                        </button>

                        {authError && (
                            <div style={{
                                color: '#ef4444',
                                marginTop: '1rem',
                                padding: '1rem',
                                background: 'rgba(239, 68, 68, 0.1)',
                                border: '2px solid rgba(239, 68, 68, 0.3)',
                                borderRadius: '12px',
                                fontWeight: '600'
                            }}>
                                ⚠️ {authError}
                            </div>
                        )}
                    </form>
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="user-header">
                <div className="user-info">
                    <span className="user-welcome">👋 Welcome, <strong>{user?.username}</strong>!</span>
                    <span className="user-email">{user?.email}</span>
                </div>
                <button className="btn-logout" onClick={handleLogout}>
                    🚪 Logout
                </button>
            </div>

            <div className="app-container">
                <div className="glass-card">
                    <h1>💻 Laptop Price Predictor</h1>
                    <p className="subtitle">Enter specifications to get an instant AI-powered valuation</p>

                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>🏷️ Brand</label>
                            <select
                                name="brand"
                                value={formData.brand}
                                onChange={handleChange}
                                required
                            >
                                <option value="HP">HP</option>
                                <option value="Asus">Asus</option>
                                <option value="Acer">Acer</option>
                                <option value="Lenovo">Lenovo</option>
                                <option value="Dell">Dell</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>⚡ Processor Speed (GHz)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="processor_speed"
                                value={formData.processor_speed}
                                onChange={handleChange}
                                placeholder="e.g. 2.5"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>🧠 RAM Size (GB)</label>
                            <input
                                type="number"
                                name="ram_size"
                                value={formData.ram_size}
                                onChange={handleChange}
                                placeholder="e.g. 8"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>💾 Storage Capacity (GB)</label>
                            <input
                                type="number"
                                name="storage_capacity"
                                value={formData.storage_capacity}
                                onChange={handleChange}
                                placeholder="e.g. 512"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>📺 Screen Size (Inches)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="screen_size"
                                value={formData.screen_size}
                                onChange={handleChange}
                                placeholder="e.g. 15.6"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>⚖️ Weight (kg)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="weight"
                                value={formData.weight}
                                onChange={handleChange}
                                placeholder="e.g. 1.8"
                                required
                            />
                        </div>

                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? '🔮 Calculating Magic...' : '🚀 Predict Price'}
                        </button>

                        {error && (
                            <div style={{
                                color: '#ef4444',
                                marginTop: '1rem',
                                padding: '1rem',
                                background: 'rgba(239, 68, 68, 0.1)',
                                border: '2px solid rgba(239, 68, 68, 0.3)',
                                borderRadius: '12px',
                                fontWeight: '600'
                            }}>
                                ⚠️ {error}
                            </div>
                        )}
                    </form>

                    {showResult && prediction !== null && (
                        <div className="result-section">
                            <p style={{ color: '#94a3b8' }}>✨ Estimated Value ✨</p>
                            <div className="price-tag">
                                <span className="currency">₹</span>
                                {formatPrice(prediction)}
                            </div>
                            <p style={{
                                fontSize: '0.9rem',
                                color: 'var(--text-secondary)',
                                marginTop: '1rem'
                            }}>
                                🎯 AI-Powered Prediction
                            </p>
                        </div>
                    )}
                </div>

                <div className="glass-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                        <div className="auth-tabs" style={{ marginBottom: 0, width: '100%' }}>
                            <button
                                className={`auth-tab ${viewMode === 'history' ? 'active' : ''}`}
                                onClick={() => setViewMode('history')}
                            >
                                📜 History
                            </button>
                            <button
                                className={`auth-tab ${viewMode === 'analytics' ? 'active' : ''}`}
                                onClick={() => setViewMode('analytics')}
                            >
                                📊 Analytics
                            </button>
                        </div>
                    </div>

                    {viewMode === 'history' ? (
                        <div className="history-list">
                            {history.length === 0 ? (
                                <p style={{
                                    color: '#94a3b8',
                                    textAlign: 'center',
                                    marginTop: '2rem',
                                    fontSize: '1.1rem'
                                }}>
                                    🔍 No history yet - Make your first prediction!
                                </p>
                            ) : (
                                history.slice(0, 10).map((item, index) => (
                                    <div
                                        key={item.id}
                                        className="history-item"
                                        style={{
                                            animationDelay: `${index * 0.1}s`,
                                            animation: 'resultAppear 0.5s ease-out forwards',
                                            opacity: 0
                                        }}
                                    >
                                        <div className="history-details">
                                            <span className="history-brand">
                                                {item.brand === 'HP' && '🖥️'}
                                                {item.brand === 'Asus' && '💻'}
                                                {item.brand === 'Acer' && '🎮'}
                                                {item.brand === 'Lenovo' && '⚡'}
                                                {item.brand === 'Dell' && '🚀'}
                                                {' '}{item.brand}
                                            </span>
                                            <span className="history-specs">
                                                🧠 {item.ram_size}GB RAM • 💾 {item.storage_capacity}GB • ⚡ {item.processor_speed}GHz
                                            </span>
                                        </div>
                                        <span className="history-price">
                                            ₹{formatPrice(item.predicted_price)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    ) : (
                        <div className="analytics-container" style={{ animation: 'fadeIn 0.5s ease-out' }}>
                            {history.length === 0 ? (
                                <p style={{
                                    color: '#94a3b8',
                                    textAlign: 'center',
                                    marginTop: '2rem',
                                    fontSize: '1.1rem'
                                }}>
                                    📊 Not enough data for analytics. Make some predictions first!
                                </p>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                                    <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '16px' }}>
                                        <canvas ref={brandCanvasRef}></canvas>
                                    </div>
                                    <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '16px' }}>
                                        <canvas ref={priceCanvasRef}></canvas>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
