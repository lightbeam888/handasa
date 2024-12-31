from rest_framework import serializers

from website.models import LocationMarker


class LocationMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMarker
        fields = '__all__'
