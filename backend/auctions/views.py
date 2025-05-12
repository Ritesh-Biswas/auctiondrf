from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        is_admin = user.is_superuser or user.groups.filter(name='MP_Admin').exists()
        return Response({
            'success': True,
            'username': user.username,
            'is_admin': is_admin
        })
    return Response({
        'success': False,
        'message': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)