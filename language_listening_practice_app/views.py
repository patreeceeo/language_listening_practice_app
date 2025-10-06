from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

exercise_data = [
    {
        'type': 'shadow',
        'is_new': True,
        'lesson_number': 3,
        'lesson_title': 'The Art of Japanese',
        'progress_percentage': 33,
        'exercise_number': 33,
        'total_exercises': 100,
        'exercise_title': 'An Aphorism',
        'youtube_video_id': 'IJEn-9nAFQE',
        'start_seconds': 84.7,
        'end_seconds': 92,
    },
    {
        'type': 'transcribe',
        'is_new': True,
        'lesson_number': 3,
        'lesson_title': 'The Art of Japanese',
        'progress_percentage': 33,
        'exercise_number': 33,
        'total_exercises': 100,
        'exercise_title': 'An Aphorism',
        'youtube_video_id': 'IJEn-9nAFQE',
        'start_seconds': 84.7,
        'end_seconds': 92,
        'correct_answer': "どういうおんがくをきくの? すきなおんがくはろっく。",
    },
    {
        'type': 'multiple_choice',
        'is_new': True,
        'lesson_number': 3,
        'lesson_title': 'The Art of Japanese',
        'progress_percentage': 33,
        'exercise_number': 33,
        'total_exercises': 100,
        'exercise_title': 'An Aphorism',
        'youtube_video_id': 'IJEn-9nAFQE',
        'start_seconds': 84.7,
        'end_seconds': 92,
        'question': "What is the capital of France?",
        'choices': ["Berlin", "Madrid", "Paris", "Rome"],
        'correct_answer': "Paris",
    },
]

data = {
    'current_exercise': 0,
    'exercises': exercise_data,
}

template_mapping = {
    'shadow': 'exercise_shadow.html',
    'transcribe': 'exercise_transcribe.html',
    'multiple_choice': 'exercise_multiple_choice.html',
}

def current_exercise(request):
    """Display the current exercise page."""
    exercise_number = data['current_exercise']

    if(exercise_number == len(data['exercises'])):
        return render(request, 'all_done.html')
    else:
        context = data['exercises'][exercise_number]
        return render(request, template_mapping[context['type']], context)


def submit_answer(request):
    data['current_exercise'] += 1
    return HttpResponseRedirect(reverse("current_exercise"))

