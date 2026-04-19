-- ============================================================
-- Cricbuzz LiveStats - MySQL Database Schema
-- Run this file once to set up all tables and sample data
-- ============================================================

CREATE DATABASE IF NOT EXISTS cricbuzz_db;
USE cricbuzz_db;

-- ------------------------------------------------------------
-- TEAMS TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    team_type ENUM('International', 'Domestic', 'Franchise') DEFAULT 'International',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- PLAYERS TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    team_id INT,
    playing_role ENUM('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper') NOT NULL,
    batting_style VARCHAR(50),
    bowling_style VARCHAR(100),
    date_of_birth DATE,
    nationality VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- VENUES TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- SERIES TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100),
    match_type ENUM('Test', 'ODI', 'T20I', 'Mixed') DEFAULT 'ODI',
    start_date DATE,
    end_date DATE,
    total_matches INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- MATCHES TABLE
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    series_id INT,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    venue_id INT,
    match_date DATE,
    match_format ENUM('Test', 'ODI', 'T20I') NOT NULL,
    match_description VARCHAR(255),
    toss_winner_id INT,
    toss_decision ENUM('bat', 'bowl'),
    winning_team_id INT,
    victory_margin INT,
    victory_type ENUM('runs', 'wickets', 'draw', 'tie', 'no result'),
    match_status ENUM('upcoming', 'live', 'completed') DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(series_id) ON DELETE SET NULL,
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL,
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (winning_team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- PLAYER STATS TABLE (per format career stats)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS player_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    format ENUM('Test', 'ODI', 'T20I') NOT NULL,
    matches_played INT DEFAULT 0,
    innings INT DEFAULT 0,
    runs_scored INT DEFAULT 0,
    highest_score INT DEFAULT 0,
    batting_average DECIMAL(6,2) DEFAULT 0.00,
    strike_rate DECIMAL(6,2) DEFAULT 0.00,
    centuries INT DEFAULT 0,
    half_centuries INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    bowling_average DECIMAL(6,2) DEFAULT 0.00,
    economy_rate DECIMAL(5,2) DEFAULT 0.00,
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    UNIQUE KEY unique_player_format (player_id, format)
);

