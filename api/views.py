from .models import User, URL
from .serializers import UserSerializer, URLSerializer, UserRegistrationSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ShortURLList(generics.ListAPIView):
    authentication_classes = [ JWTAuthentication]
    # , JWTAuthentication
    permission_classes = [IsAuthenticated]
    
    serializer_class = URLSerializer

    def get_queryset(self):
        return URL.objects.filter(user=self.request.user.id)


class URLRedirection(APIView):
    def get(self, request, pk):
        try:
            url_object = URL.objects.get(alias=pk)
            serializer = URLSerializer(url_object)
            return redirect(serializer.data.get('long'))
        except:
            return Response({'error':'alias not found'},status=status.HTTP_404_NOT_FOUND)
        


# The `urlAPI` class is an API view that handles POST requests to create a URL object with
# authentication and permission checks.
class urlAPI(APIView):
    authentication_classes = [ JWTAuthentication] #removed BasicAuthentication
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = {
            'alias': request.data.get('alias'),
            'long': request.data.get('long'),
            'user': request.user.id
        }
        serializer = URLSerializer(data=data)
        if serializer.is_valid():
            # Valid data, create and save the URL object
            url_object = serializer.save()
            serialized_data = URLSerializer(url_object).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            # Invalid data, return error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class URLUpdateDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        url_object = get_object_or_404(URL, alias=pk, user=request.user)
        serializer = URLSerializer(url_object)
        return Response(serializer.data)

    def put(self, request, pk):
        url_object = get_object_or_404(URL, alias=pk, user=request.user)
        data = {
        'alias': request.data.get('alias'),
        'long': request.data.get('long'),
        'user': request.user.id
        }
        serializer = URLSerializer(url_object, data=data)
        print(serializer)
        if serializer.is_valid():
            url_object.delete()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        url_object = get_object_or_404(URL, alias=pk, user=request.user)
        url_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)