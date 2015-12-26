# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

'''------------------------answer-------------------------------------------'''

class Answer_Provider(models.Model):
        Provider = models.IntegerField(primary_key=True)#User_No

class Answer_Voter(models.Model):
        Voter = models.IntegerField(primary_key=True)#User_No
        
class Answer_Comment(models.Model):
	Ans_Comment_No = models.AutoField(primary_key=True)
	Commenter = models.IntegerField()#User_No
	Context = models.TextField()
	VotersNum = models.IntegerField()

class Answer(models.Model):
	Ans_No = models.AutoField(primary_key=True)
	Ans_Provider = models.ForeignKey(Answer_Provider)#User_No------------------ 
	Ans_Time = models.DateField()
	Ans_Context = models.TextField()
	Ans_Of_Question = models.IntegerField()#Ques_No
	Ans_Voters = models.ManyToManyField(Answer_Voter,blank=True)#vote
	Ans_Comments = models.ManyToManyField(Answer_Comment,blank=True)#comment

'''------------------------answer-------------------------------------------'''

'''------------------------question-------------------------------------------'''

class Question_Follower(models.Model):
        Follower = models.IntegerField(primary_key=True)#User_No
        
class Tag(models.Model):
        tag_choices = (
                (0,u"自然语言"),
                (1,u"数学"),
                (2,u"外语"),
                (3,u"计算机"),
                (4,u"物理学"),
                (5,u"化学"),
                (6,u"生物科学"),
                (7,u"地理学"),
                (8,u"政治学"),
                (9,u"经济学"),
                (10,u"历史学"),
                (11,u"社会学"),
                (12,u"生活"),
                (13,u"哲学"),
                (14,u"体育"),
                (15,u"健康"),
                (16,u"情感"),
        )
	Tag_Name = models.IntegerField(choices = tag_choices,primary_key=True)
	Tag_Description = models.TextField()

class Question_Comment(models.Model):
	Question_Comment_No = models.AutoField(primary_key=True)
	Commenter = models.IntegerField()#User_No
	Context = models.TextField()
	VotersNum = models.IntegerField()
	
class Question_Asker(models.Model):
    Asker = models.IntegerField(primary_key=True)#User_No

class Question(models.Model):
	No = models.AutoField(primary_key=True)
	Title = models.CharField(max_length=100)
	Description = models.TextField()
	Tags = models.ForeignKey(Tag,related_name='topic')#tag
	Asker = models.ForeignKey(Question_Asker)#User_No--------------------------
	Followers = models.ManyToManyField(Question_Follower,blank=True)#User_No
	Answers = models.ManyToManyField(Answer,blank=True)#ans
	Comments = models.ManyToManyField(Question_Comment,blank=True)#comment

'''------------------------question-------------------------------------------'''

'''------------------------User-------------------------------------------'''
class Follow_Question(models.Model):
        Follow_Question = models.IntegerField(primary_key=True)#Question_No

class Asked_Question(models.Model):
        Asked_Question = models.IntegerField(primary_key=True)#Question_No

class Comment_Question(models.Model):
        Comment_Question = models.IntegerField(primary_key=True)#Question_No

class Followed_User(models.Model):
        Followed_User = models.IntegerField(primary_key=True)#User_No

class Follower_User(models.Model):
        Follower_User = models.IntegerField(primary_key=True)#User_No
        
class Ans_of_User(models.Model):
        Ans_of_User = models.IntegerField(primary_key=True)#Ans_No

class Comment_Ans_of_User(models.Model):
        Ans_of_User = models.IntegerField(primary_key=True)#Ans_No

class Vote_Ans_of_User(models.Model):
        Ans_of_User = models.IntegerField(primary_key=True)#Ans_No

class Contact_Info(models.Model):
		No = models.AutoField(primary_key=True)
		receiver = models.IntegerField()#User_No
		sender = models.IntegerField()#User_No
		message = models.TextField()
		message_time = models.DateField()

	
class User(models.Model):
	User_No = models.AutoField(primary_key=True)
	User_Name = models.CharField(max_length=10)
	User_Pass = models.CharField(max_length=40)
	User_Description = models.TextField()
	User_Email = models.EmailField()
	User_FollowQues = models.ManyToManyField(Follow_Question,blank=True)#ques
	User_AskedQues = models.ManyToManyField(Asked_Question,blank=True)#ques
	User_CommentQues = models.ManyToManyField(Comment_Question,blank=True)#ques
	User_Followed = models.ManyToManyField(Followed_User,blank=True)#user
	User_Followers = models.ManyToManyField(Follower_User,blank=True)#user
	User_Ans = models.ManyToManyField(Ans_of_User,blank=True)#ans
	User_CommentAns = models.ManyToManyField(Comment_Ans_of_User,blank=True)#ans
	User_VoteAns = models.ManyToManyField(Vote_Ans_of_User,blank=True)#ans
	User_MyMessage = models.ManyToManyField(Contact_Info,blank=True)#
'''------------------------User-------------------------------------------'''
'''Classes of manage backend database for django administration'''
	
    
