# main/context_processors.py
from .forms import NewsletterForm # Replace with your actual newsletter form import if named differently

def newsletter(request):
    return {
        'newsletter_form': NewsletterForm()
    }