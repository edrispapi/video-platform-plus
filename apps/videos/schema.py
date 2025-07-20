import graphene
from graphene_django import DjangoObjectType
from .models import Video, Comment
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")

class VideoType(DjangoObjectType):
    class Meta:
        model = Video
        fields = ("id", "title", "uploader", "likes", "created_at")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "video", "user", "text", "parent", "created_at")

class Query(graphene.ObjectType):
    videos = graphene.List(VideoType, query=graphene.String())
    video = graphene.Field(VideoType, id=graphene.Int())

    def resolve_videos(self, info, query=None):
        if query:
            return Video.objects.filter(title__icontains=query)
        return Video.objects.all()

    def resolve_video(self, info, id):
        return Video.objects.get(id=id)

class CreateVideo(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        file = graphene.String()  # مسیر فایل

    video = graphene.Field(VideoType)

    def mutate(self, info, title, file):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        video = Video(title=title, uploader=user, file=file)
        video.save()
        return CreateVideo(video=video)

class Mutation(graphene.ObjectType):
    create_video = CreateVideo.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
