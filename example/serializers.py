from rest_framework import serializers

class VisitorName(serializers.Serializer):
    visitor_name = serializers.CharField(max_length=255)