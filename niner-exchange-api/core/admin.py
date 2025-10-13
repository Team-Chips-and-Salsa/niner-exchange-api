from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MeetupLocation, Transaction, Category, Listing, Image

class CustomUserAdmin(UserAdmin):
    """
    Admin for CustomUser.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role', 'status')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_image_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role', 'status')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )

@admin.register(MeetupLocation)
class MeetupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'meetup_location', 'final_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'buyer__email', 'seller__email')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('listing_id', 'seller', 'category_id', 'title', 'condition', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'condition', 'category_id')
    search_fields = ('title', 'description')

admin.site.register(CustomUser, CustomUserAdmin)
# Need to register Image
admin.site.register(Category)