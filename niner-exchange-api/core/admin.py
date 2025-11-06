from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models.listing import Listing, ItemListing, TextbookListing, Sublease, Service
from core.models.meetup_location import MeetupLocation
from core.models.transaction import Transaction
from core.models.user import CustomUser
from core.models.image import Image


class CustomUserAdmin(UserAdmin):
    """
    Admin for CustomUser.
    """

    list_display = ("email", "first_name", "last_name", "is_staff", "role", "status")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "profile_image_url")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                    "status",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2"),
            },
        ),
    )


@admin.register(MeetupLocation)
class MeetupLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer",
        "seller",
        "meetup_location",
        "final_price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("id", "buyer__email", "seller__email")


admin.site.register(CustomUser, CustomUserAdmin)


# Register Listing models
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "listing_id",
        "title",
        "seller",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "seller__email")


@admin.register(ItemListing)
class ItemListingAdmin(admin.ModelAdmin):
    list_display = (
        "listing_id",
        "title",
        "seller",
        "condition",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "condition", "created_at")
    search_fields = ("title", "description", "seller__email")


@admin.register(TextbookListing)
class TextbookListingAdmin(admin.ModelAdmin):
    list_display = (
        "listing_id",
        "title",
        "seller",
        "course_code",
        "condition",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "condition", "created_at")
    search_fields = ("title", "description", "course_code", "seller__email")


@admin.register(Sublease)
class SubleaseAdmin(admin.ModelAdmin):
    list_display = (
        "listing_id",
        "title",
        "seller",
        "property_type",
        "start_date",
        "end_date",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "property_type", "created_at")
    search_fields = ("title", "description", "seller__email")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "listing_id",
        "title",
        "seller",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "seller__email")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image_id", "listing", "upload_order")
    list_filter = ("upload_order",)
