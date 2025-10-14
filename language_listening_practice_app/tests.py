from django.test import TestCase
from django.contrib.auth.models import User
from .models import Exercise, YouTubeClip, ExerciseAttempt
from .utils import relative_datetime

class ExercisePracticeSetTestCase(TestCase):
    def setUp(self):
        self.next_user_id = 0

    def _create_youtube_clip(self):
        return YouTubeClip.objects.create(video_id='abc123', start_seconds=0, end_seconds=10)

    def _create_user(self):
        id = self.next_user_id
        self.next_user_id += 1
        return User.objects.create_user(username=f'user{id}', password='12345')

    def test_never_attempted(self):
        user = self._create_user()
        Exercise.objects.create(
            type='shadow',
            youtube_clip=self._create_youtube_clip(),
            question='',
            correct_answer=''
        )
        exercises = Exercise.get_practice_set(user)
        self.assertEqual(exercises.count(), 1, "Should include never attempted exercises")

    def test_last_attempt_incorrect(self):
        exercise = Exercise.objects.create(
            type='transcribe',
            youtube_clip=self._create_youtube_clip(),
            question='What is said?',
            correct_answer='Hello'
        )
        user = self._create_user()
        ExerciseAttempt.objects.create(
            user=user,
            exercise=exercise,
            user_answer='Hi',
            is_correct=False,
        )
        exercises = Exercise.get_practice_set(user)
        self.assertIn(exercise, exercises, "Should include exercises with last attempt incorrect")

    def test_last_attempt_before_rest_interval(self):
        exercise = Exercise.objects.create(
            type='multiple_choice',
            youtube_clip=self._create_youtube_clip(),
            question='Choose the correct option',
            answers=['Option A', 'Option B', 'Option C'],
            correct_answer='Option A'
        )
        user = self._create_user()
        attempt = ExerciseAttempt.objects.create(
            user=user,
            exercise=exercise,
            user_answer='Option A',
            is_correct=True,
        )
        # Have to manually set timestamp after creation because auto_now_add
        attempt.timestamp = relative_datetime(minutes=-10)
        attempt.save()

        exercises = Exercise.get_practice_set(user, relative_datetime(minutes=-5))
        self.assertIn(exercise, exercises, "Should include exercises last attempted before rest interval regardless of correctness")

    def test_attempted_by_other_user(self):
        exercise = Exercise.objects.create(
            type='shadow',
            youtube_clip=self._create_youtube_clip(),
            question='',
            correct_answer=''
        )
        user = self._create_user()
        other_user = self._create_user()
        ExerciseAttempt.objects.create(
            user=other_user,
            exercise=exercise,
            user_answer='',
            is_correct=True,
        )
        exercises = Exercise.get_practice_set(user, relative_datetime(minutes=-1))
        self.assertIn(exercise, exercises, "Should include exercises attempted by other users")

    def test_multiple_attempts(self):
        clip = self._create_youtube_clip()
        exercise = Exercise.objects.create(
            type='shadow',
            youtube_clip=clip,
            question='',
            correct_answer=''
        )
        user = self._create_user()
        ExerciseAttempt.objects.create(
            user=user,
            exercise=exercise,
            user_answer='',
            is_correct=False,
        )
        ExerciseAttempt.objects.create(
            user=user,
            exercise=exercise,
            user_answer='Hi',
            is_correct=False,
        )
        exercises = Exercise.get_practice_set(user, relative_datetime(minutes=-1))
        self.assertEqual(exercises.count(), 1, "Should return distinct exercises")

    def test_distinct_exercises(self):
        user = self._create_user()
        ex1 = Exercise.objects.create(
            type='shadow',
            youtube_clip=self._create_youtube_clip(),
            question='',
            correct_answer=''
        )
        ex2 = Exercise.objects.create(
            type='transcribe',
            youtube_clip=self._create_youtube_clip(),
            question='What is said?',
            correct_answer='Hello'
        )

        # Create multiple attempts for each
        ExerciseAttempt.objects.create(user=user, exercise=ex1, is_correct=False)
        ExerciseAttempt.objects.create(user=user, exercise=ex1, is_correct=False)
        ExerciseAttempt.objects.create(user=user, exercise=ex2, is_correct=False)

        exercises = Exercise.get_practice_set(user)
        exercise_list = list(exercises)

        # Check no duplicates
        self.assertEqual(len(exercise_list), len(set(exercise_list)))
        # Or check both exercises appear exactly once
        self.assertEqual(exercise_list.count(ex1), 1)
        self.assertEqual(exercise_list.count(ex2), 1)

        self.assertEqual(
            exercises.count(),
            exercises.values('id').distinct().count(),
            "Should return distinct exercises even with multiple attempts"
        )

    def test_distinct_when_multiple_conditions_match(self):
        user = self._create_user()
        exercise = Exercise.objects.create(
            type='shadow',
            youtube_clip=self._create_youtube_clip(),
            question='',
            correct_answer=''
        )

        # Create attempt that's BOTH incorrect AND old
        attempt = ExerciseAttempt.objects.create(
                user=user, exercise=exercise, is_correct=False
                )
        attempt.timestamp = relative_datetime(minutes=-10)
        attempt.save()

        # This exercise matches TWO conditions - should still appear once
        exercises = Exercise.get_practice_set(user, relative_datetime(minutes=-5))
        self.assertEqual(exercises.count(), 1, "Should return distinct exercises even if multiple conditions match")
