from django.db.models import (
    Model, CharField, FloatField, ForeignKey, TextField, BooleanField,
    ManyToManyField, DateTimeField, JSONField, CASCADE, Q, OuterRef, Subquery, Max,
    IntegerField
    )
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from .utils import loose_str_compare, relative_datetime

class YouTubeClip(Model):
    video_id = CharField(max_length=20)
    start_seconds = FloatField()
    end_seconds = FloatField()

    def __str__(self):
        return f"{self.video_id} ({self.start_seconds}-{self.end_seconds})"

class Exercise(Model):
    TYPES = {
        "shadow": "Shadowing",
        "transcribe": "Transcription",
        "multiple_choice": "Multiple Choice",
    }
    type = CharField(choices=TYPES)
    youtube_clip = ForeignKey(YouTubeClip, on_delete=CASCADE)
    question = TextField(blank=True, null=True)
    answers = JSONField(blank=True, null=True)  # For multiple choice
    correct_answer = CharField(max_length=255, blank=True, null=True)
    show_video = BooleanField(default=True)

    @staticmethod
    def get_practice_set(max_last_attempt_time = None) -> QuerySet["Exercise"]:
        """
        Get exercises that either:
        1. Have never been attempted
        2. Were last attempted incorrectly
        3. Were last attempted more than rest_interval minutes ago
        Return them in random order.
        """
        if max_last_attempt_time is None:
            max_last_attempt_time = relative_datetime()
        latest_attempt = ExerciseAttempt.objects.filter(
            exercise=OuterRef('pk')
            ).order_by('-timestamp').values('is_correct')[:1]

        return Exercise.objects.annotate(
            last_attempt_time=Max('exerciseattempt__timestamp'),
            last_attempt_correct=Subquery(latest_attempt)
        ).filter(
            Q(exerciseattempt__isnull=True) | # Never attempted
            Q(last_attempt_correct=False) | # Last attempt was incorrect
            Q(last_attempt_time__lt=max_last_attempt_time)
        ).distinct().order_by('?')  # Random order

    def is_correct(self, answer: str) -> bool:
        """Check if the provided answer is correct."""
        if self.type == 'shadow':
            return True

        return loose_str_compare(answer, self.correct_answer)


    def __str__(self):
        return f"{self.type} for clip {self.youtube_clip}"

class Lesson(Model):
    number = IntegerField()
    title = CharField(max_length=255)
    exercises = ManyToManyField(Exercise)

    def __str__(self):
        return f"#{self.number} {self.title}"

class ExerciseAttempt(Model):
    exercise = ForeignKey(Exercise, on_delete=CASCADE)
    user_answer = TextField()
    is_correct = BooleanField()
    timestamp = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"{self.exercise} at {self.timestamp}"
