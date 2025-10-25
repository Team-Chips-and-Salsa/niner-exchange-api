# Used AI to implement eBay API tokens and responses

import requests
import base64
import time
import os
from django.core.cache import cache


EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
TOKEN_CACHE_KEY = "ebay_application_token"
CACHE_TIMEOUT_BUFFER = 120  # Refresh token 2 minutes before actual expiry


def get_ebay_application_token():
    cached_token_info = cache.get(TOKEN_CACHE_KEY)

    if cached_token_info and cached_token_info["expires_at"] > time.time():
        return cached_token_info["token"]

    if not EBAY_CLIENT_ID or not EBAY_CLIENT_SECRET:
        print("Error: eBay Client ID or Secret not configured.")
        return None

    credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}",
    }
    body = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }

    try:
        response = requests.post(EBAY_TOKEN_URL, headers=headers, data=body, timeout=10)
        response.raise_for_status()

        data = response.json()
        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 7200)

        if access_token:
            expires_at = time.time() + expires_in - CACHE_TIMEOUT_BUFFER
            token_info = {"token": access_token, "expires_at": expires_at}
            # Cache the new token with its expiry time
            cache.set(TOKEN_CACHE_KEY, token_info, timeout=(expires_at - time.time()))
            return access_token
        else:
            print(f"Error: Could not retrieve access token from eBay. Response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching eBay token: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during token fetch: {e}")
        return None
