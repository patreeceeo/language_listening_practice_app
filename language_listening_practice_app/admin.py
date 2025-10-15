from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import JsonResponse
import re

from .models import YouTubeClip, Exercise, ExerciseAttempt

@admin.register(YouTubeClip)
class YouTubeClipAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_seconds', 'end_seconds', 'video_id')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['create_clip_url'] = 'create-clip/'
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-clip/', self.admin_site.admin_view(self.create_clip_view), name='youtubeclip_create_clip'),
            path('<path:object_id>/edit-clip/', self.admin_site.admin_view(self.edit_clip_view), name='youtubeclip_edit_clip'),
        ]
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Redirect to custom edit view
        return redirect('admin:youtubeclip_edit_clip', object_id=object_id)

    def add_view(self, request, form_url='', extra_context=None):
        # Redirect to custom create view
        return redirect('admin:youtubeclip_create_clip')

    def create_clip_view(self, request):
        if request.method == 'POST':
            video_id = request.POST.get('video_id')
            start_seconds = float(request.POST.get('start_seconds'))
            end_seconds = float(request.POST.get('end_seconds'))
            title = request.POST.get('title', '')

            clip = YouTubeClip.objects.create(
                video_id=video_id,
                start_seconds=start_seconds,
                end_seconds=end_seconds,
                title=title if title else None
            )
            return redirect('admin:language_listening_practice_app_youtubeclip_changelist')

        return render(request, 'admin/youtube_clip_create.html', {
            'site_header': admin.site.site_header,
            'site_title': admin.site.site_title,
            'opts': self.model._meta,
            'is_edit': False,
        })

    def edit_clip_view(self, request, object_id):
        clip = YouTubeClip.objects.get(pk=object_id)

        if request.method == 'POST':
            clip.video_id = request.POST.get('video_id')
            clip.start_seconds = float(request.POST.get('start_seconds'))
            clip.end_seconds = float(request.POST.get('end_seconds'))
            clip.title = request.POST.get('title', '') or None
            clip.save()
            return redirect('admin:language_listening_practice_app_youtubeclip_changelist')

        return render(request, 'admin/youtube_clip_create.html', {
            'site_header': admin.site.site_header,
            'site_title': admin.site.site_title,
            'opts': self.model._meta,
            'is_edit': True,
            'clip': clip,
        })

admin.site.register(Exercise)
admin.site.register(ExerciseAttempt)
