from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Vehicle, FuelRecord, ServiceRecord
from .serializers import VehicleSerializer, FuelRecordSerializer, ServiceRecordSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
import logging

User = get_user_model()
logger = logging.getLogger('vehicles.views')

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        logger.info(f"Creating vehicle with data: {serializer.validated_data}")
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            logger.error(f"Error creating vehicle: {str(e)}")
            raise

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        try:
            vehicle = self.get_object()
            fuel_records = FuelRecordSerializer(vehicle.fuel_records.all(), many=True).data
            service_records = ServiceRecordSerializer(vehicle.service_records.all(), many=True).data
            
            # Combine and sort all records by date
            timeline = []
            for record in fuel_records:
                timeline.append({
                    'type': 'fuel',
                    'date': record['date'],
                    'data': record
                })
            for record in service_records:
                timeline.append({
                    'type': 'service',
                    'date': record['date'],
                    'data': record
                })
            
            timeline.sort(key=lambda x: x['date'], reverse=True)
            return Response(timeline)
        except Exception as e:
            logger.error(f"Error getting timeline: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        try:
            vehicle = self.get_object()
            
            # Calculate fuel efficiency
            fuel_records = vehicle.fuel_records.all()
            total_miles = 0
            total_gallons = 0
            total_cost = 0
            
            for i in range(len(fuel_records) - 1):
                miles = fuel_records[i].mileage - fuel_records[i + 1].mileage
                gallons = fuel_records[i].gallons
                total_miles += miles
                total_gallons += gallons
                total_cost += fuel_records[i].total_cost
            
            mpg = total_miles / total_gallons if total_gallons > 0 else 0
            
            # Get recent service records
            recent_services = ServiceRecordSerializer(
                vehicle.service_records.all()[:5],
                many=True
            ).data
            
            return Response({
                'fuel_efficiency': {
                    'mpg': round(mpg, 2),
                    'total_cost': total_cost,
                    'total_miles': total_miles,
                    'total_gallons': total_gallons
                },
                'recent_services': recent_services
            })
        except Exception as e:
            logger.error(f"Error getting dashboard: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FuelRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FuelRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FuelRecord.objects.filter(vehicle_id=self.kwargs['vehicle_pk'])

    def create(self, request, *args, **kwargs):
        logger.info(f"create view called with request data: {request.data}")
        logger.info(f"URL kwargs: {kwargs}")

         # Ensure vehicle ID is included in the request data
        vehicle_id = self.kwargs['vehicle_pk']
        request.data['vehicle'] = vehicle_id  # Add vehicle ID to the request data


        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in create view: {str(e)}")
            raise

    def perform_create(self, serializer):
        logger.info(f"perform_create called with validated_data: {serializer.validated_data}")
        logger.info(f"Vehicle ID from URL: {self.kwargs['vehicle_pk']}")
        try:
            instance = serializer.save(vehicle_id=self.kwargs['vehicle_pk'])
            logger.info(f"Successfully created fuel record: {instance.id}")
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            logger.error(f"Full error details: {e.__dict__}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            # Update vehicle's current mileage if this record has the highest mileage
            vehicle = instance.vehicle
            if instance.mileage > vehicle.current_mileage:
                vehicle.current_mileage = instance.mileage
                vehicle.save()
        except Exception as e:
            logger.error(f"Error updating fuel record: {str(e)}")
            raise

class ServiceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceRecord.objects.filter(vehicle_id=self.kwargs['vehicle_pk'])


    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            # Update vehicle's current mileage if this record has the highest mileage
            vehicle = instance.vehicle
            if instance.mileage > vehicle.current_mileage:
                vehicle.current_mileage = instance.mileage
                vehicle.save()
        except Exception as e:
            logger.error(f"Error updating service record: {str(e)}")
            raise

    def perform_create(self, serializer):
        logger.info(f"Creating service record with data: {serializer.validated_data}")
        
        # Ensure vehicle ID is included in the validated data
        vehicle_id = self.kwargs['vehicle_pk']
        
        # Retrieve the Vehicle instance
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        serializer.validated_data['vehicle'] = vehicle  # Assign the Vehicle instance

        try:
            serializer.save(vehicle=vehicle)  # Save the ServiceRecord with the Vehicle instance
            logger.info(f"Successfully created service record for vehicle ID: {vehicle_id}")
        except Exception as e:
            logger.error(f"Error creating service record: {str(e)}")
            logger.error(f"Full error details: {e.__dict__}")
            raise
        except serializers.ValidationError as ve:
            logger.error(f"Validation error: {ve.detail}")
            raise

    def create(self, request, *args, **kwargs):
        # Ensure vehicle ID is included in the request data
        vehicle_id = self.kwargs['vehicle_pk']
        request.data['vehicle'] = vehicle_id  # Add vehicle ID to the request data
        
        logger.info(f"ServiceRecord create called with request data: {request.data}")
        logger.info(f"URL kwargs: {kwargs}")
        return super().create(request, *args, **kwargs)

class LoginView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # First try to find user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If not found by username, try email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return Response(
                    {'error': 'No active account found with the given credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        # Authenticate with the found user's username
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
