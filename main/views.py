from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ChapterReportForm, ContactForm, NewsletterForm, StudentMemberForm, ChapterLeaderForm
from .models import (
    ChapterReport, DailyPrayerFocus, Event, EventRegistration,
    FAQ, Leader, Milestone, Region, Resource, Testimony, Value
)

def process_newsletter(request):
    if request.method == 'POST' and 'newsletter_submit' in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to the newsletter.')
            return redirect(request.path)
        else:
            messages.error(request, 'Please provide a valid email address for the newsletter.')
    return None

def home_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    context = {
        'total_chapters': ChapterReport.objects.count(),
        'total_regions': Region.objects.count(),
        'active_focus': DailyPrayerFocus.objects.filter(is_active=True).first(),
        'testimonies': Testimony.objects.filter(is_approved=True)[:2],
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'index.html', context)


def about_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    context = {
        'leaders': Leader.objects.all().order_by('order'),
        'milestones': Milestone.objects.all().order_by('order'),
        'values': Value.objects.all().order_by('order'),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'about.html', context)


def events_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    now = timezone.now()
    next_event = Event.objects.filter(date__gte=now).order_by('date').first()

    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')
    past_events = Event.objects.filter(date__lt=now).order_by('-date')
    regions = Region.objects.all()

    if request.method == 'POST' and 'newsletter_submit' not in request.POST:
        full_name = request.POST.get('full_name')
        event_title = request.POST.get('event_title')
        institution_name = request.POST.get('institution_name')
        delegation_size = request.POST.get('delegation_size')
        phone_number = request.POST.get('phone_number')

        event_obj = Event.objects.filter(title=event_title).first() or next_event

        if event_obj and full_name and institution_name and phone_number:
            EventRegistration.objects.create(
                event=event_obj,
                full_name=full_name,
                institution_name=institution_name,
                delegation_size=delegation_size or 1,
                phone_number=phone_number,
            )
            messages.success(request, 'Your delegation spot has been successfully secured.')
            return redirect('events')
        else:
            messages.error(request, 'Please fill in all required fields correctly.')

    context = {
        'next_event': next_event,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events': upcoming_events,
        'regions': regions,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'events.html', context)


def event_detail_view(request, event_id):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'event_detail.html', context)


def resources_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST' and 'newsletter_submit' not in request.POST:
        report_form = ChapterReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            report_form.save()
            messages.success(request, 'Your chapter report has been submitted successfully.')
            return redirect('resources')
        else:
            messages.error(request, 'Please correct the errors below in your chapter report submission.')
    else:
        report_form = ChapterReportForm()

    featured_resource = Resource.objects.filter(is_featured=True).first()
    prayer_guides = Resource.objects.filter(category='prayer-guides')
    leadership_docs = Resource.objects.filter(category='leadership')
    audio_sermons = Resource.objects.filter(category='audio')
    video_resources = Resource.objects.filter(category='video')

    context = {
        'featured_resource': featured_resource,
        'prayer_guides': prayer_guides,
        'leadership_docs': leadership_docs,
        'audio_sermons': audio_sermons,
        'video_resources': video_resources,
        'report_form': report_form,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'resources.html', context)


def contact_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST' and 'newsletter_submit' not in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully. The secretariat will reach out shortly.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form, 'newsletter_form': NewsletterForm()})


def faq_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'faq.html', context)


def join_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response

    student_form = StudentMemberForm()
    chapter_form = ChapterLeaderForm()

    if request.method == 'POST':
        if 'register_student' in request.POST:
            student_form = StudentMemberForm(request.POST)
            if student_form.is_valid():
                student_form.save()
                messages.success(request, "Student registration successful!")
                return redirect('join')
            else:
                messages.error(request, "Please correct the errors in the student form.")
                
        elif 'register_chapter' in request.POST:
            chapter_form = ChapterLeaderForm(request.POST)
            if chapter_form.is_valid():
                chapter_form.save()
                messages.success(request, "Chapter charter submission successful!")
                return redirect('join')
            else:
                messages.error(request, "Please correct the errors in the chapter form.")

    context = {
        'student_form': student_form,
        'chapter_form': chapter_form,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'join.html', context)

def privacy_policy_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response
    
    context = {
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'privacy.html', context)


def terms_of_service_view(request):
    redirect_response = process_newsletter(request)
    if redirect_response:
        return redirect_response
    
    context = {
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'terms.html', context)