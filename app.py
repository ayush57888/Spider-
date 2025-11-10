# Vercel's app.py

from flask import Flask, render_template, request, jsonify
import json
import os
import requests 

app = Flask(__name__)

# =================================================================
# 🛑 CRITICAL: REPLACE THIS WITH YOUR REAL RAILWAY PUBLIC URL
# IMPORTANT: Removed the port variable and concatenation. 
# Railway exposes the app directly on the domain (e.g., port 443/80).
# =================================================================
BOT_API_BASE_URL = "http://your-bot-project-name.up.railway.app" # <--- IMPORTANT: Change this!
# We no longer need BOT_API_PORT, as the base URL should handle it.

@app.route('/')
def index():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'emotes.json')
        
        with open(file_path, 'r') as f:
            emotes = json.load(f)
        
        # Assumes you have an 'index.html' file in a 'templates' folder
        return render_template('index.html', emotes=emotes) 
    except FileNotFoundError:
        return jsonify({'message': 'Error: emotes.json or index.html not found on Vercel.'}), 500
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/send_emote', methods=['POST'])
def send_emote():
    try:
        data = request.get_json()
        team_code = data.get('team_code')
        emote_id = data.get('emote_id')
        uids = data.get('uids', [])

        # ... (Validation logic) ...
        missing_fields = []
        if not team_code: missing_fields.append("team_code")
        if not emote_id: missing_fields.append("emote_id")
        if not uids or not isinstance(uids, list) or len(uids) == 0: missing_fields.append("uids (must be a non-empty list)")

        if missing_fields:
            return jsonify({'message': 'Error: Missing required data fields.', 'missing': missing_fields}), 400

        # Build the parameters for the API call to your bot
        params = {
            'emote_id': emote_id,
            'tc': team_code
        }
        for i, uid in enumerate(uids[:4]):
            params[f'uid{i+1}'] = uid

        # FIX: Removed explicit port number in the URL concatenation
        api_url = f"{BOT_API_BASE_URL}/join"
        
        # FIX: Using POST method to match the bot's route
        response = requests.post(api_url, data=params, timeout=45) 
        
        response.raise_for_status() 

        api_response_content = response.text if response.text else "Bot API returned empty content (Success, but No Content)."

        return jsonify({
            'message': 'Emote request sent successfully to the bot!',
            'api_response': api_response_content
        }), 200

    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, 'status_code', 503)
        return jsonify({
            'message': 'Error communicating with the external Bot API (Check if bot is running).',
            'error_details': str(e),
            'api_status_code': status_code
        }), status_code 

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred on Vercel: {e}'}), 500

# --- END OF FILE app.py ---
