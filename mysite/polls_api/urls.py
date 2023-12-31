from django.urls import path,include
from .views import *

# 1. METHOD로 구현
"""
urlpatterns = [
    path('question/', question_list, name='question-list'),
    path('question/<int:id>/', question_detail, name='question-detail'),
]
"""


# 2. CLASS로 구현
"""
urlpatterns = [
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:id>/', QuestionDetail.as_view(), name='question-detail'),
]
"""


# 3. mixins을 통해 구현
urlpatterns = [ # QuestionDetail을 호출할 때 pk인 id가 필요
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('users/', UserList.as_view(),name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('register/', RegisterUser.as_view()),
    path('api-auth/', include('rest_framework.urls'))
]