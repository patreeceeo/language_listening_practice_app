from django.contrib import admin

from .models import YouTubeClip, Exercise, ExerciseAttempt

admin.site.register(YouTubeClip)
admin.site.register(Exercise)
admin.site.register(ExerciseAttempt)
