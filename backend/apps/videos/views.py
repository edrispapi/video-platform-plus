from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.videos.models import Video
from apps.videos.serializers import VideoSerializer
from ai_engine.tasks import process_video_for_branding_removal

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def start_ai_processing(self, request, pk=None):
        video = self.get_object()
        process_video_for_branding_removal.delay(video.id)
        return Response({'status': 'AI processing started for video', 'video_id': video.id}, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        """جستجوی ویدئوها با پارامتر q"""
        query = request.query_params.get('q', '')
        videos = Video.objects.filter(title__icontains=query)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """آپلود ویدئو جدید"""
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
