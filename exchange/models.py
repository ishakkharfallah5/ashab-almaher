from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    points = models.IntegerField(default=100)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return self.username

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم'),
        ('expert', 'خبير'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Skill.LEVEL_CHOICES)
    is_teaching = models.BooleanField(default=True) # True if teaching, False if wanting to learn
    
    def __str__(self):
        role = "Teaching" if self.is_teaching else "Learning"
        return f"{self.user.username} - {role} {self.skill.name}"

class Session(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_sessions')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learned_sessions')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    points_exchanged = models.IntegerField()
    
    def __str__(self):
        return f"{self.teacher.username} teaching {self.learner.username}: {self.skill.name}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

class Review(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class VideoPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_posts')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"

class Report(models.Model):
    REPORT_TYPES = [
        ('harassment', 'تحرش أو إساءة'),
        ('inappropriate', 'محتوى غير لائق'),
        ('spam', 'رسائل مزعجة'),
        ('other', 'آخر'),
    ]
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.ForeignKey(VideoPost, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report by {self.reporter.username} against {self.reported_user.username}"
