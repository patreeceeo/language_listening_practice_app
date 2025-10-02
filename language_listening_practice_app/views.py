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
        'video_url': 'https://www.youtube.com/embed/IJEn-9nAFQE?clip=UgkxHECVQoFBYuSrsZx59oRIsjzQlHaa_fdC&clipt=EPiARhi4v0Y',
        'is_new': True
    }

    return render(request, 'exercise_detail.html', context)
