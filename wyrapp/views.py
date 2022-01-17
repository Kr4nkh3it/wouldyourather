from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice
import random

# Create your views here.

def index(request):
    questionid=0
    if len(Question.objects.all()) >= 1:
        question = random.choice(Question.objects.all())
        questionid=question.id
    question = get_object_or_404(Question,pk=questionid)
    return render(request,'wyrapp/index.html',{'question':question})

def choose(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'wyrapp/choose.html',{'question':question,'choice0':question.choice_set.all()[0],'choice1':question.choice_set.all()[1]})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'wyrapp/choose.html',{'question':question,'error_message': "You didn't select a choice"})
    else:
        selected_choice.results += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('wyrapp:results',args=(question.id,)))
    
def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    next_question = question
    questionid=0
    results0 = round((question.choice_set.all()[0].results/(question.choice_set.all()[0].results+question.choice_set.all()[1].results))*100)
    results1 = round((question.choice_set.all()[1].results/(question.choice_set.all()[1].results+question.choice_set.all()[0].results))*100)
    if len(Question.objects.all()) > 1:
        while next_question == question:
            next_question = random.choice(Question.objects.all())
            questionid=next_question.id
        next_question = Question.objects.get(pk=questionid)
    else:
        return render(request, 'wyrapp/results.html',{'question':question,'next_question':question,'results0':results0,'results1':results1,'error_message':'There are no more questions'})
    return render(request, 'wyrapp/results.html',{'question':question,'next_question':next_question,'results0':results0,'results1':results1})

