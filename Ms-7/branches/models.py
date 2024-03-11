from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

from S3config import PublicMediaStorage

# Create your models here.

class Topic (models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userontopic')
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Branch(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='useronbranch')
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='topiconbranch')
    heading = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.FileField(null=True, blank=True,storage=PublicMediaStorage())
    is_delete = models.BooleanField(default=False)
    def __str__(self):
        return self.heading


class Leaf(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='useronleaf')
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='branchonleaf')
    content = models.TextField()
    is_parent = models.BooleanField(default=True)
    parent_leaf = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='sub_leaf')
    created_at = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return self.branch.heading


class Politician(models.Model):
    name = models.CharField(max_length=50)
    discription = models.TextField()
    picture = models.ImageField(null=True, blank=True,storage=PublicMediaStorage())
    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='useronrating')
    politician = models.ForeignKey(Politician,on_delete=models.CASCADE,related_name='politicianonrating')
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    feedback = models.CharField(max_length=400)
    def __str__(self):
        return f'{self.politician.name}({self.rate})'



    



