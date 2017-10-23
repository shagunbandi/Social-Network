from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from comments.models import Comment


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'parent',
            'reply_count',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
            'reply_count',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        return obj.children().count()


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'replies',
            'reply_count',
            'timestamp',
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0