# -*- coding: utf-8 -*-
from django.contrib import admin
from qaq.models import*
admin.site.register(Answer_Voter)
admin.site.register(Answer_Comment)
admin.site.register(Answer_Provider)
admin.site.register(Answer)

admin.site.register(Question_Follower)
admin.site.register(Tag)
admin.site.register(Question_Comment)
admin.site.register(Question_Asker)
admin.site.register(Question)

admin.site.register(Follow_Question)
admin.site.register(Asked_Question)
admin.site.register(Comment_Question)
admin.site.register(Followed_User)
admin.site.register(Follower_User)
admin.site.register(Ans_of_User)
admin.site.register(Comment_Ans_of_User)
admin.site.register(Vote_Ans_of_User)
admin.site.register(Contact_Info)
admin.site.register(User)
