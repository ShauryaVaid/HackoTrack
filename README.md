# HackoTrack

Find and track hackathons in one place.

## Features
- Search hackathons by name
- Store hackathon details in database
- Simple web interface

## Tech
- FastAPI (backend)
- Streamlit (frontend)
- MySQL (database)

## Getting Started

If you are cloning this project on a new system, follow these steps to get everything running.

### 1. Prerequisites
- **Python 3.8+** installed on your system.
- **MySQL Server** installed and running.

### 2. Install Dependencies
Open your terminal in the project directory and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Since the `.env` file is not tracked in GitHub for security reasons, you need to create one.
Create a file named `.env` in the root directory and add your configurations:
```env
DB_HOST=localhost
DB_USER=root
MYSQL_PWD=your_mysql_password
DB_NAME=hackotrack_db
ADMIN_PASS=your_admin_password
```

### 4. Database Setup
To automatically create the required database and tables, use the provided `setup.sql` file. Run this command in your terminal:
```bash
mysql -u root -p < setup.sql
```
*(Enter your MySQL root password when prompted)*

### 5. Run the Application
Start the FastAPI backend:
```bash
uvicorn main:app --reload
```
Start the Streamlit frontend (in a separate terminal):
```bash
streamlit run streamlit_app.py
```

## LinkedIn
[linkedin.com/in/shaurya-vaid](https://linkedin.com/in/shaurya-vaid)
## GitHub
[[Link]](https://github.com/ShauryaVaid)
