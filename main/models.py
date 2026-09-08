from django.db import models
import re

class Leader(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text="e.g., National Chairperson")
    bio = models.TextField()
    image = models.ImageField(upload_to='leaders/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.position}"

class Milestone(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.year} - {self.title}"

class Value(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class e.g., fas fa-fire-alt")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    
    highlight_summary = models.TextField(blank=True, null=True, help_text="Summary or notes for past events")
    recap_image = models.ImageField(upload_to='events/recaps/', blank=True, null=True)
    resource_file = models.FileField(upload_to='events/resources/', blank=True, null=True, help_text="Downloadable notes or media files")
    
    # Removed editable=False so list_editable can work without throwing errors
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        if not self.pk and self.order == 0:
            self.order = Event.objects.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=255)
    institution_name = models.CharField(max_length=255)
    delegation_size = models.PositiveIntegerField(default=1)
    phone_number = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.institution_name} ({self.event.title})"

class Resource(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF Document'),
        ('audio', 'Audio / MP3'),
        ('video', 'Video Link'),
    ]
    
    CATEGORY_CHOICES = [
        ('prayer-guides', 'Prayer Guides'),
        ('leadership', 'Leadership Docs'),
        ('audio', 'Sermon Audio'),
        ('video', 'Sermon & Media Videos'),
        ('branding', 'Media & Branding'),
        ('reports', 'Chapter Reports'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='pdf')
    file_size = models.CharField(max_length=50, blank=True, help_text="e.g., 45 MINS or 2.4 MB")
    description = models.TextField()
    
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Paste YouTube or Facebook video link here")
    
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-uploaded_at']

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        if not self.video_url:
            return ""
        youtube_regex = (
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        )
        match = re.search(youtube_regex, self.video_url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url

class ChapterReport(models.Model):
    institution_name = models.CharField(max_length=200, help_text="e.g., University of Nairobi CU")
    secretary_name = models.CharField(max_length=100)
    email = models.EmailField()
    report_file = models.FileField(upload_to='chapter_reports/')
    testimony_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.institution_name} Report - {self.submitted_at.strftime('%b %Y')}"

class DailyPrayerFocus(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    zoom_link = models.URLField()
    is_active = models.BooleanField(default=True, help_text="Check this to show this focus on the home page.")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Testimony(models.Model):
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=150, help_text="e.g., CU Chairperson, University of Nairobi")
    quote = models.TextField()
    avatar = models.ImageField(upload_to='testimonies/', blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.author_role}"

class SiteStatistic(models.Model):
    chapters_count = models.PositiveIntegerField(default=52)
    regions_count = models.PositiveIntegerField(default=12)
    patrons_count = models.PositiveIntegerField(default=150)
    impacted_count = models.PositiveIntegerField(default=10000)

    def __str__(self):
        return "Site Statistics Configuration"


class ContactMessage(models.Model):
    INQUIRY_CHOICES = [
        ('New Chapter Application', 'New Chapter Application'),
        ('Partnership & Alumni Inquiry', 'Partnership & Alumni Inquiry'),
        ('Media & Press', 'Media & Press'),
        ('Prayer Request', 'Prayer Request'),
    ]
    
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    institution = models.CharField(max_length=150, blank=True, null=True)
    inquiry_type = models.CharField(max_length=100, choices=INQUIRY_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inquiry_type} - {self.full_name}"


class RegionalCoordinator(models.Model):
    region_name = models.CharField(max_length=150)
    coordinator_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.region_name} - {self.coordinator_name}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class NewsletterCampaign(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField(help_text="Write the body of your email message here.")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

from django.db import models

class StudentMember(models.Model):
    full_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=100, unique=True)
    whatsapp_number = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.institution}"

class ChapterLeader(models.Model):
    chapter_name = models.CharField(max_length=255)
    chairperson_name = models.CharField(max_length=255)
    member_count = models.PositiveIntegerField()
    region = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chapter_name} ({self.chairperson_name})"