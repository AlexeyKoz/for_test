import React from 'react';
import { FiGithub, FiMail, FiLinkedin, FiCode, FiDatabase, FiServer } from 'react-icons/fi';
import { SiReact, SiFlask, SiPostgresql, SiDocker, SiTypescript } from 'react-icons/si';
import './About.css';

const About: React.FC = () => {
    return (
        <div className="about">
            <div className="about-header">
                <h1>About This Project</h1>
                <p className="about-subtitle">
                    Vacation Statistics Dashboard - Part III of the Vacation Management System
                </p>
            </div>

            <div className="about-content">
                <section className="about-section">
                    <h2>Project Overview</h2>
                    <p>
                        This statistics dashboard is the third and final part of a comprehensive
                        vacation management system. It provides administrators with powerful analytics
                        tools to monitor system usage, track user engagement, and analyze vacation
                        trends through an intuitive and visually appealing interface.
                    </p>
                    <p>
                        The project demonstrates full-stack development skills, including backend API
                        development, frontend application design, database integration, and cloud
                        deployment using modern technologies and best practices.
                    </p>
                </section>

                <section className="about-section">
                    <h2>Technology Stack</h2>
                    <div className="tech-grid">
                        <div className="tech-card">
                            <SiReact className="tech-icon react" />
                            <h3>React</h3>
                            <p>Frontend framework with TypeScript for type-safe development</p>
                        </div>
                        <div className="tech-card">
                            <SiFlask className="tech-icon flask" />
                            <h3>Flask</h3>
                            <p>Lightweight Python backend for REST API services</p>
                        </div>
                        <div className="tech-card">
                            <SiPostgresql className="tech-icon postgres" />
                            <h3>PostgreSQL</h3>
                            <p>Robust relational database for data persistence</p>
                        </div>
                        <div className="tech-card">
                            <SiDocker className="tech-icon docker" />
                            <h3>Docker</h3>
                            <p>Containerization for consistent deployment</p>
                        </div>
                        <div className="tech-card">
                            <FiServer className="tech-icon" />
                            <h3>AWS Cloud</h3>
                            <p>Cloud hosting for scalable deployment</p>
                        </div>
                        <div className="tech-card">
                            <SiTypescript className="tech-icon typescript" />
                            <h3>TypeScript</h3>
                            <p>Type-safe JavaScript for better development experience</p>
                        </div>
                    </div>
                </section>

                <section className="about-section">
                    <h2>Features</h2>
                    <div className="features-list">
                        <div className="feature">
                            <FiCode className="feature-icon" />
                            <div>
                                <h4>JWT Authentication</h4>
                                <p>Secure admin-only access with JSON Web Tokens</p>
                            </div>
                        </div>
                        <div className="feature">
                            <FiDatabase className="feature-icon" />
                            <div>
                                <h4>Real-time Statistics</h4>
                                <p>Live data updates from the vacation management system</p>
                            </div>
                        </div>
                        <div className="feature">
                            <FiServer className="feature-icon" />
                            <div>
                                <h4>RESTful API</h4>
                                <p>Clean API architecture with proper endpoint design</p>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="about-section">
                    <h2>Developer Information</h2>
                    <div className="developers-container">
                        <div className="developer-card">
                            <div className="developer-info">
                                <h3>Doron Shalom & Alexey Kozlov</h3>
                                <p className="developer-title">Full Stack Developers</p>
                                <p className="developer-description">
                                    Passionate about creating efficient, scalable web applications
                                    with modern technologies. This project showcases expertise in
                                    both frontend and backend development, database design, and
                                    cloud deployment.
                                </p>
                                <div className="developer-skills">
                                    <span className="skill-tag">Python</span>
                                    <span className="skill-tag">JavaScript</span>
                                    <span className="skill-tag">TypeScript</span>
                                    <span className="skill-tag">React</span>
                                    <span className="skill-tag">Flask</span>
                                    <span className="skill-tag">PostgreSQL</span>
                                    <span className="skill-tag">Docker</span>
                                    <span className="skill-tag">AWS</span>
                                </div>
                            </div>

                            <div className="developers-links">
                                <div className="developer-links-section">
                                    <h4>Doron Shalom</h4>
                                    <div className="developer-links">
                                        <a href="https://github.com/doron1405" target="_blank" rel="noopener noreferrer" className="contact-link">
                                            <FiGithub />
                                            GitHub
                                        </a>
                                        <a href="https://www.linkedin.com/in/doron-shalom-370977233/" target="_blank" rel="noopener noreferrer" className="contact-link">
                                            <FiLinkedin />
                                            LinkedIn
                                        </a>
                                        <a href="mailto:doron1405@gmail.com" className="contact-link">
                                            <FiMail />
                                            Email
                                        </a>
                                    </div>
                                </div>

                                <div className="developer-links-section">
                                    <h4>Alexey Kozlov</h4>
                                    <div className="developer-links">
                                        <a href="https://github.com/AlexeyKoz" target="_blank" rel="noopener noreferrer" className="contact-link">
                                            <FiGithub />
                                            GitHub
                                        </a>
                                        <a href="https://www.linkedin.com/in/alexey-kozlov-full-stack-developer/" target="_blank" rel="noopener noreferrer" className="contact-link">
                                            <FiLinkedin />
                                            LinkedIn
                                        </a>
                                        <a href="mailto:AL7koz@gmail.com" className="contact-link">
                                            <FiMail />
                                            Email
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="about-section">
                    <h2>Project Structure</h2>
                    <div className="structure-info">
                        <p>The complete vacation management system consists of three parts:</p>
                        <ol>
                            <li>
                                <strong>Part I:</strong> Database design and initial setup
                            </li>
                            <li>
                                <strong>Part II:</strong> Main vacation website (Django-based)
                            </li>
                            <li>
                                <strong>Part III:</strong> Statistics dashboard (React + Flask) - This project
                            </li>
                        </ol>
                        <p>
                            All components are containerized using Docker and can be deployed
                            together using Docker Compose for a seamless, integrated system.
                        </p>
                    </div>
                </section>

                <section className="about-section">
                    <h2>Acknowledgments</h2>
                    <p>
                        This project was developed as part of the Python Full Stack Web Developer
                        course at John Bryce Training. Special thanks to our instructor Ophir Gal
                        for his guidance and support throughout the course.
                    </p>
                </section>
            </div>
        </div>
    );
};

export default About;