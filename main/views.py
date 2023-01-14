from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as dj_login
from .forms import *


@csrf_exempt
def main(request):
    form = LoginForm(request.POST or None)
    if request.is_ajax():
        if form.is_valid():
            if form.cleaned_data["username"] in Group.objects.values_list("username", flat=True):
                group = Group.objects.get(username=form.cleaned_data["username"])
                if form.cleaned_data["password"] == group.password:
                    group = dj_login(request, group)
                    return JsonResponse({'ok': True})
                else:
                    return JsonResponse({'ok': False, "description": "همچین گروهی نداریم!"})
            else:
                return JsonResponse({'ok': False, "description": "همچین گروهی نداریم!"})
        else:
            return JsonResponse({'ok': False, "description": "فرم رو درست وارد کن!"})
    context = {
        'form': form,
        'groups': Group.objects.order_by('-score')
    }
    return render(request, "main.html", context=context)


@csrf_exempt
def question(request):
    form = QuestionForm(request.POST or None, request.FILES or None)
    if request.is_ajax():
        if form.is_valid():
            step = request.user.step
            question = Question.objects.get(sort_number=step)
            if form.cleaned_data["answer"] == "next":
                if not question.is_question:
                    group = Group.objects.get(id=request.user.id)
                    group.step = group.step + 1
                    group.save()
                    return JsonResponse({'ok': True})
            elif form.cleaned_data["answer"] == question.answer:
                group = Group.objects.get(id=request.user.id)
                group.score = group.score + 10
                group.step = group.step + 1
                group.save()
                Answer.objects.create(group=group, text=form.cleaned_data["answer"], score=10)
                return JsonResponse({'score': group.score, 'ok': True, 'true_answer': True, "description": "آفرین! 10 امتیاز به گروهتون اضافه شد، بریم مرحله بعدی"})
            else:
                group = Group.objects.get(id=request.user.id)
                group.score = group.score - 5
                group.save()
                Answer.objects.create(group=group, text=form.cleaned_data["answer"], score=-5)
                return JsonResponse({'score': group.score, 'ok': True, 'true_answer': False, "description": "اوه اشتباه جواب دادید، متاسفانه 5 امتیاز از گروهتون کم شد"})
        else:
            return JsonResponse({'ok': False, "description": "فرم رو درست وارد کن!"})
    if request.user.is_authenticated:
        step = request.user.step
        if step == 13:
            return redirect('/')
        else:
            question = Question.objects.get(sort_number=step)
    else:
        return redirect('/')
    context = {
        'form': form,
        'question': question,
    }
    return render(request, "question.html", context=context)