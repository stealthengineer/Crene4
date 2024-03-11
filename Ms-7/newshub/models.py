from django.db import models
from django.contrib.auth.models import User
from branches.models import (Branch,
                             Leaf,
                             Rating)

# Create your models here.

class Comments(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    leaf = models.ForeignKey(Leaf,on_delete=models.CASCADE,blank=True,null=True,related_name='commentonleaf')
    rating = models.ForeignKey(Rating,on_delete=models.CASCADE,blank=True,null=True,related_name='commentonrating')
    text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    news_id = models.CharField(max_length=500,blank=True,null=True)
    is_delete = models.BooleanField(default=False,null=True,blank=True)
    is_parent = models.BooleanField(default=True)
    parent_comment = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='sub_comments')

    class Meta:
        db_table = 'comments'
        indexes = [
            models.Index(fields=[ 'news_id','is_delete']),
        ]

class Reactions(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='reactions')
    reaction_type = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    news_id = models.CharField(max_length=500)
    is_delete= models.BooleanField(default=False,null=True,blank=True)

    class Meta:
        db_table = 'reactions'
        indexes = [
            models.Index(fields=[ 'news_id','is_delete']),
        ]


class Voting(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='voteing')
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE,blank=True,null=True,related_name='commnt_voteing')
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True,related_name='votingonbranch')
    leaf = models.ForeignKey(Leaf,on_delete=models.CASCADE,blank=True,null=True,related_name='votingonleaf')
    rating = models.ForeignKey(Rating,on_delete=models.CASCADE,blank=True,null=True,related_name='votingonrating')
    in_favour =  models.BooleanField()
    # class Meta:
    #     unique_together = ["user", "comment",]