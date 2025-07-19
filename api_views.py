"""API Views for Video Platform"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    """مدیریت آپلود و مشاهده ویدئو"""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def start_processing(self, request, pk=None):
        # فراخوانی کار Celery جهت پردازش ویدئویی با هوش مصنوعی
        video = self.get_object()
        from ai_engine.tasks import process_video_ai
        process_video_ai.delay(video.id)
        return Response({'status': 'processing started'}, status=status.HTTP_202_ACCEPTED)
