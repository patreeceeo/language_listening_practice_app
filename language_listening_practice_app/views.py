from django.shortcuts import render


def exercise_detail(request, exercise_id):
    """Display an exercise detail page."""

    # Sample data - replace with database queries later
    context = {
        'lesson_number': 3,
        'lesson_title': 'The Art of Japanese',
        'progress_percentage': 33,
        'exercise_number': 33,
        'total_exercises': 100,
        'exercise_title': 'An Aphorism',
        'youtube_video_id': 'IJEn-9nAFQE',
        'start_seconds': 85,
        'end_seconds': 95,
        'is_new': True
    }

    return render(request, 'exercise_detail.html', context)
