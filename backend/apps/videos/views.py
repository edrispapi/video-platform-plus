import jwt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from ai_engine.tasks import process_video_for_branding_removal
from datetime import datetime, timedelta

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
        text = request.data.get('text')
        parent_id = request.data.get('parent_id')
        comment = Comment.objects.create(video=video, user=request.user, text=text)
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
            comment.parent = parent_comment
            comment.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def like_video(self, request, pk=None):
        video = self.get_object()
        video.likes.add(request.user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def authenticate(self, request, pk=None):
        token = request.headers.get('X-Token')
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            if payload.get('exp') < datetime.utcnow().timestamp():
                return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status': 'authenticated'}, status=status.HTTP_200_OK)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['get'])
    def get_token(self, request, pk=None):
        video = self.get_object()
        token = jwt.encode(
            {'video_id': video.id, 'exp': (datetime.utcnow() + timedelta(minutes=10)).timestamp()},
            'your_secret_key',
            algorithm='HS256'
        )
        return Response({'token': token}, status=status.HTTP_200_OK)
