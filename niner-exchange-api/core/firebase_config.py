import os
import firebase_admin
from firebase_admin import credentials
from django.conf import settings

SERVICE_ACCOUNT_KEY_PATH = os.path.join(settings.BASE_DIR, 'firebase-service-account.json')

# Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK for Django Initialized.")