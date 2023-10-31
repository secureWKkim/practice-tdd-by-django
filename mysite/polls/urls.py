from django.urls import path
from . import views #views가 선언되지 않으면 오류가 남

app_name = 'polls'

"""
result는 파라미터가 있기 때문에 그냥 호출하는 것이 아니라 args=(parameter,)를 추가해서 호출한다.
꼭 parameter를 호출한 뒤 ,를 붙이는 걸 기억해 둔다.
"""
urlpatterns = [
    path('',views.index, name='index'),  #만약 requestURL이 없으면 views의 index에 간다.
    # path('some_url',views.some_url)
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/result/', views.result, name='result'),
]