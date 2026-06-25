CREATE DATABASE IF NOT EXISTS hackotrack_db;
USE hackotrack_db;

CREATE TABLE IF NOT EXISTS hackathon_entries (
    entry_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    linkedin_url VARCHAR(255),
    github_url VARCHAR(255),
    hackathon_name VARCHAR(255) NOT NULL,
    organizing_community VARCHAR(255),
    application_date DATE NOT NULL,
    rough_start_month VARCHAR(50),
    tentative_start_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    location VARCHAR(255),
    tags VARCHAR(255),
    tech_stack VARCHAR(255),
    prize_pool VARCHAR(255),
    team_size VARCHAR(50),
    rules TEXT,
    registration_link VARCHAR(255),
    venue_details TEXT
);
