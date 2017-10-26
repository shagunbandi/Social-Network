from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, ValidationError
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from accounts.api.serializers import UserDetailSerializer

User = get_user_model()


def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError('this content type does not exist')
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError('no such slug for the provided content type')
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            if user:
                main_user = user
            else:
                main_user = User.objects.first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type, slug, content, main_user,
                parent_obj=parent_obj
            )
            return comment

    return CommentCreateSerializer


def get_children_count(obj):
    return obj.children().count()


def get_children_count_total(obj):
    return obj.total_children_count()


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    reply_total = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'parent',
            'reply_count',
            'reply_total',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        return get_children_count(obj)

    def get_reply_total(self, obj):
        return get_children_count_total(obj)


class CommentListSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    reply_total = SerializerMethodField()
    replies = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)
    url = HyperlinkedIdentityField(
        view_name='api-comments:detail'
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'reply_count',
            'reply_total',
            'replies',
            'timestamp',
            'url'
        ]

    def get_reply_count(self, obj):
        return get_children_count(obj)

    def get_reply_total(self, obj):
        return get_children_count_total(obj)

    def get_replies(self, obj):
        try:
            return CommentChildSerializer(obj.children(), many=True).data
        except:
            return None


class CommentUpdateSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]


class CommentChildSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    reply_total = SerializerMethodField()
    replies = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'reply_count',
            'reply_total',
            'replies'
        ]

    def get_reply_count(self, obj):
        return get_children_count(obj)

    def get_reply_total(self, obj):
        return get_children_count_total(obj)


    def get_replies(self, obj):
        try:
            return CommentChildSerializer(obj.children(), many=True).data
        except:
            return None


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    reply_total = SerializerMethodField()
    content_obj_url = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content_type',
            'object_id',
            'content',
            'timestamp',
            'content_obj_url',
            'reply_count',
            'reply_total',
            'replies'
        ]
        read_only_fields = [
            'reply_count',
            'reply_total',
            'replies'
        ]

    def get_content_obj_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        try:
            return CommentChildSerializer(obj.children(), many=True).data
        except:
            return None

    def get_reply_count(self, obj):
        return get_children_count(obj)

    def get_reply_total(self, obj):
        return get_children_count_total(obj)

