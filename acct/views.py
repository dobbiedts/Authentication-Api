from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .emails import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import logout
import datetime, jwt

from twilio.base.exceptions import TwilioRestException
# Create your views here.



class RegisterAPI(APIView):
    
    # permission_classes = [AllowAny ]
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                
                serializer.save(data)
                sendOtp(serializer.data['email'],serializer.data['phonenumber'])
                
                return Response({
                        'status' : 200,
                        'message': 'registration successful',
                        'data': serializer.data,
                    })
            else:
                return Response({
                    'status' : 200,
                    'message': 'registration failed',
                    'data': serializer.errors,
                    
                })
        except TwilioRestException as e:
            return Response({"i am here {e}".format(e=e)})
    def get_serializer_class(self):
            if not isinstance(self.serializer_classes, dict):
                raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
            if self.action in self.serializer_classes.keys():
                return self.serializer_classes[self.action]
            return super().get_serializer_class()
        
class LoginView(APIView):
    # permission_classes = [AllowAny ]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('user not found!')
        #incase, you don't have a a password to compare with, this helps validate password
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
          'id' : user.id,
          'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
          'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm= 'HS256')
        response = Response()
        #setting list jwt token to cookies
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt' : token
        }
        return response
    
        
class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)
            
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                          'status' : 400,
                          'message' : 'something went wrong' , 
                          'data' : 'invalid email'
                        }
                    )
                elif user[0].otp != otp:
                    return Response(
                        {
                          'status' : 400,
                          'message' : 'something went wrong' , 
                          'data' : 'wrong otp'
                        }
                    )
                user = user.first()
                user.is_verified = True
                user.save()
                
                return Response(
                        {
                          'status' : 400,
                          'message' : 'verification successful' , 
                          'data' : {}
                        }
                    )
            else:
                 return Response(
                        {
                          'status' : 400,
                          'message' : 'something went wrong' , 
                          'data' : serializer.errors  
                        })
        except Exception as e:
            print (e)
               
                    
class UserView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request,id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
    
        user = User.objects.get(id=id)
      
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class ListView(APIView):
    #  permission_classes = [IsAuthenticated]
     def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
    
        
        user = User.objects.all()
      
        serializer = UserSerializer(user, many= True)
        
        return Response(serializer.data)
    
class LogOut(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data= {
            'message' : 'Success'
        }
        return response
    
    
    
    
    
    
    
    
                        