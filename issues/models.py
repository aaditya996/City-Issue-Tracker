from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver # Signal ke liye zaroori
from django.core.exceptions import ObjectDoesNotExist

# Define the 5 Categories and 5 Statuses as Choices

class Issue(models.Model):

    # --- CATEGORIES ---
    CATEGORY_CHOICES = [
        ('ROAD', 'Roads & Infrastructure'),
        ('SANI', 'Sanitation & Waste'),
        ('WATR', 'Water & Drainage'),
        ('SAFE', 'Public Safety'),
        ('CIVC', 'Civic Amenities & Public Spaces'),
    ]

    # --- STATUSES (Tracker) ---
    STATUS_CHOICES = [
        ('REP', 'Reported'),
        ('REV', 'Under Review'),
        ('IPR', 'In Progress'),
        ('RES', 'Resolved'),
        ('REJ', 'Rejected'),
    ]

    # --- ISSUE FIELDS ---
    title = models.CharField(max_length=150, verbose_name="Issue Title")
    description = models.TextField(verbose_name="Detailed Description")

    category = models.CharField(
        max_length=4,
        choices=CATEGORY_CHOICES,
        default='ROAD',
        verbose_name="Category"
    )
    
    # Location
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Media and Status Tracking
    photo = models.ImageField(upload_to='issue_photos/', blank=True, null=True)
    
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='REP',
        verbose_name="Current Status"
    )

    # Metadata
    reported_at = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-reported_at'] # Naye issues pehle dikhenge
        verbose_name = "Issue"
        verbose_name_plural = "Issues"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# -------------------------------------------------------------
# --- COMMENT MODEL ---
# -------------------------------------------------------------
class Comment(models.Model):
    issue = models.ForeignKey(
        Issue, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    # ✅ FIX: Field name ko 'text' rakha gaya hai
    text = models.TextField(verbose_name="Comment Content") 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ...
        ordering = ['-created_at'] 

    def __str__(self):
        return f'Comment by {self.user.username} on {self.issue.title[:30]}...'
        
# -------------------------------------------------------------
# --- USER PROFILE MODEL ---
# -------------------------------------------------------------
class UserProfile(models.Model):
    # One-to-One Link to the default User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other/Prefer not to say'),
    ]
    
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f'{self.user.username} Profile'

# -------------------------------------------------------------
# --- SIGNALS (Automatic Profile Creation/Update) ---
# -------------------------------------------------------------

# Naya user banne par profile automatically create ho jayegi
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Agar naya user create hua hai, toh uske liye UserProfile bhi create karo
    if created:
        UserProfile.objects.create(user=instance)
    
    # Agar user exist karta hai aur save ho raha hai, toh uske associated profile ko bhi save karo
    # Ismein UserProfileForm se kiye gaye changes save ho jayenge.
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Yeh tab hoga jab user exist karta ho but profile na ho (migrations ke dauraan)
        # Is case mein hum profile create kar denge
        UserProfile.objects.create(user=instance)