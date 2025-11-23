from rest_framework import permissions, generics
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import isAdminUser
from core.models.report import Report
from core.models.listing import Listing
from core.models.review import Review
from core.models.user import CustomUser
from django.contrib.contenttypes.models import ContentType
from core.serializers.report_serializer import ReportSerializer, ReportStatusSerializer
from core.serializers.content_type_serializer import ContentTypeSerializer
from core.serializers.user_serializer import UserSerializer
from core.views.meetup_location_view import MeetupLocationListView


class ContentTypeView(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class FlaggedReportView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, isAdminUser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type', 'status', 'reason']

class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

class FlaggedReportStatusUpdateView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportStatusSerializer
    permission_classes = [permissions.IsAuthenticated, isAdminUser]
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        report = serializer.save()
        
        reports = Report.objects.filter(
            content_type = report.content_type,
            object_id = report.object_id,
            status = "PENDING",
        )
        
        if report.status == "APPROVED":
            target_object = report.content_object
            for r in reports:
                r.status = "APPROVED"
                r.save()
            
            if isinstance(target_object, Listing):
                target_object.status = "REMOVE"
                target_object.save()
            elif isinstance(target_object, CustomUser):
                target_object.status = "suspended"
                target_object.save()
            elif isinstance(target_object, Review):
                target_object.status = "INACTIVE"
                target_object.save()

class ExchangeZonesView(MeetupLocationListView):
    permission_classes = [permissions.IsAuthenticated, isAdminUser]

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, isAdminUser]
    