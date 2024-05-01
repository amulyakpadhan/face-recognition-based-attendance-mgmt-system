# Django Attendance Management System with Face Recognition

## Overview
This project is a Django-based attendance management system that uses face recognition to mark attendance. It allows administrators to manage student details, and students can mark their attendance by capturing an image through a webcam and matching it with stored profile pictures.

## Features
- User-friendly interface with light/dark mode support.
- Admin dashboard for managing student details.
- Automated attendance marking using face recognition.
- Display of marked attendance, including student names and enrollment numbers.
- Secure AJAX requests with CSRF protection.

## Prerequisites
- Python 3.x
- Django 3.x or 4.x
- OpenCV for face detection
- DeepFace for face recognition
- Git (for version control)
- Virtual environment tool like `venv` or `virtualenv` (recommended)

## Setup and Installation
Follow these steps to set up and run the project locally:

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/attendance-management-system.git
cd attendance-management-system
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment (Linux/macOS)
# For Windows, use: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt  # Install the required packages
```

### Step 4: Configure Django Settings
Ensure your Django settings are configured properly:

- Set ALLOWED_HOSTS to include your local development domain.
- Configure DATABASES to use a suitable database (e.g., SQLite for development).
- Ensure MEDIA_ROOT and STATIC_ROOT are properly set to handle media files and static files.

### Step 5: Run Migrations
```bash
python manage.py migrate  # Apply database migrations
```

### Step 6: Create a Superuser (Admin Account)
```bash
python manage.py createsuperuser  # Create an admin account
```
### Step 7: Start the Django Server
```bash
python manage.py runserver  # Start the Django development server
```
Now, you can access the project by navigating to http://127.0.0.1:8000/ in your web browser.

## Usage
- Log in as an admin to add student details and manage the system.
- Click the "Mark Attendance" button to open a new window for webcam capture.
- Capture an image to mark attendance.
- If the face is recognized, the attendance is marked, and a success message is displayed.
- View the list of students who have marked attendance, including their names, enrollment numbers, departments, and semesters.

## Contributing
Contributions to this project are welcome! If you'd like to contribute, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or fix.
- Make your changes and commit them with descriptive commit messages.
- Push to your fork and create a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgments
- Django: The web framework used in this project.
- DeepFace: The face recognition library used for matching faces.
- OpenCV: The computer vision library used for face detection.

## 🚀 About Me
I'm Amulya Kumar Padhan, a computer science student specializing in artificial intelligence and web development. This project is a demonstration of my skills and expertise in building web-based applications that incorporate advanced technologies like computer vision and face recognition.
