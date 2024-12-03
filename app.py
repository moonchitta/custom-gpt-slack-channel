from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Slack Bot Token from .env file
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN is not set in the .env file")

client = WebClient(token=SLACK_BOT_TOKEN)

@app.route('/list_channels', methods=['GET'])
def list_channels():
    """
    List all Slack channels.
    """
    try:
        response = client.conversations_list(types="public_channel,private_channel")
        channels = response.get("channels", [])
        return jsonify({"ok": True, "channels": [{"id": ch["id"], "name": ch["name"]} for ch in channels]})
    except SlackApiError as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# Topic Endpoints
@app.route('/get_channel_topic', methods=['GET'])
def get_channel_topic():
    """
    Get the topic of a channel.
    Query Param: channel_id
    """
    channel_id = request.args.get('channel_id')
    if not channel_id:
        return jsonify({"ok": False, "error": "channel_id is required"}), 400

    try:
        response = client.conversations_info(channel=channel_id)
        topic = response.get("channel", {}).get("topic", {}).get("value", "No topic set")
        return jsonify({"ok": True, "topic": topic})
    except SlackApiError as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/update_channel_topic', methods=['POST'])
def update_channel_topic():
    """
    Update the topic of a channel.
    JSON Body: { "channel_id": "C12345678", "topic": "New topic" }
    """
    data = request.json
    channel_id = data.get("channel_id")
    topic = data.get("topic")

    if not channel_id or not topic:
        return jsonify({"ok": False, "error": "channel_id and topic are required"}), 400

    try:
        client.conversations_setTopic(channel=channel_id, topic=topic)
        return jsonify({"ok": True, "message": "Channel topic updated successfully"})
    except SlackApiError as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# Purpose Endpoints
@app.route('/get_channel_purpose', methods=['GET'])
def get_channel_purpose():
    """
    Get the purpose of a channel.
    Query Param: channel_id
    """
    channel_id = request.args.get('channel_id')
    if not channel_id:
        return jsonify({"ok": False, "error": "channel_id is required"}), 400

    try:
        response = client.conversations_info(channel=channel_id)
        purpose = response.get("channel", {}).get("purpose", {}).get("value", "No purpose set")
        return jsonify({"ok": True, "purpose": purpose})
    except SlackApiError as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/update_channel_purpose', methods=['POST'])
def update_channel_purpose():
    """
    Update the purpose of a channel.
    JSON Body: { "channel_id": "C12345678", "purpose": "New purpose" }
    """
    data = request.json
    channel_id = data.get("channel_id")
    purpose = data.get("purpose")

    if not channel_id or not purpose:
        return jsonify({"ok": False, "error": "channel_id and purpose are required"}), 400

    try:
        client.conversations_setPurpose(channel=channel_id, purpose=purpose)
        return jsonify({"ok": True, "message": "Channel purpose updated successfully"})
    except SlackApiError as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
