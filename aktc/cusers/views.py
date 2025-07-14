# from django.shortcuts import render
# from django.contrib.auth.models import User
# from rest_framework import generics
# from .serializers import CUserserializer

# from rest_framework.permissions import IsAuthenticated


# class CUserDetailView(generics.RetrieveAPIView):
#     serializer_class = CUserserializer
#     permission_classes = [IsAuthenticated,]

#     def get_object(self):
#         return self.request.user

#     def get(self, request, *args, **kwargs):
#         print("User:", request.user)
#         print("Auth:", request.auth)
#         return self.retrieve(request, *args, **kwargs)
