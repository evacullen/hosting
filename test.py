from flask import Flask, request, jsonify
import requests
import time
from flask import send_file

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.args.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    api_url = "https://api.elevenlabs.io/v1/text-to-speech/9BWtsMINqrJLrRacOk9x"
    headers = {
        "xi-api-key": "sk_5cad5860361f77c8232ab18738dfa18f0b02ea87ce5605c0"
    }
    body = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        "optimize_streaming_latency": 3,
        "output_format": "mp3_44100_128"
    }

    response = requests.post(api_url, headers=headers, json=body)
    if response.status_code != 200:
        return jsonify({"error": "API request failed"}), 500

    # output = response.json()
    timestamp = int(time.time())
    with open(f'audio/output_{timestamp}.mpga', 'wb') as f:
        f.write(response.content)

    return jsonify({"message": f"Output saved successfully", "filename": f"output_{timestamp}.mpga"}), 200

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        return send_file(f'audio/{filename}', as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)