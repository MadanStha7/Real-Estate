import uuid
from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import AgentDetail, UserProfile, Contact, StaffDetail, AdminProfile
from project.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.core.exceptions import ValidationError


class UsernameValidator(object):
    """
    validate the username and check if it already exist in add and update method
    """

    def set_context(self, serializer_field):
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.parent, "instance", None)
        if not self.instance:
            # try to get user from other model:
            root_instance = getattr(serializer_field.root, "instance", None)
            self.instance = getattr(root_instance, "user", None)

    def __call__(self, value):
        if (
            self.instance
            and User.objects.filter(username=value)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise ValidationError("Username already exists.")
        if not self.instance and User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")


class EmailValidator(object):
    """
    validate the email and check if it already exist in add and update method
    """

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.parent, "instance", None)
        if not self.instance:
            # try to get user from other model:
            root_instance = getattr(serializer_field.root, "instance", None)
            self.instance = getattr(root_instance, "user", None)

    def __call__(self, value):
        if (
            self.instance
            and User.objects.filter(email=value).exclude(id=self.instance.id).exists()
        ):
            raise ValidationError("Email already exists.")

        if not self.instance and User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if "data:" in data and ";base64," in data:
                # Break out the header from the base64 content
                header, data = data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, validators=[UsernameValidator()])
    email = serializers.CharField(required=True, validators=[EmailValidator()])
    password = serializers.CharField(write_only=True, min_length=6, max_length=68)
    password2 = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=68,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]

    def validate(self, attrs):
        print("attrs", attrs)
        if self.context.get("request") == "POST":
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."}
                )
        return attrs


class AgentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    identification_type = serializers.CharField(required=False)
    identification_number = serializers.CharField(required=False)

    class Meta:
        model = AgentDetail
        fields = [
            "id",
            "user",
            "location",
            "phone_number",
            "identification_type",
            "identification_number",
            "identification_file",
            "accept_terms_and_condition",
        ]

    @transaction.atomic
    def create(self, validated_data):
        # create user
        user = validated_data.pop("user")
        print("user", user)
        users = User.objects.create_user(
            username=user["username"], email=user["email"], password=user["password"]
        )
        AgentDetail.objects.create(user_id=users.id, **validated_data)
        return True


class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    designation_display = serializers.CharField(
        source="get_designation_display", read_only=True
    )
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    information_display = serializers.CharField(
        source="get_information_display", read_only=True
    )
    state_display = serializers.CharField(source="get_state_display", read_only=True)

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
            "state_display",
            "state",
            "identification_number",
            "identification_image",
        ]

    @transaction.atomic
    def create(self, validated_data):
        # create user
        user = validated_data.pop("user")
        users = User.objects.create_user(
            username=user["username"], email=user["email"], password=user["password"]
        )
        StaffDetail.objects.create(user_id=users.id, **validated_data)
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
        userSerializer = UserSerializer(user, data=user_data, partial=True)
        if userSerializer.is_valid(raise_exception=True):
            userSerializer.save()
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
        model = UserProfile
        fields = (
            "id",
            "full_name",
            "user",
            "phone_number",
            "address",
            "profile_picture",
        )

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(
            username=user_data["email"],
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
            EMAIL_HOST_USER,
            [user_data["email"]],
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
        # UserProfile model
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.address = validated_data.get("profile_picture", instance.address)
        instance.save()
        # User model
        user.email = user_data.get("email", user.email)
        user.username = user_data.get("username", user.username)
        user.save()
        return instance


class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdminProfile
        fields = ["id", "user", "full_name", "image", "phone"]

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(
            username=user_data["email"],
            email=user_data["email"],
            password=user_data["password"],
        )
        admin_profile = AdminProfile.objects.create(user_id=user.id, **validated_data)
        return admin_profile

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        userSerializer = UserSerializer(user, data=user_data, partial=True)
        if userSerializer.is_valid(raise_exception=True):
            userSerializer.save()
        # Update Admin data
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.image = validated_data.get("image", instance.image)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
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
        fields = ("id", "name", "email", "phone", "message")


class OtpSerializer(serializers.Serializer):
    """
    created when user register
    """

    otp_code = serializers.CharField(write_only=True, required=True)
    user_id = serializers.IntegerField(write_only=True, required=True)

class AgentSearchSerializer(serializers.ModelSerializer):

    class Meta:

        model = AgentDetail
        fields = ("user", "location", "full_name", "phone_number", "identification_type", "identification_number","identification_file", "accept_terms_and_condition", "added_at", "is_verified")





