from django.shortcuts import render
import random

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
        'transcript': "どういうおんがくをきくの? すきなおんがくはろっく。",
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

template_mapping = {
    'shadow': 'exercise_shadow.html',
    'transcribe': 'exercise_transcribe.html',
    'multiple_choice': 'exercise_multiple_choice.html',
}

def exercise(request, exercise_id: int):
    """Display a shadow exercise page."""
    context = exercise_data[exercise_id % len(exercise_data)]

    return render(request, template_mapping[context['type']], context)


