from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice
import random

# Create your views here.

def index(request):
    question_list = Question.objects.all()
    return render(request,'wyrapp/index.html',{'question':random.choice(question_list)})

def choose(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_list = []
    for choice in question.choice_set.all():
        choice_list.append(choice)
    return render(request,'wyrapp/choose.html',{'question':question,'choice1':choice_list[0],'choice2':choice_list[1]})

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
    question_list = Question.objects.all()
    random_question = random.choice(question_list)
    question = get_object_or_404(Question,pk=question_id)
    choice_list = []
    for choice in question.choice_set.all():
        choice_list.append(choice)
    while random_question == question:
        random_question = random.choice(question_list)
    results1 = str(int(round((choice_list[0].results / (choice_list[0].results + choice_list[1].results)) * 100)))+"%"
    results2 = str(int(round((choice_list[1].results / (choice_list[0].results + choice_list[1].results)) * 100)))+"%"
    return render(request, 'wyrapp/results.html',{'question':question,'random_question':random_question,'results1':results1,'results2':results2})

