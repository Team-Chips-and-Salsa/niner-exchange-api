# Used AI to implement eBay API tokens and responses

import requests
import statistics
from django.core.cache import cache
from .ebay_auth import get_ebay_application_token

EBAY_BROWSE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
BROWSE_CACHE_DURATION = 1800  # Cache results for 30 minutes


def get_average_listing_price(query, condition_ids):
    if not isinstance(condition_ids, list) or not condition_ids:
        print("Error: condition_ids must be a non-empty list.")
        return None

    # Generate cache key based on query and conditions
    conditions_str = "|".join(
        map(str, sorted(condition_ids))
    )  # Ensure consistent order
    cache_key = f'ebay_browse_{query.lower().replace(" ", "_")}_{conditions_str}'

    cached_price = cache.get(cache_key)
    if cached_price is not None:
        return cached_price

    token = get_ebay_application_token()
    if not token:
        print("Error: Could not get eBay token for Browse API call.")
        return None

    headers = {"Authorization": f"Bearer {token}"}

    # Format filter string correctly: conditionIds:{id1}|{id2}
    filter_value = "|".join(map(str, condition_ids))
    filter_string = f"conditionIds:{{{filter_value}}}"

    # Smart exclusion: Exclude accessory keywords unless they are part of the user's query
    accessory_keywords = [
        "case", "cover", "box", "screen", "protector", "skin", "sticker", "decal",
        "cable", "charger", "adapter", "part", "replacement", "battery", "manual",
        "stand", "mount", "holder", "fan", "cooler", "strap", "band",
        "dummy", "fake", "prop", "display", "lens", "frame", "assembly",
        "headphone", "headset", "earpod", "earbud"
    ]
    
    query_words = set(query.lower().split())
    exclusions = [word for word in accessory_keywords if word not in query_words]
    
    refined_query = query
    if exclusions:
        refined_query += " -" + " -".join(exclusions)

    params = {"q": refined_query, "filter": filter_string, "limit": 50}

    prices = []
    try:
        response = requests.get(
            EBAY_BROWSE_URL, headers=headers, params=params, timeout=15
        )  # Added timeout
        response.raise_for_status()
        data = response.json()

        items = data.get("itemSummaries", [])
        if not items:
            # Cache the fact that no items were found (cache None)
            cache.set(cache_key, None, timeout=BROWSE_CACHE_DURATION)
            return None

        for item in items:
            try:
                price_str = item.get("price", {}).get("value")
                if price_str:
                    prices.append(float(price_str))
            except (ValueError, TypeError):
                # Ignore items with invalid price format
                continue

        if not prices:
            cache.set(cache_key, None, timeout=BROWSE_CACHE_DURATION)
            return None

        # 1. First, remove extreme upper outliers using IQR (e.g. $25,000 item)
        # We do this BEFORE gap detection so the gap detection isn't skewed by one massive outlier
        if len(prices) > 4:
            sorted_prices = sorted(prices)
            q1 = sorted_prices[len(sorted_prices) // 4]
            q3 = sorted_prices[3 * len(sorted_prices) // 4]
            iqr = q3 - q1
            upper_bound = q3 + 1.5 * iqr
            
            # Filter out upper outliers
            prices = [p for p in sorted_prices if p <= upper_bound]
            if not prices:
                prices = sorted_prices

        # 2. Filter out low-price accessories using a "Significant Gap" heuristic
        sorted_prices = sorted(prices)
        cutoff_index = 0
        for i in range(len(sorted_prices) - 1):
            current_price = sorted_prices[i]
            next_price = sorted_prices[i+1]
            
            # Relaxed gap: > 2x price AND > $50 difference
            # This catches the jump from "Parts/Broken" ($300) to "Used/Refurb" ($700)
            if next_price > current_price * 2 and (next_price - current_price) > 50:
                cutoff_index = i + 1
                break 
        
        # Keep only the prices from the high-value cluster
        final_prices = sorted_prices[cutoff_index:]

        # Calculate median price
        median_price = round(statistics.median(final_prices), 2)
        cache.set(cache_key, median_price, timeout=BROWSE_CACHE_DURATION)
        return median_price

    except requests.exceptions.HTTPError as e:
        print(
            f"HTTP Error fetching eBay listings for {cache_key}: {e.response.status_code} - {e.response.text}"
        )
        # Cache None on error to prevent hammering the API
        cache.set(cache_key, None, timeout=600)  # Cache error result for 10 min
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network Error fetching eBay listings for {cache_key}: {e}")
        return None  # Return None, don't cache
    except Exception as e:
        print(f"An unexpected error occurred during listing fetch for {cache_key}: {e}")
        return None  # Return None, don't cache
