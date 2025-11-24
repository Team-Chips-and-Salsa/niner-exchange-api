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
from core.models.meetup_location import MeetupLocation
from core.serializers.meetup_location_serializer import MeetupLocationSerializer


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
                target_object.is_verified_student = False
                target_object.save()
            elif isinstance(target_object, Review):
                target_object.status = "INACTIVE"
                target_object.save()

class MeetupLocationCreateView(generics.CreateAPIView):
    queryset = MeetupLocation.objects.all().order_by('name')
    serializer_class = MeetupLocationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class MeetupLocationListView(MeetupLocationListView):
    permission_classes = [permissions.IsAuthenticated, isAdminUser]

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, isAdminUser]

class MeetupLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeetupLocation.objects.all()
    serializer_class = MeetupLocationSerializer
    permission_classes = [permissions.IsAuthenticated, isAdminUser]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
