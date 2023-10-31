# polls(호출한 app) views.py에 url 호출 시 보여 줄 화면 구현
from .models import *
# template으로 그려 주기 위해서 render 메서드 사용
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5] # pub_date를 역순으로 정렬을 해서 다섯 개를 가지고 온다.
    context = {'first_question': latest_question_list}
    # context = {'questions': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    """
    # 404는 워낙 자주 발생하는 에러라 shortcuts 모듈 내에 아래와 같이 편한 메서드 제공.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': f"선택이 없습니다. id={request.POST['choice']}"})
    else:
        # A서버에서도 Votes = 1, B서버에서도 Votes = 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # return HttpResponseRedirect(reverse('polls:index'))
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
    

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})