


from django import forms
from django.forms import ModelForm

from .models import *

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'category','subtitle1', 'subtitle1_completed', 'subtitle2', 'subtitle2_completed','subtitle3', 'subtitle3_completed','subtitle4', 'subtitle4_completed','subtitle5', 'subtitle5_completed','priority', 'is_completed']
        widgets = {
            'priority': forms.RadioSelect,  # ラジオボタンで選択
            'category': forms.Select,       # ドロップダウンメニューでカテゴリを選択
        }




class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['title', 'subtitle1', 'subtitle2', 'subtitle3', 'subtitle4', 'subtitle5', 'category', 'priority']
        labels = {
            'title': 'テンプレートのタイトル',
            'subtitle': 'サブタイトル',
            'category': 'カテゴリ',
            'priority': '重要度',
        }
        widgets = {
            'priority': forms.RadioSelect,  # ラジオボタンで選択
            'category': forms.Select,       # ドロップダウンメニューでカテゴリを選択
        }