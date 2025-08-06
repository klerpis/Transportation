from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer



# NOTE: The permission_classes are removed to allow the view to handle both
# authenticated and unauthenticated requests gracefully within the get() method.

class UserProfileAPIView(APIView):
    """
    A view that provides user details (username, names, email) and
    the user's profile data.
    It handles both authenticated and unauthenticated requests.
    """
    # def get(self, request):
    #     serializer = ProfileSerializer(request.user.profile)
    #     return Response(serializer.data)


    def get(self, request):
        """
        Retrieves and returns user and profile data for an authenticated user.
        If the user is not authenticated, a 401 Unauthorized response is returned.
        """
        # A try-catch block is a good practice for handling potential errors,
        # but the primary logic here is checking for authentication status first.
        try:
            # Check if the user is authenticated before proceeding.
            # This replaces the need for the `permission_classes` attribute.
            user = request.user

            if user.is_authenticated:
                profile_serializer = ProfileSerializer(user.profile)
                # --- Step 1: Extract details from the default User model ---
                # We can access the user object directly from the request.
                
                # Create a dictionary with the specific user details you need.
                user_details = {
                    # 'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }
                
                # --- Step 2: Extract details from the Profile model ---
                # The Profile is connected to the user with the field 'user'.
                # We get the profile object and serialize it.
                # profile_serializer = ProfileSerializer(user.profile)

                # --- Step 3: Combine both sets of data into a single response ---
                # This merges the user_details dictionary with the profile data.
                response_data = {
                    **profile_serializer.data,
                    **user_details,
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # If the user is not authenticated, return a custom 401 response.
                # This directly addresses the "catch unauthenticated users" part of the request.
                user_details = {
                    # 'username': '',
                    'firstname': '',
                    'lastname': '',
                    'email': '',
                }
                # response_data = {
                #     **user_details,
                # }
                return Response(user_details, status=status.HTTP_200_OK)
                # return Response(
                #     {'detail': 'Authentication credentials were not provided.'},
                #     status=status.HTTP_401_UNAUTHORIZED
                # )
        except Exception as e:
            # Catch any other potential errors, such as a missing profile,
            # and return a 500 server error response.
            return Response(
                {'detail': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def put(self, request):
        serializer = ProfileSerializer(
            request.user.profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print()
        print(f"ONEEE")
        print()

        return Response(serializer.data)
