from django.shortcuts import render, get_object_or_404
from polls.models import Question
from polls_api.serializers import QuestionSerializer, UserSerializer, RegisterSerializer
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, mixins, generics, permissions
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly


# 1. METHOD로 구현
"""
@api_view(['GET', 'POST']) 
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many = True)
        #serializer를 여러 개 줄 때는 many 옵션을 줘 serializer 해야 하는 게 여러 개임을 인식하게 해 준다.
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        # 새로 serialize된 데이터를 저장할 시 유효성 검사를 해줘야 함
        if serializer.is_valid():
            serializer.save()
            # 그냥 200보다 자세한 상태 코드 반환
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# @api_view(['GET','POST']) #괄호 안을 비우면 get 명령을 처리함
@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request):
    question = get_object_or_404(Question, pk=id)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""



# 2. CLASS로 구현
"""
class QuestionList(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    def get(self, request, id):
        question = get_object_or_404(Question, pk=id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, id):
        question = get_object_or_404(Question, pk=id)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        question = get_object_or_404(Question, pk=id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""



# 3. mixins을 통해 구현
# 다른 방식들에 비해 훨씬 더 간결
# 자체 기능이 존재하기 때문에 여러 값을 가지고 올 때는 .list, 하나의 값을 가지고 올 때는 .retrieve,
# 새로 만들 때는 .create, 수정할 때는 .update, 마지막으로 삭제할 때는 .destroy를 쓰면 된다.
"""
class QuestionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class QuestionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""



# 4. generics를 통해 구현
# 가장 간단한 코드로 구현된다.
#  get, put, delete를 하지 않아도 RetrieveUpdateDestroyAPIView나 ListCreateAPIView 내부에 모두 구현되어 있기 때문
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer