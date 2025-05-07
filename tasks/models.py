from django.db import models

class Task(models.Model):
    CATEGORIES = [
        ('sport', 'Sport'),
        ('health', 'Health'),
        ('tourism', 'Tourism'),
        ('finance', 'Finance'),
        ('games', 'Games'),
    ]

    LANGUAGES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('swift', 'Swift'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('html_css', 'HTML/CSS'),
    ]

    PROMPT_TYPES = [
        ('debugging', 'Debugging'),
        ('documentation', 'Documentation'),
        ('generation', 'Generation'),
    ]

    email = models.EmailField()
    prompt = models.TextField()
    response = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORIES)
    programming_language = models.CharField(max_length=10, choices=LANGUAGES)
    prompt_type = models.CharField(max_length=15, choices=PROMPT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)