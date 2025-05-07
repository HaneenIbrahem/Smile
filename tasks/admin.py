from django.contrib import admin
from django.http import HttpResponse
from .models import Task
import pandas as pd
from django import forms
from django.shortcuts import render, redirect
from django.urls import path, reverse

class ExportExcelForm(forms.Form):
    PROMPT_TYPES = [('all', 'All')] + list(Task.PROMPT_TYPES)
    LANGUAGES = [('all', 'All')] + list(Task.LANGUAGES)
    CATEGORIES = [('all', 'All')] + list(Task.CATEGORIES)

    prompt_type = forms.MultipleChoiceField(
        choices=PROMPT_TYPES[1:],
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        help_text="Hold Ctrl/Cmd to select multiple options"
    )
    programming_language = forms.MultipleChoiceField(
        choices=LANGUAGES[1:],
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        help_text="Hold Ctrl/Cmd to select multiple options"
    )
    category = forms.MultipleChoiceField(
        choices=CATEGORIES[1:],
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        help_text="Hold Ctrl/Cmd to select multiple options"
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('email', 'category', 'programming_language', 'prompt_type', 'ip_address', 'created_at')
    list_filter = ('category', 'programming_language', 'prompt_type', 'ip_address')
    search_fields = ('email', 'prompt', 'ip_address')
    readonly_fields = ('ip_address',)
    date_hierarchy = 'created_at'
    actions = ['export_selected_to_excel']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('export-excel/', self.export_excel_view, name='task_export_excel'),
        ]
        return my_urls + urls

    def export_excel_view(self, request):
        if request.method == 'POST':
            form = ExportExcelForm(request.POST)
            if form.is_valid():
                prompt_types = form.cleaned_data['prompt_type']
                programming_languages = form.cleaned_data['programming_language']
                categories = form.cleaned_data['category']

                queryset = Task.objects.all()

                if prompt_types:
                    queryset = queryset.filter(prompt_type__in=prompt_types)
                if programming_languages:
                    queryset = queryset.filter(programming_language__in=programming_languages)
                if categories:
                    queryset = queryset.filter(category__in=categories)

                data = queryset.values(
                    'id', 'email', 'prompt', 'response', 'category',
                    'programming_language', 'prompt_type', 'ip_address', 'created_at'
                )

                df = pd.DataFrame(list(data))
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="filtered_tasks.xlsx"'
                df.to_excel(response, index=False)
                return response
        else:
            form = ExportExcelForm()

        return render(
            request,
            'admin/export_excel_form.html',
            {'form': form, 'title': 'Export to Excel with Filters'}
        )

    def export_selected_to_excel(self, request, queryset):
        data = queryset.values(
            'id', 'email', 'prompt', 'response', 'category',
            'programming_language', 'prompt_type', 'ip_address', 'created_at'
        )
        df = pd.DataFrame(list(data))
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="tasks_{queryset.count()}.xlsx"'
        df.to_excel(response, index=False)
        return response
    
    export_selected_to_excel.short_description = "Export selected to Excel"