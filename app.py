import os
import requests
import msal
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_access_token(tenant_id, client_id, client_secret):
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    scope = ['https://graph.microsoft.com/.default']

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )
    
    result = app.acquire_token_for_client(scopes=scope)
    
    if "access_token" in result:
        return result['access_token']
    else:
        raise Exception(f"Error obtaining access token: {result.get('error_description')}")

def send_email(tenant_id, client_id, client_secret, user_id, from_email, to, subject, body, cc=None, bcc=None, attachments=None):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "from": {"emailAddress": {"address": from_email}},
            "toRecipients": [{"emailAddress": {"address": to}}],
        },
        "saveToSentItems": "true"
    }

    if cc:
        email_data["message"]["ccRecipients"] = [{"emailAddress": {"address": addr}} for addr in cc]

    if bcc:
        email_data["message"]["bccRecipients"] = [{"emailAddress": {"address": addr}} for addr in bcc]

    if attachments:
        email_data["message"]["attachments"] = []
        for attachment in attachments:
            with open(attachment, "rb") as f:
                content_bytes = f.read()
                content_base64 = base64.b64encode(content_bytes).decode('utf-8')
            email_data["message"]["attachments"].append({
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": os.path.basename(attachment),
                "contentBytes": content_base64,
                "contentType": "application/octet-stream"
            })
    
    graph_api_endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'
    response = requests.post(graph_api_endpoint, headers=headers, json=email_data)
    
    if response.status_code == 202:
        return {"status": "Email sent successfully!"}
    else:
        return {"status": "Error", "details": response.text}, response.status_code

@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    data = request.json
    
    tenant_id = data.get('tenant_id')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    user_id = data.get('user_id')
    from_email = data.get('from_email')
    to = data.get('to')
    cc = data.get('cc')
    bcc = data.get('bcc')
    subject = data.get('subject')
    body = data.get('body')
    attachments = data.get('attachments')  # Optional list of file paths
    
    if not all([tenant_id, client_id, client_secret, user_id, from_email, to, subject, body]):
        return {"error": "Missing required parameters"}, 400
    
    try:
        result = send_email(tenant_id, client_id, client_secret, user_id, from_email, to, subject, body, cc, bcc, attachments)
        return jsonify(result)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
