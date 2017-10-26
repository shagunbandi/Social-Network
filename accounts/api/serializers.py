from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, ValidationError, EmailField
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email address')
    email2 = EmailField(label='Confirm email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        data = self.initial_data()
        email1 = value
        email2 = data.get('email2')
        if email1 != email2:
            raise ValidationError('Emails must be same')
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Emails must be same')
        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError("This email id is already being used")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

