from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .utils import relative_datetime

from .models import Exercise, ExerciseAttempt

def home(request: HttpRequest):
    """Display the home/landing page."""
    return render(request, 'home.html')

def get_exercise_context(exercise: Exercise, total_exercises: int, exercise_index: int) -> dict:
    attempts = ExerciseAttempt.objects.filter(exercise=exercise)
    return {
        'exercise_id': exercise.id,
        'type': exercise.type,
        'is_new': not attempts.exists(),
        'lesson_number': 1,  # Placeholder, implement logic to get lesson number
        'lesson_title': "The Art of Japanese",  # Placeholder, implement logic to get lesson title
        'progress_percentage': (int((exercise_index) / total_exercises * 100) if total_exercises > 0 else 100),
        'exercise_number': exercise_index + 1,
        'total_exercises': total_exercises,
        'youtube_video_id': exercise.youtube_clip.video_id,
        'start_seconds': exercise.youtube_clip.start_seconds,
        'end_seconds': exercise.youtube_clip.end_seconds,
        'show_video': exercise.show_video,
        'question': exercise.question,
        'answers': exercise.answers,
        'correct_answer': exercise.correct_answer,
        'explanation': exercise.explanation,
    }

template_mapping = {
    'shadow': 'exercise_shadow.html',
    'transcribe': 'exercise_transcribe.html',
    'multiple_choice': 'exercise_multiple_choice.html',
}

@login_required(login_url='/accounts/login/')
def profile(request: HttpRequest):
    """Display the user profile page."""
    user = request.user
    attempts = ExerciseAttempt.objects.filter(user=user).order_by('-timestamp')[:10]
    context = {
        'username': user.username,
        'attempts': attempts,
    }
    return render(request, 'profile.html', context)

def get_exercise_set_cache_key(user: User) -> str:
    return f'exercise_practice_set:{user.id}'

def refresh_exercise_set_cache(user: User) -> list[Exercise]:
    """Refresh the exercise set cache for a user."""
    cache_key = get_exercise_set_cache_key(user)
    max_last_attempt_time = relative_datetime(minutes=-1)
    exercises = Exercise.get_practice_set(user, max_last_attempt_time) or []
    cache.set(cache_key, list(exercises), 60)
    return exercises

def get_exercise_practice_set_with_caching(user: User) -> list[Exercise]:
    """Retrieve exercises with caching."""
    cache_key = get_exercise_set_cache_key(user)
    exercises = cache.get(cache_key)
    if exercises is None:
        exercises = refresh_exercise_set_cache(user)
    return exercises

def get_exercise_practice_set_index(user: User) -> int:
    """Retrieve the current index in the exercise practice set with caching."""
    cache_key = f'exercise_practice_set_index:{user.id}'
    index = cache.get(cache_key)
    if index is None:
        index = 0
        cache.set(cache_key, index, 60)
    return index

def next_exercise_practice_set_index(user: User):
    """Increment the exercise practice set index by 1."""
    cache_key = f'exercise_practice_set_index:{user.id}'
    index = get_exercise_practice_set_index(user)
    cache.set(cache_key, index + 1, 60)

def reset_exercise_practice_set_index(user: User):
    """Reset the exercise practice set index to 0."""
    cache_key = f'exercise_practice_set_index:{user.id}'
    cache.set(cache_key, 0, 60)

@login_required(login_url='/accounts/login/')
def current_exercise(request: HttpRequest):
    """Display the current exercise page."""
    exercises = get_exercise_practice_set_with_caching(request.user)
    index = get_exercise_practice_set_index(request.user)

    total_exercises = len(exercises)

    print(f"Total exercises: {total_exercises}, Current index: {index}")

    if index >= total_exercises:
        reset_exercise_practice_set_index(request.user)
        return render(request, 'all_done.html')

    context = get_exercise_context(exercises[index], total_exercises, index)
    template = template_mapping.get(context['type'])
    return render(request, template, context)

@login_required(login_url='/accounts/login/')
def submit_answer(request: HttpRequest):
    """Handle submission of an exercise answer."""
    exercise_id = request.POST.get('exercise_id')
    exercise = Exercise.objects.get(id=exercise_id)
    answer = request.POST.get('answer') if exercise.type != 'shadow' else '';
    is_correct = exercise.is_correct(answer)
    # refresh_exercise_set_cache(request.user)

    print(f"""
          User answered:  '{answer}'
          Correct answer: '{exercise.correct_answer}'
          Correct: {is_correct}
          """)

    attempt = ExerciseAttempt(
            exercise=exercise,
            user_answer=answer,
            is_correct=is_correct,
            user=request.user
    )
    attempt.save()
    increment_exercise_practice_set_index(request.user)
    return HttpResponseRedirect(reverse("current_exercise"))

