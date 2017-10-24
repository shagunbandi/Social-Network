from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
    # def all(self):
    #     qs = super(CommentManager, self).filter(parent=None)
    #     return qs

    def filter_by_instance(self, instance):
        # TODO understand __class__ thingy
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
        return qs

    def filter_if_parent(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first()
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_upvotes')
    objects = CommentManager()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_upvotes_url(self):
        return reverse('posts:comments:upvote-toggle', kwargs={'pk': self.pk, 'slug': self.content_object.slug})

    def get_api_upvotes_url(self):
        return reverse('posts:comments:upvote-toggle-api', kwargs={'pk': self.pk, 'slug': self.content_object.slug})

    def has_upvoted(self, user):
        print(self.upvotes.all())
        if user in self.upvotes.all():
            return True
        return False

