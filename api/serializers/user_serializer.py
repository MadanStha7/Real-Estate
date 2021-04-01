from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import AgentDetail, UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "user", "profile_picture", "phone_number", "address"]


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


class ChangePasswordSerializer(serializers.Serializer):
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


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    created when user register
    """
    full_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            # "user",
            "email",
            "username",
            "password",
            "password2",
            # "is_active",
        )

    def create(self, validated_data):
        # user = get_user_model(**validated_data)
        # user.set_password(validated_data['password'])
        # user.save()
        full_name = validated_data.pop("full_name")
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        print("email", email)
        print("username", username)
        print("password", password)
        print("password", full_name)

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        print("user", user.id)
        profile = UserProfile.objects.create(user_id=user.id, full_name=full_name)
        return profile

    def validate(self, attrs):
        print(attrs, "===attrs")
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

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

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
