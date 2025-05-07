from django.shortcuts import render, redirect
from .models import Task
import pandas as pd
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction
from django.db import transaction


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def submit_task(request):
    if request.method == 'POST':
        with transaction.atomic():
            prompt = ' '.join(request.POST['prompt'].strip().split()).lower()
            response = ' '.join(request.POST['response'].strip().split()).lower()
            
            if Task.objects.filter(prompt__iexact=prompt).exists():
                messages.error(request, 'This prompt has already been submitted!')
                return render(request, 'tasks/submit_task.html', {'form_data': request.POST})
            
            if Task.objects.filter(response__iexact=response).exists():
                messages.error(request, 'This response has already been submitted!')
                return render(request, 'tasks/submit_task.html', {'form_data': request.POST})
            
            ip_address = get_client_ip(request)

            original_prompt = ' '.join(request.POST['prompt'].strip().split())
            original_response = ' '.join(request.POST['response'].strip().split())

            Task.objects.create(
                email=request.POST['email'],
                prompt=original_prompt,
                response=original_response,
                category=request.POST['category'],
                programming_language=request.POST['programming_language'],
                prompt_type=request.POST['prompt_type'],
                ip_address=ip_address
            )
            return redirect('success')
    return render(request, 'tasks/submit_task.html')

def success(request):
    return render(request, 'tasks/success.html')

@staff_member_required
def export_excel(request):
    tasks = Task.objects.all().values()
    df = pd.DataFrame(tasks)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tasks.xlsx"'
    df.to_excel(response, index=False)
    return response