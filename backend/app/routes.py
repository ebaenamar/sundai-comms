from flask import Blueprint, request, jsonify, current_app, make_response
import hmac
import hashlib
import base64
import json
from app import db
from app.email_service import send_welcome_email, send_newsletter
import os

# Create blueprints
webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhook')
subscribers_bp = Blueprint('subscribers', __name__, url_prefix='/api/subscribers')
newsletter_bp = Blueprint('newsletter', __name__, url_prefix='/api/newsletter')

# Webhook route to receive Tally form submissions
@webhook_bp.route('/tally', methods=['POST'])
def tally_webhook():
    """
    Handle webhook from Tally forms
    """
    # Get the request data
    payload = request.json
    
    # Verify webhook signature if secret is set
    tally_signature = request.headers.get('tally-signature')
    webhook_secret = os.environ.get('TALLY_WEBHOOK_SECRET')
    
    if webhook_secret and tally_signature:
        # Calculate signature
        calculated_signature = base64.b64encode(
            hmac.new(
                webhook_secret.encode('utf-8'),
                json.dumps(payload).encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        # Compare signatures
        if tally_signature != calculated_signature:
            return jsonify({'error': 'Invalid signature'}), 401
    
    # Process the webhook data
    try:
        # Extract form data
        form_id = payload.get('data', {}).get('formId')
        form_name = payload.get('data', {}).get('formName')
        fields = payload.get('data', {}).get('fields', [])
        
        # Save the form submission
        db.save_form_submission(form_id, payload)
        
        # Extract email field
        email = None
        name = None
        data = {}
        
        for field in fields:
            field_type = field.get('type')
            field_label = field.get('label', '').lower()
            field_value = field.get('value')
            
            # Store all fields in data dictionary
            data[field_label] = field_value
            
            # Look for email field
            if field_type == 'INPUT_EMAIL':
                email = field_value
            
            # Look for name field
            elif field_label in ['name', 'full name', 'first name']:
                name = field_value
        
        # If we found an email, add the subscriber
        if email:
            db.add_subscriber(email, name, data)
            # Send welcome email
            send_welcome_email(email, name)
            
        return jsonify({'success': True, 'message': 'Webhook processed successfully'}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error processing webhook: {e}")
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

# Subscribers routes
@subscribers_bp.route('/', methods=['GET', 'OPTIONS'])
def get_all_subscribers():
    """
    Get all subscribers
    """
    if request.method == 'OPTIONS':
        # Responder a la solicitud preflight
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Max-Age', '86400')  # 24 horas
        return response
        
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        subscribers = db.get_subscribers(active_only=active_only)
        response = jsonify(subscribers)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        current_app.logger.error(f'Error getting subscribers: {str(e)}')
        error_response = jsonify({'error': 'Internal server error'})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500   
        return response
    except Exception as e:
        current_app.logger.error(f'Error getting subscribers: {str(e)}')
        error_response = jsonify({'error': 'Internal server error'})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

@subscribers_bp.route('/unsubscribe', methods=['POST', 'OPTIONS'])
def unsubscribe():
    """
    Unsubscribe a user
    """
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    db.unsubscribe(email)
    return jsonify({'success': True})

# Newsletter routes
@newsletter_bp.route('/send', methods=['POST'])
def send_newsletter_route():
    """
    Send a newsletter to all active subscribers
    """
    data = request.json
    subject = data.get('subject')
    content = data.get('content')
    
    if not subject or not content:
        return jsonify({'error': 'Subject and content are required'}), 400
    
    # Get all active subscribers
    subscribers = db.get_subscribers(active_only=True)
    recipient_emails = [sub['email'] for sub in subscribers]
    
    if not recipient_emails:
        return jsonify({'error': 'No active subscribers found'}), 400
    
    # Send the newsletter
    success = send_newsletter(subject, content, recipient_emails)
    
    if success:
        return jsonify({'success': True, 'recipients_count': len(recipient_emails)})
    else:
        return jsonify({'error': 'Failed to send newsletter'}), 500
