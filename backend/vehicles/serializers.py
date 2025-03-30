from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vehicle, FuelRecord, ServiceRecord
import logging

logger = logging.getLogger('vehicles.serializers')

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class FuelRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_internal_value(self, data):
        logger.info(f"to_internal_value called with data: {data}")
        try:
            # Calculate total_cost before validation
            if 'gallons' in data and 'cost_per_gallon' in data:
                gallons = float(data['gallons'])
                cost_per_gallon = float(data['cost_per_gallon'])
                data['total_cost'] = gallons * cost_per_gallon
                logger.info(f"Calculated total cost in to_internal_value: {data['total_cost']}")
            
            internal_value = super().to_internal_value(data)
            logger.info(f"Converted to internal value: {internal_value}")
            return internal_value
        except Exception as e:
            logger.error(f"Error in to_internal_value: {str(e)}")
            raise

    def validate(self, data):
        logger.info(f"validate called with data: {data}")
        try:
            # Ensure total_cost exists and is correct
            if 'gallons' in data and 'cost_per_gallon' in data:
                gallons = float(data['gallons'])
                cost_per_gallon = float(data['cost_per_gallon'])
                data['total_cost'] = gallons * cost_per_gallon
                logger.info(f"Calculated total cost in validate: {data['total_cost']}")
            return data
        except Exception as e:
            logger.error(f"Error in validate: {str(e)}")
            raise serializers.ValidationError(f"Error calculating total cost: {str(e)}")

    def create(self, validated_data):
        logger.info(f"create called with validated_data: {validated_data}")
        try:
            # Final check to ensure total_cost exists
            if 'gallons' in validated_data and 'cost_per_gallon' in validated_data:
                gallons = float(validated_data['gallons'])
                cost_per_gallon = float(validated_data['cost_per_gallon'])
                validated_data['total_cost'] = gallons * cost_per_gallon
                logger.info(f"Calculated total cost for creation: {validated_data['total_cost']}")
            return super().create(validated_data)
        except Exception as e:
            logger.error(f"Error in create: {str(e)}")
            raise serializers.ValidationError(f"Error creating fuel record: {str(e)}")

class ServiceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        logger.info(f"Validating service record data: {data}")
        return data

    def create(self, validated_data):
        logger.info(f"Creating service record with data: {validated_data}")
        try:
            return super().create(validated_data)
        except Exception as e:
            logger.error(f"Error in ServiceRecordSerializer.create: {str(e)}")
            raise serializers.ValidationError(f"Error creating service record: {str(e)}")

class VehicleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    fuel_records = FuelRecordSerializer(many=True, read_only=True)
    service_records = ServiceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at') 