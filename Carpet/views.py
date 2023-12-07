from django.shortcuts import render

# Create your views here.
# views.py
from dj_rest_auth.views import UserDetailsView
from rest_framework.response import Response

class CustomUserDetailsView(UserDetailsView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'first_name':user.first_name,
            'last_name':user.last_name,
           
        }
        return Response(data)
