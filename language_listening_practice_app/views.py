from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Exercise, ExerciseAttempt

def get_exercise_context(exercise: Exercise):
    attempts = ExerciseAttempt.objects.filter(exercise=exercise)
    return {
        'exercise_id': exercise.id,
        'type': exercise.type,
        'is_new': not attempts.exists(),
        'lesson_number': 1,  # Placeholder, implement logic to get lesson number
        'lesson_title': "The Art of Japanese",  # Placeholder, implement logic to get lesson title
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

@login_required(login_url='/accounts/login/')
def current_exercise(request: HttpRequest):
    """Display the current exercise page."""
    exercises = Exercise.get_practice_set()

    if not exercises.exists():
        return render(request, 'all_done.html')

    context = get_exercise_context(exercises.first())
    template = template_mapping.get(context['type'])
    return render(request, template, context)

@login_required(login_url='/accounts/login/')
def submit_answer(request: HttpRequest):
    """Handle submission of an exercise answer."""
    exercise_id = request.POST.get('exercise_id')
    exercise = Exercise.objects.get(id=exercise_id)
    answer = request.POST.get('answer') if exercise.type != 'shadow' else '';
    is_correct = exercise.is_correct(answer)

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
    return HttpResponseRedirect(reverse("current_exercise"))

