from rest_framework import generics, permissions
from core.models.review import Review
from core.serializers.review_serializer import (
    ReviewCreateSerializer,
    PopulatedReviewSerializer,
)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserReviewListView(generics.ListAPIView):
    serializer_class = PopulatedReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return (
            Review.objects.filter(reviewee_id=user_id)
            .select_related("reviewer")
            .order_by("-created_at")
        )
