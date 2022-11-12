from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .services import get_client_ip
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from .serializers import CustomUserSerializer, RegisterSerializer
from django.contrib.auth import login
from django.http import StreamingHttpResponse
from .services import open_file


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        super(LoginAPI, self).post(request, format=None)
        return Response({
            "user": CustomUserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class MovieListView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
