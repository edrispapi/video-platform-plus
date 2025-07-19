from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from apps.videos.models import Video
from apps.videos.serializers import VideoSerializer

class DevVideoAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
