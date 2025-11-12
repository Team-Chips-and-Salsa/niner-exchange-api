import django_filters
from core.models.listing import Listing, PhysicalListing


class ListingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_search", label="Search (title or description)"
    )

    # Filter by minimum price (price__gte: greater than or equal)
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    # Filter by maximum price (price__lte: less than or equal)
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    # Filter by listing type using the model's choices
    listing_type = django_filters.ChoiceFilter(
        field_name="listing_type", choices=Listing.LISTING_TYPE_CHOICES
    )

    condition = django_filters.ChoiceFilter(
        field_name="condition", choices=PhysicalListing.CONDITIONS
    )

    class Meta:
        model = Listing
        # Fields for exact filtering
        fields = [
            "status",
            "listing_type",
            "condition",
        ]

    def filter_search(self, queryset, name, value):
        from django.db.models import Q

        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
