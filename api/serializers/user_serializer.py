import uuid
from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import AgentDetail, UserProfile, User, Contact, StaffDetail
from project.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import authenticate
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]

    def validate_username(self, username):
        user_old = User.objects.filter(username=username).exists()
        if user_old:
            raise serializers.ValidationError("User already exists")
        return username

    def validate_email(self, email):
        email_old = User.objects.filter(email=email).exists()
        if email_old:
            raise serializers.ValidationError("Email already exists")
        return email
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs


class AgentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDetail
        fields = [
            "id",
            "user",
            "location",
            "identification_type",
            "identification_number",
            "identification_file",
            "accept_terms_and_condition",
        ]


class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    designation_display = serializers.CharField(
        source="get_designation_display", read_only=True
    )
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    information_display = serializers.CharField(
        source="get_information_display", read_only=True
    )
    # identification_image = serializers.ImageField(required=False)

    class Meta:
        model = StaffDetail
        fields = [
            "id",
            "user",
            "designation",
            "designation_display",
            "gender",
            "gender_display",
            "information",
            "information_display",
            "full_name",
            "phone_number",
            "address",
            "city",
            "state",
            "identification_number",
        ]

    

    @transaction.atomic
    def create(self, validated_data):
        # create user
        user = validated_data.pop("user")
        users = User.objects.create_user(
            username=user["username"], email=user["email"], password=user["password"]
        )
        StaffDetail.objects.create(
            user_id=users.id,
            designation=validated_data["designation"],
            gender=validated_data["gender"],
            information=validated_data["information"],
            full_name=validated_data["full_name"],
            phone_number=validated_data["phone_number"],
            address=validated_data["address"],
            city=validated_data["city"],
            state=validated_data["state"],
            identification_number=validated_data["identification_number"],
        )
        return True

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        # update the staff detail
        instance.designation = validated_data.get("designation", instance.designation)
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.information = validated_data.get("information", instance.information)
        instance.identification_number = validated_data.get(
            "identification_number", instance.identification_number
        )
        instance.identification_image = validated_data.get(
            "identification_image", instance.identification_image
        )
        instance.save()
        # update user
        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        read_only_fields = ["user.username"]
        model = UserProfile
        fields = ("id", "full_name", "user", "phone_number", "address")

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        ran_number = str(uuid.uuid1())[:4]
        ran_num_upper = ran_number[:2].upper() + ran_number[2:]
        send_mail(
            "Please Confirm Your Account",
            "Here is the message. {}".format(
                "Your 4 Digit Verification Pin" + str(ran_num_upper)
            ),
            user_data["email"],
            [EMAIL_HOST_USER],
            fail_silently=False,
        )
        user_profile = UserProfile.objects.create(
            user_id=user.id, otp_code=ran_num_upper, **validated_data
        )
        return user_profile

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        #UserProfile model
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('profile_picture', instance.address)
        instance.save()
        #User model
        user.email = user_data.get(
            'email',
            user.email
        )
        user.username = user_data.get(
            'username',
            user.username
         )
        user.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(
        max_length=50, required=True, write_only=True
    )
    password = serializers.CharField(max_length=50, required=True, write_only=True)


class ContactSerializer(serializers.ModelSerializer):
    """
    This view return details of contact
    """

    name = serializers.CharField(max_length=60)

    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "message")


class OtpSerializer(serializers.Serializer):
    """
    created when user register
    """

    otp_code = serializers.CharField(write_only=True, required=True)
    user_id = serializers.IntegerField(write_only=True, required=True)
