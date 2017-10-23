from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post
from comments.models import Comment
from comments.api.serializers import CommentSerializer


link_to_post = HyperlinkedIdentityField(
    view_name='api-posts:detail',
    lookup_field='slug'
)


class PostListSerializer(ModelSerializer):
    url = link_to_post
    delete_url = HyperlinkedIdentityField(
        view_name='api-posts:delete',
        lookup_field='slug'
    )
    user = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'timestamp',
            'id',
            'delete_url',
        ]

    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api-posts:detail',
        lookup_field='slug'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='api-posts:delete',
        lookup_field='slug'
    )
    user = SerializerMethodField()
    image = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'slug',
            'content',
            'timestamp',
            'id',
            'delete_url',
            'image',
            'comments',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        # c_qs = Comment.objects.filter_by_instance(obj)
        c_qs = obj.comments
        comment = CommentSerializer(c_qs, many=True).data
        return comment


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'timestamp'
        ]