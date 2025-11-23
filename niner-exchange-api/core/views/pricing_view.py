from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  
from rest_framework.response import Response
from rest_framework import status
from ..services.ebay_browse import get_average_listing_price

EBAY_CONDITION_NEW = [1000]
EBAY_CONDITION_OPEN_BOX = [1500]
EBAY_CONDITION_USED = [3000]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_price(request):
    title = request.data.get("title")
    condition = request.data.get("condition")

    if not title:
        return Response(
            {"error": "Title is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    response_data = {}

    price_new = get_average_listing_price(title, EBAY_CONDITION_NEW)
    response_data["median_price_new"] = price_new

    if condition == "LIKE_NEW":
        price_open_box = get_average_listing_price(title, EBAY_CONDITION_OPEN_BOX)
        response_data["median_price_open_box"] = price_open_box
    else:
        price_used = get_average_listing_price(title, EBAY_CONDITION_USED)
        response_data["median_price_used"] = price_used

    return Response(response_data, status=status.HTTP_200_OK)
