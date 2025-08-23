# Exercise Validation System for PhysioMilestones

## Overview

This system provides automated exercise validation for children's physiotherapy sessions using computer vision and pose estimation. The system can detect and count repetitions for various exercises including arm raises, squats, and jumping jacks.

## Features

### 🎯 Exercise Detection
- **Arm Raises**: Tracks shoulder-elbow-wrist angles
- **Squats**: Monitors hip-knee-ankle angles  
- **Jumping Jacks**: Analyzes both arm and leg positioning
- **Extensible**: Easy to add new exercise types

### 📊 Performance Metrics
- **Repetition Counting**: Accurate rep detection with confidence scoring
- **Set Tracking**: Automatic set calculation based on rep thresholds
- **Accuracy Scoring**: Overall performance score combining multiple factors
- **Progress Tracking**: Historical data and improvement trends

### 🎨 User Interface
- **Modal Upload**: Clean popup interface for video upload
- **Real-time Processing**: Live status updates during video analysis
- **Results Display**: Comprehensive results with visual feedback
- **Progress Dashboard**: Overview of recent exercises and performance

## Technical Architecture

### Core Components

#### 1. Exercise Validator (`utils/exercise_validator.py`)
```python
class ExerciseValidator:
    - process_video(video_path, exercise_type)
    - detect_arm_raise(results)
    - detect_squat(results)
    - detect_jumping_jack(results)
    - count_repetitions(exercise_type, detection_results)
```

#### 2. Models (`models.py`)
- **ExerciseVideo**: Stores video files and analysis results
- **ExerciseSession**: Tracks exercise sessions and progress

#### 3. Views (`views.py`)
- **VideoUploadView**: Handles video upload and processing
- **VideoStatusView**: Provides processing status updates
- **ExerciseResultsView**: Displays detailed results

#### 4. Templates
- **Exercise_Instructions.html**: Updated with upload modal
- **Exercise_Results.html**: Detailed results display
- **Dashboard.html**: Enhanced with recent videos

## Installation & Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Dependencies
- Django 5.2.5
- OpenCV 4.8.1.78
- MediaPipe 0.10.7
- NumPy 1.24.3
- Django REST Framework 3.16.1

### Database Migration
```bash
python manage.py makemigrations Child
python manage.py migrate
```

## Usage

### 1. Exercise Assignment
Doctors assign exercises through the admin interface with:
- Exercise type and description
- Target repetitions and sets
- Instructions and video references

### 2. Video Upload Process
1. Child clicks "Let's Begin!" on exercise instructions
2. Upload modal appears with file selection
3. Video is uploaded and processed asynchronously
4. Real-time status updates are shown
5. Results are displayed upon completion

### 3. Analysis Results
The system provides:
- **Overall Score**: Combined accuracy metric
- **Repetition Accuracy**: Completed vs target reps
- **Set Accuracy**: Completed vs target sets  
- **Pose Accuracy**: Form correctness score
- **Detailed Feedback**: Specific improvement suggestions

## Exercise Detection Logic

### Arm Raises
```python
# Angle calculation: shoulder-elbow-wrist
angle_threshold = 160°  # Arms raised position
min_angle = 60°         # Arms down position
max_angle = 180°        # Maximum range
```

### Squats
```python
# Angle calculation: hip-knee-ankle  
angle_threshold = 120°  # Squat position
min_angle = 60°         # Deep squat
max_angle = 180°        # Standing position
```

### Jumping Jacks
```python
# Dual angle tracking
arm_angle_threshold = 150°   # Arms up
leg_angle_threshold = 160°   # Legs spread
```

## Configuration

### Exercise Types
Add new exercises in `exercise_validator.py`:
```python
self.exercise_configs = {
    'new_exercise': {
        'angle_threshold': 140,
        'min_angle': 60,
        'max_angle': 180,
        'landmarks': ['shoulder', 'elbow', 'wrist'],
        'rep_threshold': 0.8
    }
}
```

### Detection Parameters
- **Confidence Thresholds**: Adjust for sensitivity
- **Angle Thresholds**: Modify for different exercise variations
- **Frame Processing**: Control processing speed vs accuracy

## API Endpoints

### Video Upload
```
POST /Child/upload-video/
Content-Type: multipart/form-data
Body: video file
Response: {success: true, video_id: 123}
```

### Status Check
```
GET /Child/video-status/<video_id>/
Response: {status: "completed", results: {...}}
```

### Results View
```
GET /Child/exercise-results/<video_id>/
Response: HTML page with detailed results
```

## Performance Considerations

### Video Processing
- **Frame Sampling**: Processes every 3rd frame for speed
- **Resolution**: Optimized for standard video formats
- **Duration**: Recommended 30-60 seconds for best results

### Scalability
- **Async Processing**: Background video analysis
- **File Storage**: Local storage with cleanup options
- **Database**: Efficient queries with proper indexing

## Testing

Run the test suite:
```bash
python manage.py test Child.tests.ExerciseValidatorTestCase
```

Tests cover:
- Exercise type detection
- Angle calculations
- Model creation and accuracy
- String representations

## Troubleshooting

### Common Issues

1. **Video Processing Fails**
   - Check video format (MP4, AVI, MOV, WMV)
   - Ensure video contains clear full-body view
   - Verify MediaPipe installation

2. **Low Accuracy Scores**
   - Improve lighting conditions
   - Ensure full body is visible
   - Check camera angle and distance

3. **Repetition Counting Issues**
   - Adjust angle thresholds in configuration
   - Ensure consistent exercise form
   - Check video frame rate and quality

### Debug Mode
Enable detailed logging:
```python
import logging
logging.getLogger('Child.utils.exercise_validator').setLevel(logging.DEBUG)
```

## Future Enhancements

### Planned Features
- **Real-time Processing**: Live pose detection during exercise
- **Advanced Exercises**: More complex movement patterns
- **Machine Learning**: Improved accuracy with training data
- **Mobile App**: Native mobile video capture
- **Social Features**: Progress sharing and challenges

### Technical Improvements
- **Celery Integration**: Distributed video processing
- **Cloud Storage**: Scalable file storage
- **API Versioning**: RESTful API for external integrations
- **WebSocket**: Real-time status updates

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request with documentation

## License

This project is part of the PhysioMilestones platform for children's physiotherapy.

## Support

For technical support or feature requests, please contact the development team.
