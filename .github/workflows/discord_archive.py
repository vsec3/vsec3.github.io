import requests
import json
import datetime
import os

AUTHORIZATION = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Discord Chat Archive</title>
    <style>
        :root {{
            --dark-primary: #36393f;
            --dark-secondary: #2f3136;
            --text-normal: #dcddde;
            --text-muted: #72767d;
            --interactive-hover: #32353b;
        }}
        body {{
            background-color: var(--dark-primary);
            color: var(--text-normal);
            font-family: 'Whitney', 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .message {{
            padding: 10px;
            margin: 5px 0;
            display: flex;
            align-items: flex-start;
        }}
        .message:hover {{
            background-color: var(--interactive-hover);
        }}
        .avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 16px;
        }}
        .message-content {{
            flex: 1;
        }}
        .username {{
            color: white;
            font-weight: 500;
            margin-right: 8px;
        }}
        .timestamp {{
            color: var(--text-muted);
            font-size: 0.8em;
        }}
        .content {{
            margin-top: 4px;
            white-space: pre-wrap;
        }}
        .attachment {{
            max-width: 400px;
            margin-top: 8px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div id="messages">
        {messages}
    </div>
</body>
</html>
'''

MESSAGE_TEMPLATE = '''
<div class="message">
    <img class="avatar" src="{avatar_url}" alt="">
    <div class="message-content">
        <div class="username">{username}</div>
        <span class="timestamp">{timestamp}</span>
        <div class="content">{content}</div>
        {attachments}
    </div>
</div>
'''

def get_messages(channel_id, before_id=None, limit=100):
    headers = {
        "Authorization": AUTHORIZATION,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
    if before_id:
        url += f"&before={before_id}"
        
    response = requests.get(url, headers=headers)
    return response.json()

def save_chat_history():
    all_messages = []
    last_id = None
    
    while True:
        messages = get_messages(CHANNEL_ID, last_id)
        if not messages:
            break
            
        all_messages.extend(messages)
        last_id = messages[-1]["id"]
        print(f"Fetched {len(all_messages)} messages...")
        
    all_messages.reverse()
    message_html = ""
    
    for msg in all_messages:
        timestamp = datetime.datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        attachments_html = ""
        for attachment in msg.get("attachments", []):
            if attachment.get("content_type", "").startswith("image/"):
                attachments_html += f'<img class="attachment" src="{attachment["url"]}" alt="Attachment">'
        
        message_html += MESSAGE_TEMPLATE.format(
            avatar_url=f"https://cdn.discordapp.com/avatars/{msg['author']['id']}/{msg['author']['avatar']}.webp",
            username=msg["author"]["username"],
            timestamp=formatted_time,
            content=msg["content"],
            attachments=attachments_html
        )
    
    html_content = HTML_TEMPLATE.format(messages=message_html)
    
    # Change output path for GitHub Pages
    output_path = "docs/discord_archive.html"
    os.makedirs("docs", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Successfully saved {len(all_messages)} messages to {output_path}")

if __name__ == "__main__":
    save_chat_history()