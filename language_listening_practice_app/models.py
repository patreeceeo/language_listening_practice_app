from django.db import models

class YouTubeClip(models.Model):
    video_id = models.CharField(max_length=20)
    start_seconds = models.FloatField()
    end_seconds = models.FloatField()

    def __str__(self):
        return f"{self.video_id} ({self.start_seconds}-{self.end_seconds})"

class Exercise(models.Model):
    TYPES = {
        "shadow": "Shadowing",
        "transcribe": "Transcription",
        "multiple_choice": "Multiple Choice",
    }
    type = models.CharField(choices=TYPES)
    youtube_clip = models.ForeignKey(YouTubeClip, on_delete=models.CASCADE)
    question = models.TextField(blank=True, null=True)
    answers = models.JSONField(blank=True, null=True)  # For multiple choice
    correct_answer = models.CharField(max_length=255, blank=True, null=True)
    show_video = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} for clip {self.youtube_clip}"

class Lesson(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return f"#{self.number} {self.title}"

class ExerciseAttempt(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise} at {self.timestamp}"
