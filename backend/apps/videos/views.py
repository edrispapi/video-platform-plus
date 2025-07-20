import jwt
import random
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Video, Comment
from .serializers import VideoSerializer, CommentSerializer
from ai_engine.tasks import process_video_for_branding_removal
from datetime import datetime, timedelta
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://your-blockchain-node'))  # نود بلاکچین
contract_address = 'your_contract_address'  # آدرس قرارداد هوشمند
contract_abi = [...]  # ABI قرارداد (باید از کد قرارداد کپی بشه)
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

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

    @action(detail=True, methods=['get'])
    def get_ad(self, request, pk=None):
        # شبیه‌سازی Real-time Bidding
        ads = [
            {'id': 1, 'url': 'ad1.mp4', 'bid': random.uniform(0.1, 1.0)},
            {'id': 2, 'url': 'ad2.mp4', 'bid': random.uniform(0.1, 1.0)},
            {'id': 3, 'url': 'ad3.mp4', 'bid': random.uniform(0.1, 1.0)}
        ]
        best_ad = max(ads, key=lambda x: x['bid'])
        return Response({'ad_url': best_ad['url']}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def record_revenue(self, request, pk=None):
        video = self.get_object()
        amount = request.data.get('amount', 0.0)
        account = w3.eth.account.from_key('your_private_key')  # کلید خصوصی امن
        tx = contract.functions.recordRevenue(video.id, amount).buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 200000,
            'gasPrice': w3.toWei('50', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, 'your_private_key')
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return Response({'tx_hash': tx_hash.hex()}, status=status.HTTP_200_OK)
