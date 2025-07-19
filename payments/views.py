"""Payment API for Zarinpal integration"""
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ZarinpalPaymentView(APIView):
    def post(self, request):
        data = request.data
        amount = data.get('amount')
        description = data.get('description')
        callback_url = data.get('callback_url')
        merchant_id = 'YOUR_ZARINPAL_MERCHANT_ID'

        payment_request = {
            'merchant_id': merchant_id,
            'amount': amount,
            'callback_url': callback_url,
            'description': description
        }

        response = requests.post('https://api.zarinpal.com/pg/v4/payment/request.json', json=payment_request)
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get('data', {}).get('code') == 100:
                authority = res_data['data']['authority']
                return Response({'payment_url': f'https://www.zarinpal.com/pg/StartPay/{authority}'})
        return Response({'error': 'Payment request failed.'}, status=status.HTTP_400_BAD_REQUEST)
