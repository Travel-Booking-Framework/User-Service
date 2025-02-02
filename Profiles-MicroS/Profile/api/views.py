from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Profile.models import UserProfile, UserBankInfo
from Profile.api.serializers import UserProfileSerializer, UserBankInfoSerializer
from Profile.services.user_profile_service import UserProfileService
from Profile.services.user_bank_service import UserBankInfoService


class UserProfileView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = UserProfileService.create_user_profile(serializer.validated_data)
            return Response(UserProfileSerializer(user_profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            user_profile = UserProfileService.update_user_profile(user_profile, serializer.validated_data)
            return Response(UserProfileSerializer(user_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            UserProfileService.delete_user_profile(user_profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)


class UserBankInfoView(APIView):
    def post(self, request):
        serializer = UserBankInfoSerializer(data=request.data)
        if serializer.is_valid():
            user_bank_info = UserBankInfoService.create_user_bank_info(serializer.validated_data)
            return Response(UserBankInfoSerializer(user_bank_info).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user_bank_info = UserBankInfo.objects.get(pk=pk)
        except UserBankInfo.DoesNotExist:
            return Response({"error": "UserBankInfo not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserBankInfoSerializer(user_bank_info, data=request.data, partial=True)
        if serializer.is_valid():
            user_bank_info = UserBankInfoService.update_user_bank_info(user_bank_info, serializer.validated_data)
            return Response(UserBankInfoSerializer(user_bank_info).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user_bank_info = UserBankInfo.objects.get(pk=pk)
            UserBankInfoService.delete_user_bank_info(user_bank_info)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserBankInfo.DoesNotExist:
            return Response({"error": "UserBankInfo not found"}, status=status.HTTP_404_NOT_FOUND)


# Profile queries
class ProfileLists(APIView):
    """
    Retrieve all user profiles
    """
    def get(self, request):
        profiles = UserProfileService.get_all_profiles()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetails(APIView):
    def get(self, request, national_code):
        profile = UserProfileService.get_profile_by_national_code(national_code)
        if profile:
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)


# BankInfo queries
class BankInfoLists(APIView):
    """
    Retrieve all user bank infos
    """
    def get(self, request):
        bank_infos = UserBankInfoService.get_all_bank_infos()  # داده‌ها از سرویس گرفته می‌شود
        serializer = UserBankInfoSerializer(bank_infos, many=True)  # سریالایز داده‌ها
        return Response(serializer.data, status=status.HTTP_200_OK)


class BankInfoDetails(APIView):
    def get(self, request, card_number):
        bank_info = UserBankInfoService.get_bank_info_by_card_number(card_number)
        if bank_info:
            serializer = UserBankInfoSerializer(bank_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "UserBankInfo not found"}, status=status.HTTP_404_NOT_FOUND)