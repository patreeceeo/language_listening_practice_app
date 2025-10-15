from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import JsonResponse
import re

from .models import YouTubeClip, Exercise, ExerciseAttempt

@admin.register(YouTubeClip)
class YouTubeClipAdmin(admin.ModelAdmin):
    list_display = ('video_id', 'start_seconds', 'end_seconds')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['create_clip_url'] = 'create-clip/'
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-clip/', self.admin_site.admin_view(self.create_clip_view), name='youtubeclip_create_clip'),
        ]
        return custom_urls + urls

    def create_clip_view(self, request):
        if request.method == 'POST':
            video_id = request.POST.get('video_id')
            start_seconds = float(request.POST.get('start_seconds'))
            end_seconds = float(request.POST.get('end_seconds'))

            clip = YouTubeClip.objects.create(
                video_id=video_id,
                start_seconds=start_seconds,
                end_seconds=end_seconds
            )
            return redirect('admin:language_listening_practice_app_youtubeclip_change', clip.id)

        return render(request, 'admin/youtube_clip_create.html', {
            'site_header': admin.site.site_header,
            'site_title': admin.site.site_title,
            'opts': self.model._meta,
        })

admin.site.register(Exercise)
admin.site.register(ExerciseAttempt)