-- ------------------------------------------------------------
-- BATTING PERFORMANCES TABLE (per match)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS batting_performances (
    perf_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    innings_number TINYINT DEFAULT 1,
    batting_position TINYINT,
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate DECIMAL(6,2) DEFAULT 0.00,
    dismissal_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- BOWLING PERFORMANCES TABLE (per match)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bowling_performances (
    perf_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    innings_number TINYINT DEFAULT 1,
    overs_bowled DECIMAL(4,1) DEFAULT 0.0,
    maidens INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    wickets INT DEFAULT 0,
    economy_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- Teams
INSERT INTO teams (team_name, country, team_type) VALUES
('India', 'India', 'International'),
('Australia', 'Australia', 'International'),
('England', 'England', 'International'),
('Pakistan', 'Pakistan', 'International'),
('South Africa', 'South Africa', 'International'),
('New Zealand', 'New Zealand', 'International'),
('West Indies', 'West Indies', 'International'),
('Sri Lanka', 'Sri Lanka', 'International'),
('Bangladesh', 'Bangladesh', 'International'),
('Afghanistan', 'Afghanistan', 'International');

-- Venues
INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Lords Cricket Ground', 'London', 'England', 30000),
('Eden Gardens', 'Kolkata', 'India', 68000),
('Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
('Wankhede Stadium', 'Mumbai', 'India', 33108),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
('Newlands Cricket Ground', 'Cape Town', 'South Africa', 25000),
('Sharjah Cricket Stadium', 'Sharjah', 'UAE', 16000),
('MA Chidambaram Stadium', 'Chennai', 'India', 50000);

-- Players
INSERT INTO players (full_name, team_id, playing_role, batting_style, bowling_style, date_of_birth, nationality) VALUES
('Virat Kohli', 1, 'Batsman', 'Right-hand bat', 'Right-arm medium', '1988-11-05', 'Indian'),
('Rohit Sharma', 1, 'Batsman', 'Right-hand bat', 'Right-arm off-break', '1987-04-30', 'Indian'),
('Jasprit Bumrah', 1, 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-12-06', 'Indian'),
('Ravindra Jadeja', 1, 'All-rounder', 'Left-hand bat', 'Left-arm orthodox', '1988-12-06', 'Indian'),
('KL Rahul', 1, 'Wicket-keeper', 'Right-hand bat', 'Right-arm medium', '1992-04-18', 'Indian'),
('Steve Smith', 2, 'Batsman', 'Right-hand bat', 'Right-arm leg-break', '1989-06-02', 'Australian'),
('Pat Cummins', 2, 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-05-08', 'Australian'),
('David Warner', 2, 'Batsman', 'Left-hand bat', 'Right-arm leg-break', '1986-10-27', 'Australian'),
('Mitchell Starc', 2, 'Bowler', 'Left-hand bat', 'Left-arm fast', '1990-01-30', 'Australian'),
('Glenn Maxwell', 2, 'All-rounder', 'Right-hand bat', 'Right-arm off-break', '1988-10-14', 'Australian'),
('Joe Root', 3, 'Batsman', 'Right-hand bat', 'Right-arm off-break', '1990-12-30', 'English'),
('Ben Stokes', 3, 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', '1991-06-04', 'English'),
('James Anderson', 3, 'Bowler', 'Right-hand bat', 'Right-arm swing', '1982-07-30', 'English'),
('Babar Azam', 4, 'Batsman', 'Right-hand bat', 'Right-arm medium', '1994-10-15', 'Pakistani'),
('Shaheen Afridi', 4, 'Bowler', 'Left-hand bat', 'Left-arm fast', '2000-04-06', 'Pakistani'),
('Shreyas Iyer', 1, 'Batsman', 'Right-hand bat', 'Right-arm leg-break', '1994-12-06', 'Indian'),
('Hardik Pandya', 1, 'All-rounder', 'Right-hand bat', 'Right-arm fast-medium', '1993-10-11', 'Indian'),
('Rishabh Pant', 1, 'Wicket-keeper', 'Left-hand bat', 'Right-arm medium', '1997-10-04', 'Indian'),
('Mohammed Shami', 1, 'Bowler', 'Right-hand bat', 'Right-arm fast-medium', '1990-09-03', 'Indian'),
('Suryakumar Yadav', 1, 'Batsman', 'Right-hand bat', 'Right-arm medium', '1990-09-14', 'Indian');

-- Series
INSERT INTO series (series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
('ICC Cricket World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
('Border-Gavaskar Trophy 2024-25', 'Australia', 'Test', '2024-11-22', '2025-01-07', 5),
('India vs England T20I Series 2024', 'India', 'T20I', '2024-01-27', '2024-02-04', 5),
('ICC T20 World Cup 2024', 'USA', 'T20I', '2024-06-01', '2024-06-29', 55),
('Ashes 2023', 'England', 'Test', '2023-06-16', '2023-07-31', 5);

-- Matches
INSERT INTO matches (series_id, team1_id, team2_id, venue_id, match_date, match_format, match_description, toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type, match_status) VALUES
(1, 1, 2, 1, '2023-10-08', 'ODI', 'IND vs AUS - CWC 2023 Match 5', 1, 'bat', 1, 6, 'wickets', 'completed'),
(1, 1, 4, 4, '2023-10-14', 'ODI', 'IND vs PAK - CWC 2023 Match 12', 4, 'bowl', 1, 7, 'wickets', 'completed'),
(1, 2, 3, 10, '2023-10-20', 'ODI', 'AUS vs ENG - CWC 2023', 3, 'bat', 2, 33, 'runs', 'completed'),
(2, 2, 1, 5, '2024-11-22', 'Test', 'AUS vs IND - BGT 1st Test', 2, 'bat', 1, 295, 'runs', 'completed'),
(2, 2, 1, 2, '2024-12-06', 'Test', 'AUS vs IND - BGT 2nd Test', 1, 'bat', 2, 10, 'wickets', 'completed'),
(4, 1, 2, 9, '2024-06-24', 'T20I', 'IND vs AUS - T20 WC SF', 1, 'bat', 1, 24, 'runs', 'completed'),
(4, 1, 3, 9, '2024-06-29', 'T20I', 'IND vs SA - T20 WC Final', 2, 'bowl', 1, 7, 'runs', 'completed'),
(3, 1, 3, 6, '2024-01-27', 'T20I', 'IND vs ENG - 1st T20I', 3, 'bat', 3, 8, 'runs', 'completed'),
(3, 1, 3, 10, '2024-02-01', 'T20I', 'IND vs ENG - 3rd T20I', 1, 'bat', 1, 6, 'wickets', 'completed'),
(1, 1, 5, 1, '2023-11-05', 'ODI', 'IND vs SA - CWC 2023 SF', 1, 'bat', 1, 212, 'runs', 'completed');

-- Player Stats (Career stats per format)
INSERT INTO player_stats (player_id, format, matches_played, innings, runs_scored, highest_score, batting_average, strike_rate, centuries, half_centuries, wickets_taken, bowling_average, economy_rate, catches, stumpings) VALUES
(1, 'ODI', 295, 289, 13906, 183, 58.18, 93.25, 50, 72, 4, 166.00, 5.78, 129, 0),
(1, 'Test', 113, 192, 8848, 254, 48.62, 55.40, 29, 30, 0, 0.00, 0.00, 84, 0),
(1, 'T20I', 125, 117, 4188, 122, 51.95, 137.97, 1, 38, 0, 0.00, 0.00, 55, 0),
(2, 'ODI', 264, 258, 10709, 264, 48.66, 89.19, 31, 55, 8, 87.75, 5.63, 133, 0),
(2, 'Test', 67, 109, 3962, 212, 40.43, 57.80, 12, 18, 1, 78.00, 3.00, 29, 0),
(2, 'T20I', 159, 154, 4231, 121, 32.05, 140.89, 5, 32, 0, 0.00, 0.00, 63, 0),
(3, 'ODI', 89, 25, 67, 10, 6.70, 74.44, 0, 0, 158, 23.53, 4.45, 25, 0),
(3, 'Test', 38, 54, 357, 55, 9.12, 58.52, 0, 1, 162, 18.89, 2.74, 11, 0),
(3, 'T20I', 85, 20, 44, 10, 7.33, 120.00, 0, 0, 88, 18.01, 6.27, 18, 0),
(4, 'ODI', 194, 156, 2531, 87, 27.50, 83.00, 0, 14, 220, 36.61, 4.96, 120, 0),
(4, 'Test', 74, 106, 3113, 175, 37.05, 47.71, 3, 19, 262, 24.52, 2.68, 72, 0),
(4, 'T20I', 74, 42, 540, 46, 22.50, 116.09, 0, 1, 54, 29.00, 7.81, 45, 0),
(6, 'Test', 110, 193, 9305, 239, 57.17, 55.49, 32, 36, 17, 92.06, 2.97, 126, 0),
(6, 'ODI', 156, 148, 6068, 164, 44.69, 87.88, 12, 42, 0, 0.00, 0.00, 81, 0),
(11, 'Test', 142, 252, 12228, 254, 52.94, 55.71, 35, 62, 46, 145.24, 3.82, 180, 0),
(11, 'ODI', 175, 170, 7296, 133, 50.32, 88.79, 22, 40, 18, 67.94, 4.86, 71, 0),
(14, 'ODI', 107, 105, 5571, 158, 57.43, 88.03, 20, 30, 0, 0.00, 0.00, 54, 0),
(14, 'T20I', 112, 110, 3986, 122, 43.33, 128.82, 3, 33, 0, 0.00, 0.00, 37, 0),
(12, 'Test', 102, 170, 6170, 258, 38.93, 56.05, 13, 33, 190, 30.49, 3.10, 115, 0),
(12, 'ODI', 105, 92, 3122, 128, 43.36, 95.23, 3, 21, 74, 41.05, 5.61, 52, 0),
(17, 'ODI', 76, 66, 1567, 92, 31.34, 117.13, 0, 12, 61, 41.52, 5.73, 44, 0),
(17, 'T20I', 85, 64, 1207, 76, 26.67, 147.48, 0, 8, 54, 34.02, 8.99, 28, 0),
(20, 'T20I', 71, 66, 2364, 117, 47.28, 173.43, 2, 16, 0, 0.00, 0.00, 26, 0);

-- Batting Performances (sample per match)
INSERT INTO batting_performances (match_id, player_id, innings_number, batting_position, runs, balls_faced, fours, sixes, strike_rate, dismissal_type) VALUES
(1, 1, 1, 3, 85, 78, 9, 2, 108.97, 'caught'),
(1, 2, 1, 1, 47, 42, 5, 1, 111.90, 'caught'),
(2, 1, 1, 3, 122, 132, 12, 1, 92.42, 'not out'),
(3, 6, 1, 4, 69, 71, 7, 1, 97.18, 'bowled'),
(4, 6, 1, 4, 141, 214, 15, 3, 65.89, 'caught'),
(5, 1, 1, 3, 36, 57, 4, 0, 63.16, 'lbw'),
(6, 20, 1, 4, 76, 45, 7, 4, 168.89, 'caught'),
(7, 1, 1, 3, 76, 48, 6, 2, 158.33, 'not out'),
(7, 20, 1, 4, 45, 28, 3, 3, 160.71, 'bowled'),
(8, 11, 1, 4, 12, 18, 1, 0, 66.67, 'caught'),
(9, 1, 1, 3, 59, 40, 5, 2, 147.50, 'caught'),
(10, 2, 1, 1, 131, 124, 14, 1, 105.65, 'not out');

-- Bowling Performances
INSERT INTO bowling_performances (match_id, player_id, innings_number, overs_bowled, maidens, runs_conceded, wickets, economy_rate) VALUES
(1, 3, 2, 10.0, 1, 34, 2, 3.40),
(2, 3, 2, 10.0, 2, 28, 3, 2.80),
(3, 7, 1, 10.0, 0, 51, 2, 5.10),
(4, 3, 2, 24.0, 8, 56, 5, 2.33),
(5, 7, 1, 26.0, 5, 89, 4, 3.42),
(6, 3, 2, 4.0, 0, 18, 2, 4.50),
(7, 3, 1, 4.0, 1, 15, 2, 3.75),
(9, 3, 2, 4.0, 0, 21, 1, 5.25),
(10, 19, 2, 10.0, 0, 43, 2, 4.30);

-- Indexes for performance
CREATE INDEX idx_player_team ON players(team_id);
CREATE INDEX idx_match_date ON matches(match_date);
CREATE INDEX idx_match_format ON matches(match_format);
CREATE INDEX idx_stats_player ON player_stats(player_id);
CREATE INDEX idx_batting_match ON batting_performances(match_id);
CREATE INDEX idx_bowling_match ON bowling_performances(match_id);

SELECT 'Database setup complete!' AS Status;
