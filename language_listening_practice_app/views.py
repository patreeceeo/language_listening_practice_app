from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q, Max, OuterRef, Subquery
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .models import Exercise, ExerciseAttempt
from .utils import loose_str_compare

def get_exercise_context(exercise: Exercise):
    return {
        'exercise_id': exercise.id,
        'type': exercise.type,
        'is_new': True,  # Placeholder, implement logic to check if user has seen this exercise
        'lesson_number': 1,  # Placeholder, implement logic to get lesson number
        'lesson_title': "Sample Lesson",  # Placeholder, implement logic to get lesson title
        'progress_percentage': 0,  # Placeholder, implement logic to calculate progress
        'exercise_number': 1,  # Placeholder, implement logic to get current exercise number
        'total_exercises': Exercise.objects.count(),  # Total exercises in the system
        'youtube_video_id': exercise.youtube_clip.video_id,
        'start_seconds': exercise.youtube_clip.start_seconds,
        'end_seconds': exercise.youtube_clip.end_seconds,
        'show_video': exercise.show_video,
        'question': exercise.question,
        'answers': exercise.answers,
        'correct_answer': exercise.correct_answer,
    }

template_mapping = {
    'shadow': 'exercise_shadow.html',
    'transcribe': 'exercise_transcribe.html',
    'multiple_choice': 'exercise_multiple_choice.html',
}

def get_session_exercises():
    """
    Get exercises that either:
    1. Have never been attempted
    2. Were last attempted incorrectly
    3. Were last attempted more than rest_interval minutes ago
    Return them in random order.
    """
    before_rest_interval = datetime.now(ZoneInfo("UTC")) - timedelta(minutes=1)
    latest_attempt = ExerciseAttempt.objects.filter(
        exercise=OuterRef('pk')
    ).order_by('-timestamp').values('is_correct')[:1]

    return Exercise.objects.annotate(
        last_attempt_time=Max('exerciseattempt__timestamp'),
        last_attempt_correct=Subquery(latest_attempt)
    ).filter(
        Q(exerciseattempt__isnull=True) | # Never attempted
        Q(last_attempt_correct=False) | # Last attempt was incorrect
        Q(last_attempt_time__lt=before_rest_interval) # Last attempt was more than one minute ago
    ).distinct().order_by('?')  # Random order

def current_exercise(request: HttpRequest):
    """Display the current exercise page."""
    exercises = get_session_exercises()

    if not exercises.exists():
        return render(request, 'all_done.html')

    context = get_exercise_context(exercises.first())
    template = template_mapping.get(context['type'])
    return render(request, template, context)

def submit_answer(request: HttpRequest):
    """Handle submission of an exercise answer."""
    exercise_id = request.POST.get('exercise_id')
    exercise = Exercise.objects.get(id=exercise_id)
    answer = request.POST.get('answer') if exercise.type != 'shadow' else '';
    is_correct = loose_str_compare(answer, exercise.correct_answer) if exercise.type != 'shadow' else True

    print(f"""
          User answered:  '{answer}'
          Correct answer: '{exercise.correct_answer}'
          Correct: {is_correct}
          """)

    attempt = ExerciseAttempt(
            exercise=exercise,
            user_answer=answer,
            is_correct=is_correct
    )
    attempt.save()
    return HttpResponseRedirect(reverse("current_exercise"))

