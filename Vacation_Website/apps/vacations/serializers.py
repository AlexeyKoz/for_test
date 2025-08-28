# Serializers for vacations, likes, and countries in the vacations app.
from rest_framework import serializers
from .models import Vacation, Like
from apps.core.models import Country

# Serializer for the Country model.
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

# Serializer for the Vacation model.
class VacationSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Vacation
        fields = [
            'id', 'country', 'country_name', 'description',
            'start_date', 'end_date', 'price', 'image',
            'is_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    # Get whether the vacation is liked by the current user.
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False

# Serializer for the Like model.
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user',)
