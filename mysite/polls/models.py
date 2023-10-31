import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


# model은 models.Model을 상속받아야 한다.
class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    """
    [@admin.display 데코레이터에 대해]
    - boolean=True 옵션은 해당 필드가 boolean 값으로 표시되도록 지정
    - description='최근생성(하루기준)' 옵션은 메서드의 레이블을 지정
    - 모델 필드가 표시되는 방식을 사용자가 지정할 수 있도록 하는 기능을 제공
    """
    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        if self.was_published_recently():
            new_badge = '[new]'
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'


class Choice(models.Model):
    # Question 의 unique id 저장
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.question.question_text}] {self.choice_text}'