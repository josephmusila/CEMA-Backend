# health_info/views.py
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from .models import HealthProgram, Client, Enrollment
from .serializers import HealthProgramSerializer, ClientSerializer, EnrollmentSerializer,DoctorRegisterSerializer
from .permissions import IsDoctor

class DoctorRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = DoctorRegisterSerializer

    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     token, _ = Token.objects.get_or_create(user=user)
    #     self.token = token

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     response.data = {"token": self.token.key}
    #     return response

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        email = request.data.get('email')
        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        user.groups.add(doctor_group)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class HealthProgramCreateListView(generics.ListCreateAPIView):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer
   

class ClientCreateListView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['first_name', 'last_name']

class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
   

class ClientProfileView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
   