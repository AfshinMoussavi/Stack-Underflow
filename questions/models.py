from django.db import models
from users.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name}'
    
    
class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name='upvoted_questions', blank=True)
    downvoters = models.ManyToManyField(User, related_name='downvoted_questions', blank=True)
    tags = models.ManyToManyField(Tag , related_name='questions', blank=True) 
    
    @property
    def votes(self):
        return self.upvoters.count() - self.downvoters.count()

    def __str__(self):
        return f'{self.title}'

class Answer(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name='upvoted_answers', blank=True)
    downvoters = models.ManyToManyField(User, related_name='downvoted_answers', blank=True)
    
    class Meta:
        ordering = ['-created_at']

    
    @property
    def votes(self):
        return self.upvoters.count() - self.downvoters.count()

    def __str__(self):
        return f'{self.body}'