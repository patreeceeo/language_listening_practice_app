from django.test import TestCase
from django.contrib.auth.models import User
from .models import Exercise, YouTubeClip, ExerciseAttempt
from .utils import relative_datetime

class ExercisePracticeSetTestCase(TestCase):
    def _create_youtube_clip(self):
        return YouTubeClip.objects.create(video_id='abc123', start_seconds=0, end_seconds=10)

    def test_never_attempted(self):
        Exercise.objects.create(
            type='shadow',
            youtube_clip=self._create_youtube_clip(),
            question='',
            correct_answer=''
        )
        exercises = Exercise.get_practice_set()
        self.assertEqual(exercises.count(), 1, "Should include never attempted exercises")

    def test_last_attempt_incorrect(self):
        exercise = Exercise.objects.create(
            type='transcribe',
            youtube_clip=self._create_youtube_clip(),
            question='What is said?',
            correct_answer='Hello'
        )
        user = User.objects.create_user(username='testuser', password='12345')
        ExerciseAttempt.objects.create(
            user=user,
            exercise=exercise,
            user_answer='Hi',
            is_correct=False,
        )
        exercises = Exercise.get_practice_set()
        self.assertIn(exercise, exercises, "Should include exercises with last attempt incorrect")

    def test_last_attempt_before_rest_interval(self):
        exercise = Exercise.objects.create(
            type='multiple_choice',
            youtube_clip=self._create_youtube_clip(),
            question='Choose the correct option',
            answers=['Option A', 'Option B', 'Option C'],
            correct_answer='Option A'
        )
        user = User.objects.create_user(username='testuser2', password='12345')
        attempt = ExerciseAttempt.objects.create(
            user=user,
            exercise=exercise,
            user_answer='Option A',
            is_correct=True,
        )
        # Have to manually set timestamp after creation because auto_now_add
        attempt.timestamp = relative_datetime(minutes=-10)
        attempt.save()

        exercises = Exercise.get_practice_set(relative_datetime(minutes=-5))
        self.assertIn(exercise, exercises, "Should include exercises last attempted before rest interval regardless of correctness")

