# AIMINI - Hospital Management System

AIMINI is a Hospital Management System built using **Python**, **Flask**, and **MySQL**. This project helps manage patients, doctors, appointments, and hospital records efficiently.

---

## 🛠 Requirements / Installations

Before running the project, make sure you have the following installed:

1. **Python 3.11**  
   Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **MySQL Server**  
   Download: [https://dev.mysql.com/downloads/](https://dev.mysql.com/downloads/)  
   - Create a database named `aimini`  
   - Import tables if SQL script provided.

3. **pip** (comes with Python)

---

## ⚡ Project Setup

1. **Clone the repository**
```bash
git clone https://github.com/pratapdabhade13/AIMINI---Hospital-Management-System.git
cd AIMINI---Hospital-Management-System

Create a virtual environment

python -m venv venv

Activate the virtual environment

Windows (Command Prompt):

venv\Scripts\activate

Windows (PowerShell):

venv\Scripts\Activate.ps1

Mac / Linux:

source venv/bin/activate

Install required Python packages

pip install -r requirements.txt

⚠️ Note: If requirements.txt does not exist, install manually:

pip install flask mysql-connector-python werkzeug
⚙️ Database Setup

Open MySQL Workbench or command line.

Create database:

CREATE DATABASE aimini;

Import table structure if SQL script is provided:

USE aimini;
SOURCE database.sql;  -- if database.sql exists

Update database credentials in your project (config.py or wherever database connection is set):

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "aimini"
🚀 Running the Project

Make sure virtual environment is active.

Run Flask application:

python app.py

Open your browser and go to:

http://127.0.0.1:5000

You should see the AIMINI Hospital Management System running.

🔧 Optional Commands

Deactivate virtual environment:

deactivate

Upgrade pip (if needed):

python -m pip install --upgrade pip
⚠️ Important Notes

Do not upload venv/ folder to GitHub. Add venv/ to .gitignore.

Always activate virtual environment before running the project.

Ensure MySQL server is running before starting the app.
