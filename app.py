# Vercel's app.py

from flask import Flask, render_template, request, jsonify
import json
import os
import requests 

app = Flask(__name__)

# This is the public URL of your bot running on Railway/Render
BOT_API_BASE_URL = "http://your-bot-project-name.up.railway.app" # <-- IMPORTANT: Change this!
BOT_API_PORT = "30151" 

@app.route('/')
def index():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'emotes.json')
        
        with open(file_path, 'r') as f:
            emotes = json.load(f)
        
        return render_template('index.html', emotes=emotes) 
    except FileNotFoundError:
        return jsonify({'message': 'Error: emotes.json or index.html not found'}), 500
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/send_emote', methods=['POST'])
def send_emote():
    try:
        data = request.get_json()
        team_code = data.get('team_code')
        emote_id = data.get('emote_id')
        uids = data.get('uids', [])

        # IMPROVEMENT: Use the more descriptive 400 error check 
        # (This resolves the less descriptive error message you previously saw)
        missing_fields = []
        if not team_code:
            missing_fields.append("team_code")
        if not emote_id:
            missing_fields.append("emote_id")
        if not uids or not isinstance(uids, list) or len(uids) == 0:
            missing_fields.append("uids (must be a non-empty list)")

        if missing_fields:
            return jsonify({
                'message': 'Error: Missing required data fields in POST request body.',
                'missing': missing_fields
            }), 400

        # Build the parameters for the API call to your bot
        params = {
            'emote_id': emote_id,
            'tc': team_code
        }
        for i, uid in enumerate(uids[:4]):
            params[f'uid{i+1}'] = uid

        api_url = f"{BOT_API_BASE_URL}:{BOT_API_PORT}/join"
        
        # FIX: Changed requests.get to requests.post to resolve 405 Method Not Allowed error
        response = requests.post(api_url, data=params, timeout=45) 
        
        response.raise_for_status() 

        # Using response.text to avoid JSONDecodeError (Expecting value)
        api_response_content = response.text if response.text else "Bot API returned empty content (Success, but No Content)."

        return jsonify({
            'message': 'Emote request sent successfully to the bot!',
            'api_response': api_response_content
        }), 200

    except requests.exceptions.RequestException as e:
        # Catch connection and SSL errors
        return jsonify({
            'message': 'Error communicating with the external Bot API.',
            'error_details': str(e)
        }), 503 

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred on Vercel: {e}'}), 500
