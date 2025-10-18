from rest_framework import generics, permissions

from core.models.category import Category
from core.serializers.category_serializer import CategorySerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]