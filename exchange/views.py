from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Skill, User, UserSkill, Session, Message, Review, VideoPost
from .forms import CustomUserCreationForm, UserSkillForm, VideoPostForm
import json

def home(request):
    skills = Skill.objects.all()[:6] # Show first 6 skills on home
    return render(request, 'home.html', {'skills': skills})

def skill_list(request):
    query = request.GET.get('q')
    if query:
        skills = Skill.objects.filter(name__icontains=query)
    else:
        skills = Skill.objects.all()
    return render(request, 'exchange/skill_list.html', {'skills': skills, 'query': query})

def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    teachers = UserSkill.objects.filter(skill=skill, is_teaching=True)
    learners = UserSkill.objects.filter(skill=skill, is_teaching=False)
    return render(request, 'exchange/skill_detail.html', {
        'skill': skill,
        'teachers': teachers,
        'learners': learners
    })


@login_required
def profile(request):
    teaching = UserSkill.objects.filter(user=request.user, is_teaching=True)
    learning = UserSkill.objects.filter(user=request.user, is_teaching=False)
    sessions = Session.objects.filter(teacher=request.user) | Session.objects.filter(learner=request.user)
    return render(request, 'exchange/profile.html', {
        'teaching': teaching,
        'learning': learning,
        'sessions': sessions.order_by('-date')[:10]
    })

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            user_skill = form.save(commit=False)
            user_skill.user = request.user
            user_skill.save()
            return redirect('exchange:profile')
    else:
        form = UserSkillForm()
    return render(request, 'exchange/add_skill.html', {'form': form})

from django.db import transaction

@login_required
def request_session(request, teacher_id, skill_id):
    teacher = get_object_or_404(User, pk=teacher_id)
    skill = get_object_or_404(Skill, pk=skill_id)
    
    if request.method == 'POST':
        points = 2 
        with transaction.atomic():
            # Get fresh user and lock row
            user = User.objects.select_for_update().get(id=request.user.id)
                
            # Create session
            Session.objects.create(
                teacher=teacher,
                learner=user,
                skill=skill,
                date=request.POST.get('date'),
                duration_hours=1,
                points_exchanged=5, # Keep teacher reward at 5 points
                status='requested'
            )
            
            # Award points immediately (+2 for starting to learn)
            user.points += points
            user.save()
            
        return redirect('exchange:profile')
    
    return render(request, 'exchange/request_session.html', {'teacher': teacher, 'skill': skill})

@login_required
def session_list(request):
    incoming = Session.objects.filter(teacher=request.user, status='requested')
    outgoing = Session.objects.filter(learner=request.user)
    return render(request, 'exchange/session_list.html', {'incoming': incoming, 'outgoing': outgoing})

@login_required
def approve_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id, teacher=request.user)
    session.status = 'approved'
    session.save()
    return redirect('exchange:session_list')

@login_required
def complete_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.teacher == request.user or session.learner == request.user:
        if session.status == 'approved':
            with transaction.atomic():
                session.status = 'completed'
                session.save()
                
                # Credit teacher
                teacher = User.objects.select_for_update().get(id=session.teacher.id)
                teacher.points += session.points_exchanged
                teacher.save()

                # Credit learner (+2 for learning)
                learner = User.objects.select_for_update().get(id=session.learner.id)
                learner.points += 2
                learner.save()
            
    return redirect('exchange:profile')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('exchange:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def leaderboard(request):
    top_users = User.objects.all().order_by('-points')[:10]
    return render(request, 'exchange/leaderboard.html', {'top_users': top_users})

@login_required
def message_list(request):
    from django.db import models
    received = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    sent = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    contact_ids = set(received) | set(sent)
    contacts = User.objects.filter(id__in=contact_ids)
    return render(request, 'exchange/message_list.html', {'contacts': contacts})

@login_required
def chat(request, user_id):
    from django.db import models
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('exchange:chat', user_id=user_id)
            
    return render(request, 'exchange/chat.html', {'other_user': other_user, 'chat_messages': messages})

@login_required
def submit_review(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.learner != request.user:
        return render(request, 'exchange/error.html', {'message': 'Only learners can review sessions.'})
    
    if session.status != 'completed':
        return render(request, 'exchange/error.html', {'message': 'You can only review completed sessions.'})

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(session=session, rating=rating, comment=comment)
        return redirect('exchange:profile')
        
    return render(request, 'exchange/submit_review.html', {'session': session})

def video_feed(request):
    videos = VideoPost.objects.all().order_by('-created_at')
    return render(request, 'exchange/video_feed.html', {'videos': videos})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoPostForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            
            # Credit user (+1 for sharing content)
            user = User.objects.select_for_update().get(id=request.user.id)
            user.points += 1
            user.save()
            
            return redirect('exchange:video_feed')
    else:
        form = VideoPostForm()
    return render(request, 'exchange/upload_video.html', {'form': form})
@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')
    return render(request, 'exchange/user_list.html', {'users': users})

@login_required
def reject_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id, teacher=request.user)
    if session.status == 'requested':
        with transaction.atomic():
            session.status = 'cancelled'
            session.save()
            
            # Refund learner
            learner = User.objects.select_for_update().get(id=session.learner.id)
            learner.points += session.points_exchanged
            learner.save()
        
    return redirect('exchange:session_list')

@login_required
def cancel_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id, learner=request.user)
    if session.status == 'requested':
        with transaction.atomic():
            session.status = 'cancelled'
            session.save()
            
            # Refund learner
            learner = User.objects.select_for_update().get(id=request.user.id)
            learner.points += session.points_exchanged
            learner.save()
        
    return redirect('exchange:session_list')

@login_required
def delete_user_skill(request, skill_id):
    user_skill = get_object_or_404(UserSkill, pk=skill_id, user=request.user)
    user_skill.delete()
    return redirect('exchange:profile')

@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user != request.user:
        if request.user.following.filter(id=user_id).exists():
            request.user.following.remove(target_user)
        else:
            request.user.following.add(target_user)
    return redirect(request.META.get('HTTP_REFERER', 'exchange:user_list'))

def rules_page(request):
    return render(request, 'exchange/rules.html')

@login_required
def report_content(request, user_id):
    reported_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        
        # Create the report
        Report.objects.create(
            reporter=request.user,
            reported_user=reported_user,
            reason=reason,
            description=description
        )
        
        # Immediate Punishment: -10 points
        reported_user.points -= 10
        reported_user.save()
        
        from django.contrib import messages
        messages.warning(request, f'تم تقديم الإبلاغ. تم خصم 10 نقاط من {reported_user.username} كعقوبة مبدئية.')
        return redirect('exchange:home')
        
    return render(request, 'exchange/report_form.html', {'reported_user': reported_user})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return reverse_lazy('exchange:rules')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        remembered_user = self.request.get_signed_cookie('remembered_user', default=None)
        if remembered_user:
            try:
                user_data = json.loads(remembered_user)
                context['remembered_user'] = user_data
            except:
                pass
        return context

def custom_logout(request):
    user = request.user
    response = redirect('login')
    if user.is_authenticated:
        user_data = json.dumps({
            'username': user.username,
            'id': user.id
        })
        # Set a signed cookie that expires in 30 days
        response.set_signed_cookie('remembered_user', user_data, max_age=30*24*60*60)
    auth_logout(request)
    return response

def quick_login(request):
    remembered_user = request.get_signed_cookie('remembered_user', default=None)
    if remembered_user:
        try:
            user_data = json.loads(remembered_user)
            user = User.objects.get(id=user_data['id'])
            # We log them in without a password as requested
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('exchange:rules')
        except:
            pass
    return redirect('login')
