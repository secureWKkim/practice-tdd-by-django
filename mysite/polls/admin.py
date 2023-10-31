from django.contrib import admin
from .models import Choice, Question

# Register your models here.
admin.site.register(Choice)

"""
Question의 커스터마이징 class에 inlines를 사용해 준다.
inlines으로 들어갈 부분도 동일하게 class를 생성해 주는데 인자로 layout을 설정할 수 있다.
(StackedInline : 세로로 배치, TabularInline : 가로로 배치)
model과 extra를 설정해 줄 수 있는데 이때 extra는 몇 개를 추가할 수 있게 할 것이냐는 설정이다.
"""

# 이 클래스를 활용하면 Question 모델을 편집하면서 Choice 모델도 함께 편집할 수 있다.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # classes를 통해 visibility를 설정
    # collapse 클래스가 적용된 생성일(pub_date)는 필드의 내용을 감추거나 보일 수 있는 옵션이 존재
    fieldsets = [
        ('질문 섹션', {'fields': ['question_text']}),
        ('생성일', {'fields': ['pub_date'], 'classes': ['collapse']}),        
    ]
    # 목록에 보여 주고 싶은 model의 column을 설정
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # pub_date는 auto_now_add = True(이미 자동으로 추가가 되도록 설정해 둠) 처리했기 때문에 그냥 데이터를 받으면 오류가 발생=> readonly로 설정
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]

    # 필터(검색) 기능
    list_filter = ['pub_date']  # 날짜 필터 기능으로, 장고에서 자체 제공하는 기능.
    search_fields = ['question_text', 'choice__choice_text']  # 검색어 입력이 필요한 요소들

admin.site.register(Question, QuestionAdmin)