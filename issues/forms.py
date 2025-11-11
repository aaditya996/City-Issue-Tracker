from django import forms
from .models import Issue, UserProfile, Comment
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status']
        
class IssueReportForm(forms.ModelForm):
    # Yahan hum hidden fields ko widgets se handle karenge
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Issue
        # Sirf woh fields jo user se input lene hain
        fields = ['title', 'description', 'category', 'photo', 'latitude', 'longitude']
        # Optional: Add custom styling classes to the fields
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# --- NEW PROFILE UPDATE FORM (STEP 2.1) ---
class UserProfileForm(forms.ModelForm):
    # User model fields ko ModelForm mein add kiya gaya hai
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True) # Email ko required rakha gaya hai

    class Meta:
        model = UserProfile
        # UserProfile ke fields
        fields = ['profile_image', 'gender', 'age', 'contact_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    # Form ko initialize karte waqt User fields ko form data se fill karna
    def __init__(self, *args, **kwargs):
        profile_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        # FIX: Agar instance available hai, toh User fields ko initial data mein set karein
        if profile_instance and profile_instance.user:
            self.initial['first_name'] = profile_instance.user.first_name
            self.initial['last_name'] = profile_instance.user.last_name
            self.initial['email'] = profile_instance.user.email

    # Form save hone ke baad User fields ko save karna
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        
        # FIX: User fields ko cleaned_data se update karein
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)

        if commit:
            user.save()
            profile.save()
        return profile
# --- END NEW PROFILE UPDATE FORM ---

# --- NEW: Comment Form ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # ✅ FIX: Field name 'text'
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Add a comment or update...',
                'style': 'resize: vertical;'
            }),
        }