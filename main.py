# --- START OF FILE main.py (Final Code for Render Deployment) ---

# --- Imports from original main.py ---
import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# --- Imports needed for Flask API ---
from flask import Flask, request, jsonify
import os # Ensure os is imported for PORT environment variable check

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# ... (EMOTE_ALIASES and global variables remain the same) ...
EMOTE_ALIASES = {
    # Evo Gun Emotes
    "m10": 909000081, "ak": 909000063, "ump": 909000098, "mp40": 909000075,
    "mp40v2": 909040010, "scar": 909000068, "xm8": 909000085, "m10v": 909000081,
    # Normal Emotes
    "puffy": 909051014, "circle": 909050009, "petals": 909051013, "bow": 909051012,
    "motorbike": 909051010, "shower": 909051004, "bigdill": 909051001, "csgm": 909041013,
    "mapread": 909050014, "tomato": 909050015, "ninja": 909050002, "100lvl": 909042007,
    "auraboat": 909050028, "flyingguns": 909049012, "heart": 909000045, "pirate": 909000034,
    "pushup": 909000012, "devil": 909000020, "shootdance": 909000008, "chicken": 909000006
}

# --- Global Variables for Bot State (REQUIRED) ---
app = Flask(__name__)
# The list that your async loop populates with active connections
ONLINE_USERS = [] 
lock = threading.Lock()
# ... (Other global bot variables remain here) ...


# =================================================================
# ✅ FIX 1: Health Check Route (Stops Render returning 404 on base URL)
# =================================================================
@app.route('/', methods=['GET'])
def api_status():
    """Simple status check to confirm the API is running."""
    return jsonify({
        'status': 'Bot API is running', 
        'ready_for_route': '/join (POST)',
        'note': 'Use an external pinger service (like UptimeRobot) to keep this active 24/7 on Render.'
    }), 200


# =================================================================
# ✅ FIX 2 & 3: Corrected API Route for Vercel Proxy
# - Changed method from GET to POST
# - Changed data parsing from request.args.get() to request.form.get()
# =================================================================
@app.route('/join', methods=['POST'])
def join_team_route():
    try:
        # Use request.form.get() because Vercel sends POST data as form-encoded
        emote_id = request.form.get('emote_id') 
        team_code = request.form.get('tc')
        
        uids = []
        for i in range(1, 5):
            uid = request.form.get(f'uid{i}')
            if uid:
                uids.append(uid)
        
        if not all([emote_id, team_code, uids]):
             return jsonify({'message': 'Error: Missing required parameters (emote_id, tc, or uids).'}), 400

        # --- Your original bot logic starts here ---
        with lock:
            if not ONLINE_USERS:
                 return jsonify({'message': 'Error: Bot is connected to the server but no users are currently online to join a team with.'}), 503

            selected_conn = ONLINE_USERS[0] # Using the first online connection
            
        # The join_team function is assumed to be defined later in your file or imported
        response_msg = selected_conn.join_team(emote_id=emote_id, team_code=team_code, uids=uids)
        
        return jsonify({'message': 'Emote join request sent successfully to bot.', 'response': response_msg}), 200

    except Exception as e:
        print(f"Error in /join route: {e}")
        return jsonify({'message': f'Internal Server Error in Bot API: {e}'}), 500


# --- Bot Connection Class (Assuming it handles the join_team method) ---
class BotConnection:
    def __init__(self, loop, Target, ...):
        # ... (Your connection initialization code) ...
        self.loop = loop
        self.Target = Target
        # ...

    async def run(self):
        # ... (Your main connection loop) ...
        pass

    def join_team(self, emote_id, team_code, uids):
        # This function must be defined here to execute the packet logic 
        # (It's not provided in the snippet, so this is a placeholder)
        print(f"Executing join_team for Emote {emote_id}, Code {team_code}, UIDs {uids}")
        # Placeholder logic: you would dispatch the protobuf packet here.
        return f"Packet for Emote {emote_id} dispatched."
        

# --- Your main async functions (TcPOnLine, MainBot, etc. remain unchanged) ---
# ... (Keep all your TcPOnLine, MainBot, get_tcp_ports, etc. functions here) ...

# --- Main Execution Block (The part that runs the whole thing) ---
async def main():
    # ... (Your existing startup and variable setting code remains) ...

    # --- Your original async tasks ---
    task1 = asyncio.create_task(MainBot(Target, Pw, key, iv, AutHToKen, acc_name)) 
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    
    # --- This part remains the same: starting Flask in a new thread ---
    def run_flask():
        # =================================================================
        # ✅ FIX 4: Use Environment PORT Variable (MANDATORY for Render)
        # =================================================================
        # Render sets the port in the PORT environment variable.
        # This is the crucial part for deployment compatibility.
        port = int(os.environ.get('PORT', 30151)) 
        print(f"Starting Flask API on host 0.0.0.0, port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    os.system('clear')
    print("FIX_VERSION: Chat logic is now running a debug print check.") 
    print(render('WINTER', colors=['white', 'green'], align='center'))
    print('')
    print(f" - BoT STarTinG And OnLine on TarGeT : {TarGeT} | BOT NAME : {acc_name}\\n")
    print(f" - BoT sTaTus > GooD | OnLinE ! (:\")
    print(f" - Web UI and API started on port {port}")
    print(f" - API Example: POST to /join with form data.")
    print(f" - Subscribe > Spideerio | Gaming ! (:\")    
    await asyncio.gather(task1, task2) # This keeps your bot running 24/7 (if kept awake)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot Stopped by User.")
    except Exception as e:
        print(f"An unexpected error occurred in the main process: {e}")

# --- END OF FILE main.py ---
