from django.contrib import admin
from .models import Issue, UserProfile

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # Yeh fields list view mein dikhenge
    list_display = ('title', 'category', 'status', 'reported_at', 'reported_by') 
    # Yeh fields side panel se filter ho sakte hain
    list_filter = ('category', 'status', 'reported_at') 
    # Yeh fields search bar se search ho sakte hain
    search_fields = ('title', 'description')

# NEW: UserProfile ko Admin mein dikhana
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'contact_number')
    search_fields = ('user__username', 'contact_number')