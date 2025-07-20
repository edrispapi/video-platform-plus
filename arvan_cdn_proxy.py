import os
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)

ARVAN_API_KEY = os.getenv('ARVAN_API_KEY')
ARVAN_DOMAIN = os.getenv('ARVAN_DOMAIN')
ARVAN_CDN_ENDPOINT = os.getenv('ARVAN_CDN_ENDPOINT')

@app.route('/hls/<path:path>')
def serve_hls(path):
    url = f"{ARVAN_CDN_ENDPOINT}/hls/{path}"
    headers = {'Authorization': f'Bearer {ARVAN_API_KEY}'}
    response = requests.get(url, headers=headers, stream=True)
    return response.content, response.status_code, {'Content-Type': 'application/vnd.apple.mpegurl'}

@app.route('/dash/<path:path>')
def serve_dash(path):
    url = f"{ARVAN_CDN_ENDPOINT}/dash/{path}"
    headers = {'Authorization': f'Bearer {ARVAN_API_KEY}'}
    response = requests.get(url, headers=headers, stream=True)
    return response.content, response.status_code, {'Content-Type': 'application/dash+xml'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
