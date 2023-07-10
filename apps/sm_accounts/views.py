from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.sm_accounts.models import ValidateEmail

from utils.permissions import CustomPermission
from utils.helpers import get_hashed_otp
from utils.swgr_doc_schmas import *

from apps.sm_users.serializers import UserSerializer, UserProfileSerializer, ProfileImageSerializer

import utils.smtp as smtp
import random

from drf_yasg.utils import swagger_auto_schema


class UserSignup(APIView):

    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        security=[],
        tags=SignupSchema.get_tag(),
        operation_id=SignupSchema.get_operation_id(),
        operation_summary=SignupSchema.get_opration_summary(),
        operation_description = SignupSchema.get_operation_description(),
        manual_parameters = SignupSchema.get_manual_parameters(),
        consumes= SignupSchema.get_consumes(),
        responses = SignupSchema.get_responses()
    )
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # Email Validation
                if User.objects.filter(email=request.data['email']).exists():
                    return Response({'detail': 'A user with that email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Create User
                serializer.save()
                
                # Password hashing
                user = User.objects.get(username=request.data['username'])
                user.set_password(request.data['password'])
                user.save()
                
                # Upload image
                data = {'user': user.id}
                
                if 'image' in request.data:
                    data['image'] = request.data['image']

                profile_img_serilizer = ProfileImageSerializer(data=data)
                if profile_img_serilizer.is_valid():
                    profile_img_serilizer.save()
                
                # Create token
                token = Token.objects.create(user=user)
                
                # Create email entry
                validate_obj = ValidateEmail.objects.create(user_id=user.id)
                
                # Auth user details
                user_data = UserProfileSerializer(user).data
                return Response({'token': token.key, 'data': user_data, 'detail': 'User created successfuly.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogin(APIView):

    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        security=[],
        tags=LoginSchema.get_tag(),
        operation_id=LoginSchema.get_operation_id(),
        operation_summary=LoginSchema.get_opration_summary(),
        operation_description = LoginSchema.get_operation_description(), 
        manual_parameters = LoginSchema.get_manual_parameters(),
        responses = LoginSchema.get_responses()
    )
    def post(self, request):
        # Use get_object_or_404() to return an object, or raise an Http404 exception if the object does not exist.
        user = get_object_or_404(User, username=request.data['username'])
        
        # Validating username and password
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        
        # Generate Token for auth user
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserProfileSerializer(user).data
        message = 'User login successful'
        
        # Email verification check
        if not ValidateEmail.objects.get(user_id=user.id).is_verified:
            message = 'User email is not verified, please verify your email.'
        return Response({'token': token.key, 'data': user_data, 'detail': message}, status=status.HTTP_200_OK)


class UserLogout(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=LogOutSchema.get_tag(),
        operation_id=LogOutSchema.get_operation_id(),
        operation_summary=LogOutSchema.get_opration_summary(),
        operation_description = LogOutSchema.get_operation_description(),
        responses = LogOutSchema.get_responses()
    )
    def get(self, request):
        try:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            user.auth_token.delete()
            return Response("Successful logout", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestToken(APIView):
    
    permission_classes = [CustomPermission]

    @swagger_auto_schema(
        tags=TestTokenSchema.get_tag(),
        operation_id=TestTokenSchema.get_operation_id(),
        operation_summary=TestTokenSchema.get_opration_summary(),
        operation_description = TestTokenSchema.get_operation_description(),
        responses = TestTokenSchema.get_responses()
    )
    def get(self, request):
        return Response("Valid Token", status=status.HTTP_200_OK)
    

class GenerateOTP(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=GenerateOTPSchema.get_tag(),
        operation_id=GenerateOTPSchema.get_operation_id(),
        operation_summary=GenerateOTPSchema.get_opration_summary(),
        operation_description = GenerateOTPSchema.get_operation_description(),
        responses = GenerateOTPSchema.get_responses()
    )
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            otp = random.randint(4000, 8000)
            otp_hasned = get_hashed_otp(str(otp))
            if not ValidateEmail.objects.filter(user_id=user.id).exists():
                ValidateEmail.objects.create(user_id=user.id)
            verify_email_obj = ValidateEmail.objects.get(user_id=user.id)
            if verify_email_obj.is_verified and verify_email_obj.is_active:
                return Response({'detail': 'User email already verified.'}, status=status.HTTP_200_OK)
            else:
                verify_email_obj.otp = otp_hasned
                verify_email_obj.save()
                smtp.send_mail(user_name=user.username, otp=otp)
                return Response({'detail': 'OTP generated and sent successfully to given email.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTP(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=VerifyOTPSchema.get_tag(),
        operation_id=VerifyOTPSchema.get_operation_id(),
        operation_summary=VerifyOTPSchema.get_opration_summary(),
        operation_description = VerifyOTPSchema.get_operation_description(),
        manual_parameters = VerifyOTPSchema.get_manual_parameters(),
        responses = VerifyOTPSchema.get_responses()
    )
    def post(self, request):
        try:
            otp = request.data['otp']
            otp_hasned = get_hashed_otp(str(otp))
            validate_email_obj = ValidateEmail.objects.get(user_id=request.user.id)
            if validate_email_obj.is_verified:
                message = 'User already verified.'
                return Response({'detail': message}, status=status.HTTP_200_OK)
            elif validate_email_obj.otp == otp_hasned:
                validate_email_obj.is_verified = True
                validate_email_obj.is_active = True
                validate_email_obj.save()
                message = 'Email verification successful.'
                return Response({'detail': message}, status=status.HTTP_200_OK)
            else:
                message = 'Please enter valid otp'
                return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
