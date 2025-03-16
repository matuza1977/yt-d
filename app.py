from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pytube import YouTube
import re

app = Flask(__name__)
CORS(app)  # Habilita CORS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_url', methods=['POST'])
def get_url():
    url = request.json['url']
    
    if not re.match(r'^https?://(www\.)?(youtube\.com|youtu\.be)/', url):
        return jsonify({'error': 'URL inválida'})
    
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        return jsonify({
            'title': yt.title,
            'url': stream.url,
            'thumbnail': yt.thumbnail_url
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
