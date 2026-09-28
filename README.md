# Job Application Tracker

A web-based Job Application Tracker built with **Python, Flask, SQLite, HTML, and CSS** to help users organize and manage their job applications from a single dashboard.

## Screenshots

### Dashboard
![Dashboard](C:\Users\Akash Gowda\Pictures.png)

### Application Details
![Application Details](C:\Users\Akash Gowda\Pictures\WPS PNG Picture file.png)

## Features

* Add new job applications
* View all applications from a dashboard
* View detailed information for an individual application
* Edit existing application details
* Delete applications
* Track application status
* Store application data using SQLite
* Clean and simple web interface
* Form-based application management

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS
* **Templating:** Jinja2
* **Development Environment:** Visual Studio Code
* **Version Control:** Git / GitHub

## Project Structure

```text
Job Application Tracker/
│
├── templates/
│   ├── add_applications.html
│   ├── application_details.html
│   ├── edit_application.html
│   └── index.html
│
│
├── app.py
├── init_db.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The SQLite database and virtual environment are kept local and are excluded from GitHub through `.gitignore`.

## How It Works

The application follows a simple CRUD workflow:

**Create → Read → Update → Delete**

### 1. Create

Users can add a new job application through the **Add Application** form.

### 2. Read

The dashboard displays saved job applications, and users can open an individual application to view its details.

### 3. Update

Users can edit an existing application and save the updated information.

### 4. Delete

Users can delete an application from the application details page.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/AkashGowda-R/Job-Application-Tracker.git
cd Job-Application-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize the database

```bash
python init_db.py
```

### 6. Run the Flask application

```bash
python app.py
```

Then open the local address shown in the terminal in your browser.

## What I Learned

Through this project, I practiced:

* Building a web application with Flask
* Creating Flask routes
* Working with HTML forms
* Using Jinja2 templates
* Connecting Python applications to SQLite
* Performing CRUD operations
* Handling form submissions
* Organizing a Flask project
* Managing Python dependencies with `requirements.txt`
* Using Git and GitHub for version control

## Future Improvements

Possible future enhancements include:

* Search and filter applications
* Application status statistics
* Sorting applications by date or status
* User authentication
* Responsive design improvements
* Deployment to a cloud platform
* Automated reminders for application follow-ups

## Project Purpose

This project was built as a practical portfolio project to demonstrate hands-on experience with **Python, Flask, SQLite, HTML, CSS, CRUD operations, and Git/GitHub**.
