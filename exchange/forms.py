from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].label = "البريد الإلكتروني"
        if 'username' in self.fields:
            self.fields['username'].label = "اسم المستخدم"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'glass', 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'})

from .models import UserSkill

class UserSkillForm(forms.ModelForm):
    IS_TEACHING_CHOICES = [
        (True, 'أريد تدريس هذه المهارة'),
        (False, 'أريد تعلم هذه المهارة'),
    ]
    is_teaching = forms.TypedChoiceField(
        choices=IS_TEACHING_CHOICES,
        coerce=lambda x: str(x) == 'True',
        widget=forms.Select(attrs={'class': 'glass', 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'}),
        label='نوع المشاركة'
    )

    class Meta:
        model = UserSkill
        fields = ['skill', 'level', 'is_teaching']
        labels = {
            'skill': 'المهارة',
            'level': 'المستوى',
        }
        widgets = {
            'skill': forms.Select(attrs={'class': 'glass', 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'}),
            'level': forms.Select(attrs={'class': 'glass', 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'}),
        }

from .models import VideoPost

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ['title', 'description', 'video_file']
        labels = {
            'title': 'العنوان',
            'description': 'الوصف',
            'video_file': 'ملف الفيديو',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'glass', 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'}),
            'description': forms.Textarea(attrs={'class': 'glass', 'rows': 3, 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'}),
            'video_file': forms.FileInput(attrs={'class': 'glass', 'style': 'width: 100%; padding: 0.75rem; margin-bottom: 1rem; color: white; border: 1px solid var(--glass-border); background: var(--glass-bg);'}),
        }
