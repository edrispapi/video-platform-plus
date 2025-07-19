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
        return Response({'status': 'AI processing started', 'video_id': video.id}, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        query = request.query_params.get('q', '')
        videos = Video.objects.filter(title__icontains=query)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        video = self.get_object()
        comment = request.data.get('comment')
        video.comments.create(user=request.user, text=comment)  # فرض مدل Comment
        return Response({'status': 'comment added'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def like_video(self, request, pk=None):
        video = self.get_object()
        video.likes.add(request.user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)
