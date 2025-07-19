from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.videos.models import Video
from apps.videos.serializers import VideoSerializer # serializer باید در همین اپلیکیشن باشد
from apps.videos.tasks import process_video_for_branding_removal

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def start_ai_processing(self, request, pk=None):
        """
        شروع پردازش هوش مصنوعی (حذف لوگو و واترمارک صوتی) برای یک ویدئو.
        """
        video = self.get_object()
        # فراخوانی وظیفه Celery
        process_video_for_branding_removal.delay(video.id)
        return Response(
            {'status': 'AI processing started for video', 'video_id': video.id},
            status=status.HTTP_202_ACCEPTED
        )
