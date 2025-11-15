import django_filters
from django.db.models import Q
from core.models.listing import Listing, PhysicalListing


# Used AI to help with the filtering logic
class ListingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_search", label="Search (title or description)"
    )
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    listing_type = django_filters.ChoiceFilter(
        field_name="listing_type", choices=Listing.LISTING_TYPE_CHOICES
    )
    listing_types = django_filters.CharFilter(method="filter_by_list")

    condition = django_filters.CharFilter(method="filter_by_list")
    price_new_min = django_filters.NumberFilter(
        field_name="physicallisting__price_new", lookup_expr="gte"
    )
    price_new_max = django_filters.NumberFilter(
        field_name="physicallisting__price_new", lookup_expr="lte"
    )

    course_code = django_filters.CharFilter(
        field_name="physicallisting__textbooklisting__course_code",
        lookup_expr="icontains",
    )

    property_types = django_filters.CharFilter(method="filter_by_list")

    bedrooms_min = django_filters.NumberFilter(
        field_name="sublease__number_of_bedrooms",
        lookup_expr="gte",
    )
    roommates_max = django_filters.NumberFilter(
        field_name="sublease__number_of_roommates",
        lookup_expr="lte",
    )
    distance_minutes_max = django_filters.NumberFilter(
        field_name="sublease__distance_from_campus_minutes",
        lookup_expr="lte",
    )
    start_date = django_filters.DateFilter(
        field_name="sublease__start_date",
        lookup_expr="gte",
    )
    end_date = django_filters.DateFilter(
        field_name="sublease__end_date",
        lookup_expr="lte",
    )

    class Meta:
        model = Listing
        fields = ["status"]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        ).distinct()

    def filter_by_list(self, queryset, name, value):
        values_list = [v.strip() for v in value.split(",") if v.strip()]
        if not values_list:
            return queryset

        if name == "condition":
            lookup = "physicallisting__condition__in"
        elif name == "listing_types":
            lookup = "listing_type__in"
        elif name == "property_types":
            lookup = "sublease__property_type__in"
        else:
            return queryset

        return queryset.filter(**{lookup: values_list}).distinct()
