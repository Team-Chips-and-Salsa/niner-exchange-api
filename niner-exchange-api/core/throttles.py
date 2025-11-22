from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ListingCreationThrottle(UserRateThrottle):
    scope = 'listing_creation'

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
            
        return super().allow_request(request, view)
    
class AuthThrottle(AnonRateThrottle):
    scope = 'auth_attempts'