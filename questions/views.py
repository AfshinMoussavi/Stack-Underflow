from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from questions.forms import QuestionForm , TagForm , AnswerForm , SearchForm
from questions.models import Question, Answer, Tag
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden


@login_required
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)
    flag_update = request.user == question.user

    form = AnswerForm()
    context = {
        'question' : question , 
        'answers' : answers,
        'form' : form ,
        'flag_update':flag_update
    }
    return render(request , "question/question_detail_view.html" , context)


@login_required
def question_list_view(request):
    questions = Question.objects.all()
    context = {
        'questions' : questions
    }
    return render(request , 'question/question_list_view.html' , context)


@login_required
def question_update_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.user:
        flag_update = False
        return HttpResponseForbidden("You are not allowed to edit this question.")

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('questions:question_list')
    else:
        form = QuestionForm(instance=question)
    context = {
        'form': form,
        'question_id': question_id,

    }
    return render(request, 'question/question_form.html', context)


@login_required
def question_delete_view(request, question_id):
    question = get_object_or_404(Question , id=question_id)
    question.delete()
    return redirect('questions:question_list')


@login_required
def question_upvote_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.upvoters.filter(id=request.user.id).exists():
        question.upvoters.remove(request.user)
    else:
        if question.downvoters.filter(id=request.user.id).exists():
            question.downvoters.remove(request.user)
        question.upvoters.add(request.user)
    question.save()
    return redirect('questions:question_detail', question_id=question_id)


@login_required
def question_downvote_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.downvoters.filter(id=request.user.id).exists():
        question.downvoters.remove(request.user)
    else:
        if question.upvoters.filter(id=request.user.id).exists():
            question.upvoters.remove(request.user)
        question.downvoters.add(request.user)
    question.save()
    return redirect('questions:question_detail', question_id=question_id)


@login_required
def question_create_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()         
            return redirect('questions:question_list')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request , 'question/question_form.html' , context)


@login_required
def question_search_view(request):
    questions = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
             questions = Question.objects.filter(title = form.cleaned_data.get('query')) 
    else:
            form = SearchForm()
    context = {
        'form' : form , 
        'questions' : questions ,
    }
    return render(request , 'question/question_search.html' , context)


@login_required
def answer_create_view(request, question_id):
    question = get_object_or_404(Question , id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('questions:question_detail' , question_id = question_id)
    else:
        form = AnswerForm()
    context = {
        'form' : form , 
        'question' : question ,
    }
    
    return render(request , "question/question_detail_view.html" , context)


@login_required
def answer_update_view(request, answer_id):
    answer = get_object_or_404(Answer , id=answer_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST , instance=answer)
        if form.is_valid():
            form.save()
            return redirect('questions:question_detail' , question_id=answer.question.id)
    else:
        form = AnswerForm(instance = answer)
        
    context = {
        'form' : form , 
        'question' : answer.question , 
        'answer_id' : answer_id , 
    }
    return render(request , "question/question_detail_view.html" , context)


@login_required
def answer_delete_view(request, answer_id):
    answer = get_object_or_404(Answer  , id = answer_id) 
    answer.delete()
    return redirect('questions:question_list')


@login_required
def answer_upvote_view(request, answer_id):
    answer = get_object_or_404(Answer , id=answer_id)
    if answer.upvoters.filter(id=request.user.id).exists():
        answer.upvoters.remove(request.user)
    else:
        if answer.downvoters.filter(id=request.user.id).exists():
            answer.downvoters.remove(request.user)
        answer.upvoters.add(request.user)
    answer.save()
    return redirect('questions:question_detail',question_id = answer.question.id)


@login_required
def answer_downvote_view(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if answer.downvoters.filter(id=request.user.id).exists():
        answer.downvoters.remove(request.user)
    else:
        if answer.upvoters.filter(id=request.user.id).exists():
            answer.upvoters.remove(request.user)
        answer.downvoters.add(request.user)
    answer.save()
    return redirect('questions:question_detail', question_id=answer.question.id)



@login_required
def tag_list_view(request):
    tags = Tag.objects.all()
    context = {
        'tags' : tags
    }
    return render(request , 'tag/tag_list_view.html',context)


@login_required
def tag_create_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('questions:tag_list')
    else:
        form = TagForm()
        
    context = {
        'form' : form
    }
    return render(request , 'tag/create_tag_form.html', context)


@login_required
def tag_detail_view(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    questions = Question.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'questions': questions,
    }
    return render(request, 'tag/tag_detail_form.html', context)


def recent_questions_view(request):
    time_threshold = timezone.now() - timedelta(minutes=5)
    
    recent_questions = Question.objects.filter(created_at__gte=time_threshold)

    context = {
        'recent_questions': recent_questions
    }
    return render(request, 'home.html', context)