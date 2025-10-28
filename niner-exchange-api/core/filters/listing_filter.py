import django_filters
from core.models.listing import Listing


class ListingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_search", label="Search (title or description)"
    )

    category_id = django_filters.UUIDFilter(field_name="category__category_id")

    # Filter by condition (exact match)
    condition = django_filters.ChoiceFilter(choices=Listing.CONDITIONS)

    # Filter by minimum price (price__gte: greater than or equal)
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    # Filter by maximum price (price__lte: less than or equal)
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Listing
        # Fields for exact filtering
        fields = [
            "category_id",
            "condition",
            "status",
        ]

    def filter_search(self, queryset, name, value):
        from django.db.models import Q

        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
