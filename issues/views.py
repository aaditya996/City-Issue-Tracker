from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.db.models import Q 
from django.core.paginator import Paginator
from django.db import transaction # For profile_edit
from django.core.exceptions import ObjectDoesNotExist 

from .models import Issue, Comment, UserProfile 
from .forms import IssueReportForm, StatusUpdateForm, CommentForm, UserProfileForm 

# 1. Issue Listing View (Home Page - Search, Filter, Pagination)
def issue_list(request):
    # Base Query: Saare issues ko naye se purane order mein lo
    issues_list = Issue.objects.all().order_by('-reported_at') 
    
    # 1. SEARCH LOGIC (Title and Description)
    query = request.GET.get('q') 
    if query:
        issues_list = issues_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    # 2. FILTER LOGIC (Category and Status)
    selected_status = request.GET.get('status')
    selected_category = request.GET.get('category')
    
    if selected_status:
        issues_list = issues_list.filter(status=selected_status)
    
    if selected_category:
        issues_list = issues_list.filter(category=selected_category)
        
    # 3. PAGINATION
    paginator = Paginator(issues_list, 10) 
    page_number = request.GET.get('page')
    issues = paginator.get_page(page_number) 

    # 4. Context Data 
    context = {
        'issues': issues, 
        'title': 'All Reported Issues',
        # Dhyan rahe ki Issue model mein STATUS_CHOICES aur CATEGORY_CHOICES defined hon
        'status_choices': Issue.STATUS_CHOICES,
        'category_choices': Issue.CATEGORY_CHOICES,
        'selected_status': selected_status,
        'selected_category': selected_category,
        'query': query or '',
    }
    return render(request, 'issues/issue_list.html', context)
    
# 2. Issue Reporting View
@login_required 
def report_issue(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reported_by = request.user
            issue.save()
            return redirect('issue_list') 
    else:
        form = IssueReportForm()

    context = {
        'form': form,
        'title': 'Report a New Issue'
    }
    return render(request, 'issues/report_issue.html', context)

# 3. Issue Detail View (Status Update and Comments)
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    
    # Forms ko initialize karo
    status_form = StatusUpdateForm(instance=issue) 
    comment_form = CommentForm() 

    if request.method == 'POST':
        
        # --- 1. Status Update Logic (Staff Only) ---
        if 'status_update' in request.POST:
            if request.user.is_staff: 
                status_form = StatusUpdateForm(request.POST, instance=issue)
                if status_form.is_valid():
                    status_form.save()
                    return redirect('issue_detail', pk=issue.pk)
            # Staff nahi hai, toh kuch nahi karo ya error do
            
        # --- 2. Comment Submission Logic (Logged-in Users) ---
        elif 'post_comment' in request.POST:
            if request.user.is_authenticated:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.issue = issue       # Issue assign kiya
                    comment.user = request.user # User assign kiya
                    comment.save()
                    return redirect('issue_detail', pk=issue.pk)
            else:
                # Login page par redirect karo, jisse woh wapas detail page par aa sakein
                return redirect('login') 
    
    # Saare comments fetch karein
    comments = issue.comments.all() 

    context = {
        'issue': issue,
        'status_form': status_form,
        'comment_form': comment_form,
        'comments': comments,        
    }
    return render(request, 'issues/issue_detail.html', context)


# 4. Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            return redirect('login') 
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'title': 'Sign Up'
    }
    return render(request, 'issues/register.html', context)  


# 5. My Issues Dashboard View
@login_required 
def my_issues(request):
    # Sirf woh issues nikaalo jo current logged-in user ne report kiye hain
    issues_list = Issue.objects.filter(reported_by=request.user).order_by('-reported_at')

    # Pagination logic
    paginator = Paginator(issues_list, 10) 
    page_number = request.GET.get('page')
    issues = paginator.get_page(page_number)

    context = {
        'issues': issues,
        'title': 'My Reported Issues',
    }
    return render(request, 'issues/my_issues.html', context)


# 6. Profile Edit/View (FIXED: Added @transaction.atomic for safety)
@login_required
@transaction.atomic # User aur UserProfile dono ko ek transaction mein save karta hai
def profile_edit(request):
    # Agar UserProfile exist nahi karta, toh create karo
    try:
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        # Agar signal fail ho gaya ya miss ho gaya, toh yahan create kar do
        profile = UserProfile.objects.create(user=request.user) 

    if request.method == 'POST':
        # request.FILES for profile_image upload
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # UserProfileForm ki custom save method User aur UserProfile dono ko save karegi
            form.save() 
            # Success ke baad Profile page par hi redirect karein taaki user changes dekh sakein
            return redirect('profile_edit') 
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'title': 'Edit Profile'
    }
    return render(request, 'issues/profile_edit.html', context)