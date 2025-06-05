import os
from pymongo import MongoClient
from datetime import datetime

# Get MongoDB connection string from environment variable
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/tally_subscribers')
client = MongoClient(mongo_uri)
db = client.get_database()

# Collections
subscribers = db.subscribers
form_submissions = db.form_submissions

def add_subscriber(email, name=None, data=None):
    """
    Add a new subscriber to the database
    """
    now = datetime.utcnow()
    subscriber = {
        'email': email,
        'name': name,
        'subscribed_at': now,
        'updated_at': now,
        'active': True,
        'data': data or {}
    }
    
    # Check if subscriber already exists
    existing = subscribers.find_one({'email': email})
    if existing:
        # Update existing subscriber
        subscribers.update_one(
            {'email': email},
            {'$set': {
                'name': name if name else existing.get('name'),
                'updated_at': now,
                'active': True,
                'data': {**existing.get('data', {}), **(data or {})}
            }}
        )
        return existing['_id']
    else:
        # Insert new subscriber
        result = subscribers.insert_one(subscriber)
        return result.inserted_id

def get_subscribers(active_only=True):
    """
    Get all subscribers
    """
    query = {'active': True} if active_only else {}
    return list(subscribers.find(query))

def unsubscribe(email):
    """
    Mark a subscriber as inactive
    """
    subscribers.update_one(
        {'email': email},
        {'$set': {'active': False, 'updated_at': datetime.utcnow()}}
    )

def save_form_submission(form_id, submission_data):
    """
    Save a form submission
    """
    submission = {
        'form_id': form_id,
        'submission_data': submission_data,
        'received_at': datetime.utcnow()
    }
    result = form_submissions.insert_one(submission)
    return result.inserted_id

def get_form_submissions(form_id=None):
    """
    Get form submissions
    """
    query = {'form_id': form_id} if form_id else {}
    return list(form_submissions.find(query))
