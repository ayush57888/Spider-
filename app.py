# Vercel's app.py

from flask import Flask, render_template, request, jsonify
import json
import os
import requests # Use requests to call your bot API

app = Flask(__name__)

# =================================================================
# 🛑 CRITICAL FIX: Changed 'https' to 'http' 
# The Railway bot is likely not running SSL on port 30151.
# =================================================================
# This is the public URL of your bot running on Railway/Render
BOT_API_BASE_URL = "http://your-bot-project-name.up.railway.app" # <--- IMPORTANT: Change this!
BOT_API_PORT = "30151" # The port your bot's Flask app is running on

@app.route('/')
def index():
    # Vercel needs access to the emotes.json file
    try:
        # Use a more robust path to ensure Vercel finds the file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'emotes.json')
        
        with open(file_path, 'r') as f:
            emotes = json.load(f)
        
        # NOTE: You must also have an 'index.html' file in a 'templates' folder 
        # for this line to work.
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

        if not all([team_code, emote_id, uids]):
            return jsonify({'message': 'Error: Missing data (team_code, emote_id, uids)'}), 400

        # Build the parameters for the API call to your bot
        # Final URL will be: http://.../join?uid1=...&uid2=...&emote_id=...&tc=...
        params = {
            'emote_id': emote_id,
            'tc': team_code
        }
        # Safely add the UIDs (up to 4)
        for i, uid in enumerate(uids[:4]):
            params[f'uid{i+1}'] = uid

        # Make the request to the bot running on Railway
        # This is where the connection error occurs
        api_url = f"{BOT_API_BASE_URL}:{BOT_API_PORT}/join"
        
        # Increased timeout slightly for external API
        response = requests.get(api_url, params=params, timeout=45) 
        
        # Raises an exception for 4xx or 5xx status codes
        response.raise_for_status() 

        return jsonify({
            'message': 'Emote request sent successfully to the bot!',
            'api_response': response.text # Use .text if the response is not guaranteed JSON
        }), 200

    except requests.exceptions.SSLError as e:
        # Catch the specific SSL error you were getting
        return jsonify({
            'message': 'SSL Connection Failed to Bot API. Check Bot API Firewall/SSL configuration.',
            'error_details': str(e)
        }), 502 # Bad Gateway

    except requests.exceptions.RequestException as e:
        # Catch all other requests errors (timeout, connection refused, etc.)
        return jsonify({
            'message': 'Error communicating with the external Bot API (e.g., Timeout, Connection Refused).',
            'error_details': str(e)
        }), 503 # Service Unavailable

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred on Vercel: {e}'}), 500

# Vercel automatically finds and runs the 'app' object.
# No need for app.run() or threading here.
