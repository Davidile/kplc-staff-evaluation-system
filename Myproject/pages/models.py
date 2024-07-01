from django.db import models
from datetime import timedelta,date
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_head')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='announcements')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title    

class PerformanceReview(models.Model):
    QUALITY_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Above Average', 'Above Average'),
        ('Average', 'Average'),
        ('Below Average', 'Below Average'),
        ('Unsatisfactory', 'Unsatisfactory'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    knowledge_of_work = models.CharField(max_length=15, choices=QUALITY_CHOICES)
    quality_of_work = models.CharField(max_length=15, choices=QUALITY_CHOICES)
    productivity = models.CharField(max_length=15, choices=QUALITY_CHOICES)
    initiative = models.CharField(max_length=15, choices=QUALITY_CHOICES)
    communication_skills = models.CharField(max_length=15, choices=QUALITY_CHOICES)
    overall_performance = models.CharField(max_length=15, choices=QUALITY_CHOICES)
    comments = models.TextField(blank=True, null=True)
    review_date = models.DateField(auto_now_add=True)

    def get_score(self, rating):
        scores = {
            'Excellent': 4,
            'Above Average': 3,
            'Average': 2,
            'Below Average': 1,
            'Unsatisfactory': 0
        }
        return scores.get(rating, 0)

    def calculate_total_score(self):
        ratings = [
            self.knowledge_of_work,
            self.quality_of_work,
            self.productivity,
            self.initiative,
            self.communication_skills,
            self.overall_performance
        ]
        total_weighted_score = sum(self.get_score(rating) for rating in ratings)
        number_of_activities = len(ratings)
        max_score = 4  # Max score per activity is 4 for 'Excellent'
        total_score = (total_weighted_score / (number_of_activities * max_score)) * 100
        return total_score
    def can_review(self):
        last_review=PerformanceReview.objects.filter(user=self.user).order_by('-review_date').first()
        if last_review and (date.today()-last_review.review_date).days<120:
            return False
        return True

    def __str__(self):
        return f"Review for {self.user.username} on {self.review_date}"
