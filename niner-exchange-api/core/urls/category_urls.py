from django.urls import path

from core.views.category_view import CategoryListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name="category-view-all")
]