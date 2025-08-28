import React, { useState, useEffect } from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    LineChart,
    Line,
} from 'recharts';
import {
    FiTrendingUp,
    FiUsers,
    FiHeart,
    FiCalendar,
    FiRefreshCw,
} from 'react-icons/fi';
import { statsAPI } from '../services/Api';
import { SummaryStats } from '../types';
import './Dashboard.css';

const Dashboard: React.FC = () => {
    const [stats, setStats] = useState<SummaryStats | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

    const fetchStats = async () => {
        setIsLoading(true);
        setError('');

        try {
            const data = await statsAPI.getSummaryStats();
            setStats(data);
            setLastUpdated(new Date());
        } catch (err: any) {
            setError('Failed to load statistics. Please try again later.');
            console.error('Error fetching stats:', err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();

        // Auto-refresh every 5 minutes
        const interval = setInterval(fetchStats, 5 * 60 * 1000);
        return () => clearInterval(interval);
    }, []);

    if (isLoading && !stats) {
        return (
            <div className="dashboard-loading">
                <div className="spinner-large"></div>
                <p>Loading statistics...</p>
            </div>
        );
    }

    if (error && !stats) {
        return (
            <div className="dashboard-error">
                <p>{error}</p>
                <button onClick={fetchStats} className="retry-button">
                    <FiRefreshCw />
                    Retry
                </button>
            </div>
        );
    }

    // Prepare data for charts
    const vacationData = stats ? [
        { name: 'Past', value: stats.vacationStats.pastVacations, color: '#8884d8' },
        { name: 'Ongoing', value: stats.vacationStats.ongoingVacations, color: '#82ca9d' },
        { name: 'Future', value: stats.vacationStats.futureVacations, color: '#ffc658' },
    ] : [];

    const topDestinations = stats?.topDestinations.slice(0, 10) || [];

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <div>
                    <h1>Statistics Dashboard</h1>
                    <p className="last-updated">
                        Last updated: {lastUpdated.toLocaleTimeString()}
                    </p>
                </div>
                <button onClick={fetchStats} className="refresh-button" disabled={isLoading}>
                    <FiRefreshCw className={isLoading ? 'spinning' : ''} />
                    {isLoading ? 'Refreshing...' : 'Refresh'}
                </button>
            </div>

            {stats && (
                <>
                    {/* Stats Cards */}
                    <div className="stats-grid">
                        <div className="stat-card">
                            <div className="stat-icon users">
                                <FiUsers />
                            </div>
                            <div className="stat-content">
                                <h3>Total Users</h3>
                                <p className="stat-value">{stats.totalUsers}</p>
                                <span className="stat-label">Registered users</span>
                            </div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-icon likes">
                                <FiHeart />
                            </div>
                            <div className="stat-content">
                                <h3>Total Likes</h3>
                                <p className="stat-value">{stats.totalLikes}</p>
                                <span className="stat-label">Vacation likes</span>
                            </div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-icon vacations">
                                <FiCalendar />
                            </div>
                            <div className="stat-content">
                                <h3>Total Vacations</h3>
                                <p className="stat-value">
                                    {stats.vacationStats.pastVacations +
                                        stats.vacationStats.ongoingVacations +
                                        stats.vacationStats.futureVacations}
                                </p>
                                <span className="stat-label">All vacations</span>
                            </div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-icon trending">
                                <FiTrendingUp />
                            </div>
                            <div className="stat-content">
                                <h3>Most Popular</h3>
                                <p className="stat-value">
                                    {topDestinations[0]?.destination || 'N/A'}
                                </p>
                                <span className="stat-label">
                                    {topDestinations[0]?.likes || 0} likes
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Charts */}
                    <div className="charts-grid">
                        {/* Vacation Status Distribution */}
                        <div className="chart-card">
                            <h3>Vacation Status Distribution</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={vacationData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={(entry: any) => `${entry.name}: ${entry.value}`}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {vacationData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Top Destinations */}
                        <div className="chart-card">
                            <h3>Top 10 Destinations by Likes</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={topDestinations}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis
                                        dataKey="destination"
                                        angle={-45}
                                        textAnchor="end"
                                        height={100}
                                    />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="likes" fill="#82ca9d" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Likes Trend */}
                        <div className="chart-card full-width">
                            <h3>Likes Distribution</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={topDestinations}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="destination" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Line
                                        type="monotone"
                                        dataKey="likes"
                                        stroke="#8884d8"
                                        strokeWidth={2}
                                        dot={{ fill: '#8884d8', r: 6 }}
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Additional Stats */}
                    <div className="additional-stats">
                        <div className="stats-summary">
                            <h3>Summary</h3>
                            <div className="summary-grid">
                                <div className="summary-item">
                                    <span className="summary-label">Past Vacations:</span>
                                    <span className="summary-value">{stats.vacationStats.pastVacations}</span>
                                </div>
                                <div className="summary-item">
                                    <span className="summary-label">Ongoing Vacations:</span>
                                    <span className="summary-value">{stats.vacationStats.ongoingVacations}</span>
                                </div>
                                <div className="summary-item">
                                    <span className="summary-label">Future Vacations:</span>
                                    <span className="summary-value">{stats.vacationStats.futureVacations}</span>
                                </div>
                                <div className="summary-item">
                                    <span className="summary-label">Average Likes per Destination:</span>
                                    <span className="summary-value">
                                        {topDestinations.length > 0
                                            ? Math.round(stats.totalLikes / topDestinations.length)
                                            : 0}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default Dashboard;