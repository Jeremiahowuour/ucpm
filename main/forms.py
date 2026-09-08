from django import forms
from .models import ChapterReport,  ContactMessage

class ChapterReportForm(forms.ModelForm):
    class Meta:
        model = ChapterReport
        fields = ['institution_name', 'secretary_name', 'email', 'report_file', 'testimony_notes']
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University Name'}),
            'secretary_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'report_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'testimony_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief testimonies or highlights'}),
        }

from django import forms
from .models import ContactMessage, NewsletterSubscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'inquiry_type', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@email.com'}),
            'inquiry_type': forms.Select(attrs={'class': 'form-select border-0 bg-light p-3 rounded-3'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'How can we help you?'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm bg-dark border-white border-opacity-25 text-white', 'placeholder': 'Email Address'}),
        }

from django import forms
from .models import StudentMember, ChapterLeader

class StudentMemberForm(forms.ModelForm):
    class Meta:
        model = StudentMember
        fields = ['full_name', 'institution', 'admission_number', 'whatsapp_number', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jane Doe'}),
            'institution': forms.Select(attrs={'class': 'form-select'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E35/1234/2026'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0712 345 678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@example.com'}),
        }

class ChapterLeaderForm(forms.ModelForm):
    class Meta:
        model = ChapterLeader
        fields = ['chapter_name', 'chairperson_name', 'member_count', 'region']
        widgets = {
            'chapter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Egerton University Main Campus'}),
            'chairperson_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Leader's Name"}),
            'member_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '15'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
        }