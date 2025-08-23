from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ExerciseVideo, ExerciseSession
from .utils.exercise_validator import ExerciseValidator
from Doctor.models import Exercise, AssignExercise
import tempfile
import os

User = get_user_model()

class ExerciseValidatorTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testchild',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Child',
            age=10,
            parent_name='Test Parent'
        )
        
        # Create test exercise
        self.exercise = Exercise.objects.create(
            name='Arm Raises',
            description='Raise your arms above your head',
            instruction='Stand straight and raise both arms above your head'
        )
        
        # Create test assignment
        self.assignment = AssignExercise.objects.create(
            Patient_name=self.user,
            Exercise=self.exercise,
            reps=10,
            sets=3
        )
    
    def test_exercise_type_detection(self):
        """Test exercise type detection from exercise names."""
        validator = ExerciseValidator()
        
        # Test arm raise detection
        self.assertEqual(validator.get_exercise_type_from_name('Arm Raises'), 'arm_raise')
        self.assertEqual(validator.get_exercise_type_from_name('Arm Lift'), 'arm_raise')
        
        # Test squat detection
        self.assertEqual(validator.get_exercise_type_from_name('Squats'), 'squat')
        self.assertEqual(validator.get_exercise_type_from_name('Sit Down'), 'squat')
        
        # Test jumping jack detection
        self.assertEqual(validator.get_exercise_type_from_name('Jumping Jacks'), 'jumping_jack')
        
        # Test default case
        self.assertEqual(validator.get_exercise_type_from_name('Unknown Exercise'), 'arm_raise')
    
    def test_angle_calculation(self):
        """Test angle calculation between three points."""
        validator = ExerciseValidator()
        
        # Test right angle
        angle = validator.calculate_angle((0, 0), (0, 1), (1, 1))
        self.assertAlmostEqual(angle, 90.0, places=1)
        
        # Test straight line
        angle = validator.calculate_angle((0, 0), (1, 0), (2, 0))
        self.assertAlmostEqual(angle, 180.0, places=1)
    
    def test_exercise_video_creation(self):
        """Test ExerciseVideo model creation and accuracy calculation."""
        # Create a mock video file
        video_content = b'fake video content'
        video_file = SimpleUploadedFile(
            "test_video.mp4",
            video_content,
            content_type="video/mp4"
        )
        
        # Create exercise video
        exercise_video = ExerciseVideo.objects.create(
            assignment=self.assignment,
            video=video_file,
            target_reps=10,
            target_sets=3,
            total_reps=8,
            total_sets=2,
            accuracy_score=85.0
        )
        
        # Test accuracy calculation
        exercise_video.calculate_accuracy()
        
        # Check calculated accuracies
        self.assertEqual(exercise_video.reps_accuracy, 80.0)  # 8/10 * 100
        self.assertEqual(exercise_video.sets_accuracy, 66.67)  # 2/3 * 100
        self.assertAlmostEqual(exercise_video.overall_score, 77.22, places=1)  # (80 + 66.67 + 85) / 3
    
    def test_exercise_session_creation(self):
        """Test ExerciseSession model creation."""
        session = ExerciseSession.objects.create(
            patient=self.user,
            assignment=self.assignment,
            videos_uploaded=5,
            average_accuracy=85.5
        )
        
        self.assertEqual(session.patient, self.user)
        self.assertEqual(session.assignment, self.assignment)
        self.assertEqual(session.videos_uploaded, 5)
        self.assertEqual(session.average_accuracy, 85.5)
    
    def test_model_string_representations(self):
        """Test model string representations."""
        # Create exercise video
        video_content = b'fake video content'
        video_file = SimpleUploadedFile(
            "test_video.mp4",
            video_content,
            content_type="video/mp4"
        )
        
        exercise_video = ExerciseVideo.objects.create(
            assignment=self.assignment,
            video=video_file
        )
        
        # Test string representation
        expected_str = f"Video for {self.user.first_name} - {self.exercise.name}"
        self.assertEqual(str(exercise_video), expected_str)
        
        # Create session
        session = ExerciseSession.objects.create(
            patient=self.user,
            assignment=self.assignment
        )
        
        # Test session string representation
        expected_session_str = f"Session for {self.user.first_name} - {session.session_date.date()}"
        self.assertEqual(str(session), expected_session_str)
