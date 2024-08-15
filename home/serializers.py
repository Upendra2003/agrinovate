from rest_framework import serializers
from .models import SoilHealth

class SoilHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilHealth
        fields = ['date', 'soil_moisture','soil_temperature','nitrogen_content','phosphorus_content','potassium_content','soil_ph']