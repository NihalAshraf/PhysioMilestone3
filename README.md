# PhysioMilestone - Enhanced Physical Therapy Management System

A comprehensive Django-based web application for managing physical therapy exercises and patient-doctor interactions. The system provides real-time exercise validation, progress tracking, and consultation management.

## 🚀 Features

### For Doctors
- **Patient Management**: View all patients with detailed information
- **Exercise Assignment**: Assign exercises with specific reps, sets, and instructions
- **Progress Monitoring**: Real-time tracking of patient progress with charts and analytics
- **Consultation Management**: Handle consultation requests from patients
- **Exercise Library**: Upload and manage exercise templates with video instructions

### For Children/Patients
- **Exercise Instructions**: View assigned exercises with detailed instructions
- **Video Upload**: Upload exercise videos for AI-powered validation
- **Progress Tracking**: Monitor personal progress with detailed reports
- **Doctor Consultation**: Request consultations with available doctors
- **Real-time Feedback**: Get instant feedback on exercise performance

### Core Features
- **AI-Powered Exercise Validation**: Computer vision-based exercise analysis
- **Real-time Progress Tracking**: Comprehensive analytics and reporting
- **Secure User Management**: Role-based access control
- **Responsive Design**: Modern, mobile-friendly interface
- **Video Processing**: Automated exercise validation and scoring

## 🛠️ Technology Stack

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **AI/ML**: OpenCV, MediaPipe, Computer Vision
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local file system (configurable for cloud storage)

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Physiomilestone
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   cd Physiomilestone
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Login with your credentials

## 📁 Project Structure

```
Physiomilestone/
├── Physiomilestone/          # Main Django project
│   ├── Doctor/              # Doctor app
│   │   ├── models.py        # Doctor models (Exercise, AssignExercise, Consultation, PatientProgress)
│   │   ├── views.py         # Doctor views and logic
│   │   ├── urls.py          # Doctor URL patterns
│   │   └── templates/       # Doctor templates
│   ├── Child/               # Child/Patient app
│   │   ├── models.py        # Child models (ExerciseVideo, ExerciseSession)
│   │   ├── views.py         # Child views and logic
│   │   ├── urls.py          # Child URL patterns
│   │   ├── templates/       # Child templates
│   │   └── utils/           # Exercise validation utilities
│   ├── USER/                # User management app
│   │   ├── models.py        # Custom user model
│   │   └── ...
│   └── manage.py            # Django management script
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

### Database Configuration
The project uses SQLite by default. For production, update settings.py to use PostgreSQL or MySQL.

## 👥 User Roles

### Doctor
- Access to patient management
- Exercise assignment capabilities
- Progress monitoring and analytics
- Consultation management

### Child/Patient
- View assigned exercises
- Upload exercise videos
- Track personal progress
- Request doctor consultations

## 🔐 Security Features

- Role-based access control
- CSRF protection
- Secure file uploads
- Input validation and sanitization
- Session management

## 📊 Key Models

### Doctor App
- **Exercise**: Exercise templates with instructions
- **AssignExercise**: Exercise assignments to patients
- **Consultation**: Patient-doctor consultation requests
- **PatientProgress**: Patient progress tracking

### Child App
- **ExerciseVideo**: Uploaded exercise videos with validation results
- **ExerciseSession**: Exercise session tracking

### User App
- **CustomUser**: Extended user model with role-based access

## 🎯 API Endpoints

### Doctor Endpoints
- `GET /Doctor/Dashboard/` - Doctor dashboard
- `GET /Doctor/patients/` - Patient list
- `GET /Doctor/patient/<id>/` - Patient details
- `GET /Doctor/patient/<id>/progress/` - Patient progress
- `GET /Doctor/consultations/` - Consultation list
- `POST /Doctor/consultation/<id>/respond/` - Respond to consultation

### Child Endpoints
- `GET /Child/Dashboard/` - Child dashboard
- `GET /Child/doctors/` - Available doctors
- `POST /Child/consultation/request/<id>/` - Request consultation
- `GET /Child/consultations/` - Consultation history
- `POST /Child/upload-video/` - Upload exercise video

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure media file storage
5. Set up HTTPS
6. Configure logging
7. Set up monitoring

### Docker Deployment
```bash
# Build the image
docker build -t physiomilestone .

# Run the container
docker run -p 8000:8000 physiomilestone
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

### v2.0.0 (Current)
- Enhanced patient monitoring system
- Doctor consultation management
- Real-time progress tracking
- Improved UI/UX
- Comprehensive analytics

### v1.0.0
- Basic exercise management
- Video upload functionality
- User authentication
- Basic progress tracking

## 🙏 Acknowledgments

- Django community for the excellent framework
- OpenCV and MediaPipe for computer vision capabilities
- Tailwind CSS for the beautiful UI components
- All contributors and testers

---

**PhysioMilestone** - Making physical therapy more accessible and effective through technology.