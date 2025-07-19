from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import DashboardConfig
from .serializers import DashboardConfigSerializer

class DashboardConfigViewSet(viewsets.ModelViewSet):
    queryset = DashboardConfig.objects.all()
    serializer_class = DashboardConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        """دریافت تنظیمات داشبورد کاربر"""
        config = DashboardConfig.objects.get(user=request.user)
        serializer = DashboardConfigSerializer(config)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """به‌روزرسانی تنظیمات داشبورد"""
        config = DashboardConfig.objects.get(user=request.user)
        serializer = DashboardConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
