from rest_framework import serializers
from .models import MeetupLocation, Transaction, CustomUser, Listing, Category, Image


class MeetupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetupLocation
        fields = ['id', 'name', 'description', 'latitude', 'longitude']


class TransactionSerializer(serializers.ModelSerializer):
    buyer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    meetup_location = serializers.PrimaryKeyRelatedField(queryset=MeetupLocation.objects.all())

    class Meta:
        model = Transaction
        fields = [
            'id', 'buyer', 'seller', 'meetup_location', 'final_price', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context.get('request')
        buyer = attrs.get('buyer')
        seller = attrs.get('seller')
        if buyer == seller:
            raise serializers.ValidationError('Buyer and seller cannot be the same user.')
        # Ensure the initiator is part of the transaction
        if request and request.user.is_authenticated:
            if request.user != buyer and request.user != seller:
                raise serializers.ValidationError('You must be a participant (buyer or seller) to create this transaction.')
        return attrs

    def create(self, validated_data):
        # All newly created transactions start as PENDING
        validated_data['status'] = 'PENDING'
        return super().create(validated_data)


class TransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['status']

    def validate_status(self, value):
        if value not in ['PENDING', 'ACCEPTED', 'REJECTED', 'COMPLETED']:
            raise serializers.ValidationError('Invalid status value.')
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        instance: Transaction = self.instance
        new_status = attrs.get('status')
        if not instance:
            return attrs
        # Only participants can update status
        if request and request.user.is_authenticated:
            if request.user != instance.buyer and request.user != instance.seller:
                raise serializers.ValidationError('Only participants can update the transaction status.')
        # Basic transition rules
        allowed = {
            'PENDING': {'ACCEPTED', 'REJECTED'},
            'ACCEPTED': {'COMPLETED'},
            'REJECTED': set(),
            'COMPLETED': set(),
        }
        current = instance.status
        if new_status not in allowed.get(current, set()):
            raise serializers.ValidationError(f'Cannot change status from {current} to {new_status}.')
        return attrs

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'