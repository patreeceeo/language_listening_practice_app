from django.shortcuts import render


def _get_exercise_context(exercise_id):
    """Get common context data for exercise views."""
    # Sample data - replace with database queries later
    return {
        'lesson_number': 3,
        'lesson_title': 'The Art of Japanese',
        'progress_percentage': 33,
        'exercise_number': 33,
        'total_exercises': 100,
        'exercise_title': 'An Aphorism',
        'youtube_video_id': 'IJEn-9nAFQE',
        'start_seconds': 84.7,
        'end_seconds': 92,
        'is_new': True,
        'transcript': "どういうおんがくをきくの? すきなおんがくはろっく。",
    }


def exercise_shadow(request, exercise_id):
    """Display a shadow exercise page with recording and navigation."""
    context = _get_exercise_context(exercise_id)
    return render(request, 'exercise_shadow.html', context)


def exercise_transcribe(request, exercise_id):
    """Display transcription exercise without recording or navigation."""
    context = _get_exercise_context(exercise_id)
    return render(request, 'exercise_transcribe.html', context)

