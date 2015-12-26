# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import*
# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
import datetime
import random

def homepage(request):
	questions = Question.objects.all()[::-1]#find all question
	t = get_template('index.html')
	match_answers_questions = {}
	for question in questions:
		answers = question.Answers.all()
		if answers:
			answer = random.choice(answers)
			provider = User.objects.filter(User_No=answer.Ans_Provider.Provider)#get answer provider's name
			match_answers_questions[question] = answer,provider[0]
		else:
			match_answers_questions[question] = None
	try:
		html = t.render(Context({'dict':match_answers_questions,'islogin':request.session['isSuccessFlag']}))#request.session['isSuccessFlag']
	except KeyError:
		html = t.render(Context({'dict':match_answers_questions,'islogin':False}))#request.session['isSuccessFlag']
	return HttpResponse(html)

def search(request):
	if request.method == "POST":
		lookfor = request.POST['lookfor']
		questions= Question.objects.filter(Title__icontains=lookfor)
		match_answers_questions = {}
		for question in questions:
			answers = question.Answers.all()
			if answers:
				answer = random.choice(answers)
				match_answers_questions[question] = answer
			else:
				match_answers_questions[question] = None
		t = get_template('search_result.html')
		try:
			html = t.render(Context({'dict':match_answers_questions,'islogin':request.session['isSuccessFlag']}))
		except KeyError:
			html = t.render(Context({'dict':match_answers_questions,'islogin':False}))
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)


def topic(request):
	match_tags_questions = {}
	for tag in Tag.objects.all():
		questions = Question.objects.filter(Tags=tag)
		tag_string = tag.tag_choices[tag.Tag_Name][1]
		tag_name = tag.Tag_Name
		match_tags_questions[tag_name] = tag_string,questions
	t = get_template('topic.html')
	try:
		html = t.render(Context({'dict':match_tags_questions,'islogin':request.session['isSuccessFlag']}))
	except KeyError:
		html = t.render(Context({'dict':match_tags_questions,'islogin':False}))
	return HttpResponse(html)

def find(request):
	match_tags_questions = {}
	for tag in Tag.objects.all():
		questions = Question.objects.filter(Tags=tag)
		match_answers_questions = []
		for question in questions:
			answers = question.Answers.all()
			if answers:
				answer = random.choice(answers)
				provider = User.objects.filter(User_No=answer.Ans_Provider.Provider)#get answer provider's name
				question_answer = question,answer,provider[0]
			else:
				question_answer = question,None,None
			match_answers_questions.append(question_answer)
		tag_string = tag.tag_choices[tag.Tag_Name][1]
		tag_name = tag.Tag_Name
		match_tags_questions[tag_name] = tag_string,match_answers_questions
	t = get_template('find.html')
	try:
		html = t.render(Context({'dict':match_tags_questions,'islogin':request.session['isSuccessFlag']}))
	except KeyError:
		html = t.render(Context({'dict':match_tags_questions,'islogin':False}))
	return HttpResponse(html)

def info(request):
	t = get_template('info.html')
	try:
		now_user = User.objects.filter(User_No = request.session['user_id'])[0]
		messages = []
		for message in now_user.User_MyMessage.all():
			sender = User.objects.filter(User_No=message.sender)[0]
			messages.append((message,sender))
		followeds = []
		for followed in now_user.User_Followed.all():
			answer_provider = Answer_Provider(Provider=followed.Followed_User)
			follow_question_answer = []
			for answer in Answer.objects.filter(Ans_Provider=answer_provider):
				question = Question.objects.filter(No = answer.Ans_Of_Question)[0]
				follow_question_answer.append((question,answer))
			followeds.append(follow_question_answer)
		html = t.render(Context({'followeds':followeds,'messages':messages,'islogin':request.session['isSuccessFlag']}))
		return HttpResponse(html)
	except KeyError:
		html = t.render(Context({'islogin':False}))
		return HttpResponse(html)

def myhome(request):
	t = get_template('myhome.html')
	followed_users = []
	follower_users = []
	asked_que = []
	followed_que = []
	comment_que = []
	answered = []
	comment_ans = []
	voted_ans = []
	try:
		user = User.objects.filter(User_No = request.session['user_id'])[0]
		followed = user.User_Followed.all()
		follower = user.User_Followers.all()
		askedQue = user.User_AskedQues.all()
		followedQue = user.User_FollowQues.all()
		commentQue = user.User_CommentQues.all()
		ans = user.User_Ans.all()
		commentAns = user.User_CommentAns.all()
		votedAns = user.User_VoteAns.all()
		for f1 in followed:
			objects1 = User.objects.filter(User_No = f1.Followed_User)[0]
			followed_users.append(objects1)
		for f2 in follower:
			objects2 = User.objects.filter(User_No = f2.Follower_User)[0]
			follower_users.append(objects2)
		for f3 in askedQue:
			objects3 = Question.objects.filter(No = f3.Asked_Question)[0]
			asked_que.append(objects3)
		for f4 in followedQue:
			objects4 = Question.objects.filter(No = f4.Follow_Question)[0]
			followed_que.append(objects4)
		for f5 in commentQue:
			objects5 = Question.objects.filter(No = f5.Comment_Question)[0]
			comment_que.append(objects5)
		for f6 in ans:
			objects6 = Answer.objects.filter(Ans_No = f6.Ans_of_User)[0]
			question = Question.objects.filter(No = objects6.Ans_Of_Question)[0]
			answered.append((question,objects6))
		for f7 in commentAns:
			objects7 = Answer.objects.filter(Ans_No = f7.Ans_of_User)[0]
			question = Question.objects.filter(No = objects7.Ans_Of_Question)[0]
			comment_ans.append((question,objects7))
		for f8 in votedAns:
			objects8 = Answer.objects.filter(Ans_No = f8.Ans_of_User)[0]
			question = Question.objects.filter(No = objects8.Ans_Of_Question)[0]
			voted_ans.append((question,objects8))
		html = t.render(Context({'followed_users':followed_users,'follower_users':follower_users,'User':user,\
						'asked_que':asked_que,'followed_que':followed_que,'comment_que':comment_que,\
						'answered':answered,'comment_ans':comment_ans,'voted_ans':voted_ans,'islogin':request.session['isSuccessFlag']}))
	except KeyError:
		html = t.render(Context({'islogin':False}))
	return HttpResponse(html)

def other_home(request):
	if 'no' in request.GET:
		isfollowed = False
		other_id = request.GET['no']
		other_id= int(other_id.encode('ascii','ignore'))
		people = User.objects.filter(User_No=int(other_id))[0]#get other info
		followed_users = []
		follower_users = []
		asked_que = []
		followed_que = []
		comment_que = []
		answered = []
		comment_ans = []
		voted_ans = []
		my_followed_users = []
		my_follower_users = []
		my_asked_que = []
		my_followed_que = []
		my_comment_que = []
		my_answered = []
		my_comment_ans = []
		my_voted_ans = []
		try:
			followed = people.User_Followed.all()
			follower = people.User_Followers.all()
			askedQue = people.User_AskedQues.all()
			followedQue = people.User_FollowQues.all()
			commentQue = people.User_CommentQues.all()
			ans = people.User_Ans.all()
			commentAns = people.User_CommentAns.all()
			votedAns = people.User_VoteAns.all()
			for f1 in followed:
				objects1 = User.objects.filter(User_No = f1.Followed_User)[0]
				followed_users.append(objects1)
			for f2 in follower:
				objects2 = User.objects.filter(User_No = f2.Follower_User)[0]
				follower_users.append(objects2)
			for f3 in askedQue:
				objects3 = Question.objects.filter(No = f3.Asked_Question)[0]
				asked_que.append(objects3)
			for f4 in followedQue:
				objects4 = Question.objects.filter(No = f4.Follow_Question)[0]
				followed_que.append(objects4)
			for f5 in commentQue:
				objects5 = Question.objects.filter(No = f5.Comment_Question)[0]
				comment_que.append(objects5)
			for f6 in ans:
				objects6 = Answer.objects.filter(Ans_No = f6.Ans_of_User)[0]
				question = Question.objects.filter(No = objects6.Ans_Of_Question)[0]
				answered.append((question,objects6))
			for f7 in commentAns:
				objects7 = Answer.objects.filter(Ans_No = f7.Ans_of_User)[0]
				question = Question.objects.filter(No = objects7.Ans_Of_Question)[0]
				comment_ans.append((question,objects7))
			for f8 in votedAns:
				objects8 = Answer.objects.filter(Ans_No = f8.Ans_of_User)[0]
				question = Question.objects.filter(No = objects8.Ans_Of_Question)[0]
				voted_ans.append((question,objects8))
			if str(other_id) == str(request.session['user_id']):
				t = get_template('myhome.html')
				user = User.objects.filter(User_No = request.session['user_id'])[0]
				my_followed = user.User_Followed.all()
				my_follower = user.User_Followers.all()
				my_askedQue = people.User_AskedQues.all()
				my_followedQue = people.User_FollowQues.all()
				my_commentQue = people.User_CommentQues.all()
				my_ans = people.User_Ans.all()
				my_commentAns = people.User_CommentAns.all()
				my_votedAns = people.User_VoteAns.all()
				for f1 in my_followed:
					my_objects1 = User.objects.filter(User_No = f1.Followed_User)[0]
					my_followed_users.append(my_objects1)
				for f2 in my_follower:
					my_objects2 = User.objects.filter(User_No = f2.Follower_User)[0]
					my_follower_users.append(my_objects2)
				for f3 in my_askedQue:
					my_objects3 = Question.objects.filter(No = f3.Asked_Question)[0]
					my_asked_que.append(my_objects3)
				for f4 in my_followedQue:
					my_objects4 = Question.objects.filter(No = f4.Follow_Question)[0]
					my_followed_que.append(my_objects4)
				for f5 in my_commentQue:
					my_objects5 = Question.objects.filter(No = f5.Comment_Question)[0]
					my_comment_que.append(my_objects5)
				for f6 in my_ans:
					my_objects6 = Answer.objects.filter(Ans_No = f6.Ans_of_User)[0]
					my_question = Question.objects.filter(No = objects6.Ans_Of_Question)[0]
					my_answered.append((my_question,my_objects6))
				for f7 in my_commentAns:
					my_objects7 = Answer.objects.filter(Ans_No = f7.Ans_of_User)[0]
					my_question = Question.objects.filter(No = objects7.Ans_Of_Question)[0]
					my_comment_ans.append((my_question,my_objects7))
				for f8 in my_votedAns:
					my_objects8 = Answer.objects.filter(Ans_No = f8.Ans_of_User)[0]
					my_question = Question.objects.filter(No = objects8.Ans_Of_Question)[0]
					my_voted_ans.append((my_question,my_objects8))
				html = t.render(Context({'followed_users':my_followed_users,'follower_users':my_follower_users,'User':user,\
										'asked_que':my_asked_que,'followed_que':my_followed_que,'comment_que':my_comment_que,\
										'answered':my_answered,'comment_ans':my_comment_ans,'voted_ans':my_voted_ans,'islogin':request.session['isSuccessFlag']}))
			else:
				t = get_template('other_home.html')
				try:
					user = User.objects.filter(User_No = request.session['user_id'])[0]#get user
					user_no = user.User_No
					other_no = people.User_No
					if (follower.filter(Follower_User = user_no)):
						isfollowed = True
					html = t.render(Context({'followed_users':followed_users,'follower_users':follower_users,'isfollowed':isfollowed,'other':people,'user':user,\
									'asked_que':asked_que,'followed_que':followed_que,'comment_que':comment_que,\
									'answered':answered,'comment_ans':comment_ans,'voted_ans':voted_ans,'islogin':request.session['isSuccessFlag']}))
				except KeyError:
					html = t.render(Context({'followed_users':followed_users,'follower_users':follower_users,'other':people,\
									'asked_que':asked_que,'followed_que':followed_que,'comment_que':comment_que,\
									'answered':answered,'comment_ans':comment_ans,'voted_ans':voted_ans,'islogin':False}))
		except KeyError:
			t = get_template('other_home.html')
			html = t.render(Context({'followed_users':followed_users,'follower_users':follower_users,'other':people,\
									'asked_que':asked_que,'followed_que':followed_que,'comment_que':comment_que,\
									'answered':answered,'comment_ans':comment_ans,'voted_ans':voted_ans,'islogin':False}))
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def contact_user(request):
	if request.method == 'POST':
		num = request.POST['contact']
		if 'contact_context' in request.POST:
			isfollowed = False
			time = datetime.datetime.now()
			t = get_template('jump.html')
			text = request.POST['contact_context']
			to = User.objects.filter(User_No = num)[0]
			user = User.objects.filter(User_No = request.session['user_id'])[0]
			user_no = user.User_No
			newcontext = Contact_Info(receiver = to.User_No,sender = user.User_No,message = text,message_time = time)
			newcontext.save()
			to.User_MyMessage.add(newcontext)
			html = t.render(Context({'contact':True,'to':to}))
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)
		
		
def editUser(request):
	t = get_template('myhome_edit.html')
	user = User.objects.filter(User_No = request.session['user_id'])
	html = t.render(Context({'User':user[0]}))
	return HttpResponse(html)

def edit_detail(request):
	p_error = False
	n_error = False
	equal_error = False
	p1_error = False
	con_error = False
	user = User.objects.filter(User_No = request.session['user_id'])
	newuser = user[0]
	if request.method == 'POST':
		if (request.POST.has_key('text')) and (request.POST.has_key('password')) and (request.POST.has_key('password_con')) \
        and (request.POST.has_key('name')):
			description = request.POST['text']
			password = request.POST['password']
			password1 = request.POST['password_con']
			name = request.POST['name']
			if name and password and password1 and (password == password1):
				newuser.User_Name = name
				newuser.User_Pass = password
				if description:
					newuser.User_Description = description
				newuser.save()
				jump_f = True
				t = get_template('jump.html')
				html = t.render(Context({'ed_flag':jump_f}))
				return HttpResponse(html)
			else:
				if not name:
					n_error = True
				if password and password1 and (password != password1):
					equal_error = True
				if len(password)<6:
					p1_error = True
				if not password:
					p_error = True
				if (not password1) and password:
					con_error = True
	t = get_template('myhome_edit.html')
	html = t.render(Context({'User':newuser,'p_error':p_error,'n_error':n_error,'p1_error':p1_error,'con_error':con_error,'equal_error':equal_error}))
	return HttpResponse(html)
	
def ask(request):
	try:
		user = User.objects.filter(User_No = request.session['user_id'])[0]#get user
		t = get_template('ask.html')
		html = t.render(Context({'islogin':request.session['isSuccessFlag']}))
	except KeyError:
		t = get_template('login.html')
		html = t.render(Context({'islogin':False}))
	return HttpResponse(html)

def login(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    t = get_template('login.html')
    html = t.render(Context({}))
    return HttpResponse(html)

def register(request):
    t = get_template('register.html')
    html = t.render(Context({}))
    return HttpResponse(html)

def registerDetail(request):
    a_error = False
    p1_error = False
    p_error = False
    n_error = False
    equal_error = False
    con_error = False
    not_error = False
    not1_error = False
    email_f = True
    email1_f = True
    jump_f = False
    if request.method == 'POST':
        if (request.POST.has_key('Email_Address')) and (request.POST.has_key('Password')) and (request.POST.has_key('Password_con')) \
        and (request.POST.has_key('Username')):
            addr = request.POST['Email_Address']
            password = request.POST['Password']
            password1 = request.POST['Password_con']
            name = request.POST['Username']
            if ('@' and '.com') not in addr:
                email_f = False
            if User.objects.filter(User_Email = addr):
                email1_f = False
            if email_f and email1_f and addr and password and password1 and name and (password == password1) and (len(password)>=6):
				newuser = User(User_Name = name,User_Pass = password,User_Email = addr)
				newuser.save()
				jump_f = True
				return render_to_response("jump.html",{'re_flag':jump_f})
            else:
                if addr:
                    if not email_f:
                        not_error = True
                    elif not email1_f:
                        not1_error = True
                if not addr:
                    a_error = True
                if password and password1 and (password != password1):
                    equal_error = True
                if len(password)<6:
                    p1_error = True
                if not password:
                    p_error = True
                if not name:
                    n_error = True
                if (not password1) and password:
                    con_error = True
    return render_to_response('register.html',{'n_error':n_error,'a_error':a_error,'p_error':p_error,'con_error':con_error,'not_error':not_error,\
                                               'equal_error':equal_error,'p1_error':p1_error,'not1_error':not1_error,\
                                               'name':name,'addr':addr,'password':password,'password1':password1})

def loginDetail(request):
    e_error = False
    p_error = False
    if request.method == 'POST':
        email = request.POST['Email Address']
        password = request.POST['password']
        if User.objects.filter(User_Email = email):
            m = User.objects.get(User_Email = email)
            if m.User_Pass == password:
                request.session['user_id'] = m.User_No
                request.session['isSuccessFlag'] = True
                return render_to_response("jump.html",{'flag':request.session['isSuccessFlag']})
            else:
                p_error = True
        else:
            e_error = True
    return render_to_response("login.html",{'e_error':e_error,'p_error':p_error,\
                              'email':email})

def add_question(request):
	if request.method == "POST":
		title = request.POST['title']
		tag = Tag(Tag_Name = int(request.POST['tag']))
		if tag not in Tag.objects.all():
			tag.save()#----------------prepare for add new tag ,for eg. Internet<<Computer science
		else:
			tag = Tag.objects.filter(Tag_Name=int(request.POST['tag']))[0]
		description = request.POST['description']
		u_id = request.session['user_id']
		asker = Question_Asker(Asker = u_id)
		#if asker not in Question_Asker.objects.all():
		#	asker.save()#----------------prepare for add new tag ,for eg. Internet<<Computer science
		#else:
		#	asker = Question_Asker.objects.filter(Asker = u_id)
		asker.save()
		question = Question(Title = title,Description = description,Tags = tag, Asker = asker)
		question.save()
		now_user = User.objects.filter(User_No=u_id)[0]
		asked_ques = Asked_Question(Asked_Question=question.No)
		asked_ques.save()
		now_user.User_AskedQues.add(asked_ques)#add the question to user
		questions = Question.objects.all()#update the index
		t = get_template('index.html')
		match_answers_questions = {}
		for question in questions:
			answers = question.Answers.all()
			if answers:
				answer = random.choice(answers)
				provider = User.objects.filter(User_No=answer.Ans_Provider.Provider)#get answer provider's name
				match_answers_questions[question] = answer,provider[0]
			else:
				match_answers_questions[question] = None
		try:
			html = t.render(Context({'dict':match_answers_questions,'islogin':request.session['isSuccessFlag']}))#request.session['isSuccessFlag']
		except KeyError:
			html = t.render(Context({'dict':match_answers_questions,'islogin':False}))#request.session['isSuccessFlag']
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)
		
def answer_question(request):
	if 'no' in request.GET:
		no = request.GET['no']
		question = Question.objects.filter(No=no)[0]
		tag_name = question.Tags.Tag_Name
		tag_string = question.Tags.tag_choices[question.Tags.Tag_Name][1]
		t = get_template('answer_question.html')
		u_id = request.session['user_id']
		id_test = True
		now_user = User.objects.filter(User_No=u_id)[0]
		#answers = question.Answers.all()
		Answers = question.Answers.all()
		answers = []
		U_id = Answer_Voter(Voter=u_id)
		question_comment_display=[]
		question_comment_list = question.Comments.all()
		asker = User.objects.filter(User_No = question.Asker.Asker)[0]
		user_followed = Question_Follower(Follower = u_id)
		if user_followed not in question.Followers.all():
			follow_re='Follow'
		else:
			follow_re='Not Follow'
		for i in question_comment_list:
			ques_commenter = User.objects.filter(User_No = i.Commenter)[0]
			question_comment_display.append((i.Context,ques_commenter))
			print ques_commenter.User_No
		for e_Answer in Answers:
			ans_provider = User.objects.filter(User_No = e_Answer.Ans_Provider.Provider)[0]
			ans_comment_display = []
			comment_list = e_Answer.Ans_Comments.all()
			vote_all = e_Answer.Ans_Voters.all()
			vote_num = len(vote_all)
			for i in comment_list:
				ans_commenter = User.objects.filter(User_No = i.Commenter)[0]
				ans_comment_display.append((i.Context,ans_commenter))
			if U_id not in e_Answer.Ans_Voters.all():
				Praise='good'
				answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
			else:
				Praise='bad'
				answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
		try:
			html = t.render(Context({'follow':follow_re,'asker':asker,'q_comment':question_comment_display,'question':question,'tag_name':tag_name,'tag_string':tag_string,'answers':answers,'islogin':request.session['isSuccessFlag']}))
		except KeyError:
			html = t.render(Context({'follow':follow_re,'asker':asker,'q_comment':question_comment_display,'question':question,'tag_name':tag_name,'tag_string':tag_string,'answers':answers,'islogin':False}))
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def add_answer(request):
	if request.method == "POST":
		no = request.POST['no']
		question = Question.objects.filter(No=no)[0]
		asker = User.objects.filter(User_No = question.Asker.Asker)[0]
		tag = question.Tags.tag_choices[question.Tags.Tag_Name][1]
		time = datetime.datetime.now()
		if 'answer' in request.POST:
			context = request.POST['answer']
		else:
			context = False
		if 'ask_comment' in request.POST:
			ask_comment = request.POST['ask_comment']
		else:
			ask_comment = False
		if 'Ans_comment' in request.POST:
			Ans_comment = request.POST['Ans_comment']
		else:
			Ans_comment = False
		if 'praise' in request.POST:
			praise = request.POST['praise']
		else:
			praise = False
		if 'follow' in request.POST:
			follow = request.POST['follow']
		else:
			follow = False
		u_id = request.session['user_id']
		now_user = User.objects.filter(User_No=u_id)[0]
		error = False
		Answers = question.Answers.all()
		answers = []
		U_id = Answer_Voter(Voter=u_id)
		question_comment_display=[]
		question_comment_list = question.Comments.all()
		for i in question_comment_list:
			ques_commenter = User.objects.filter(User_No = i.Commenter)[0]
			question_comment_display.append((i.Context,ques_commenter))
		user_followed = Question_Follower(Follower = u_id)
		if user_followed not in question.Followers.all():
			follow_re='Follow'
		else:
			follow_re='Not Follow'
		#print answers
		#print context,ask_comment,Ans_comment,praise
		if not context:
			if not ask_comment:
				if not Ans_comment:
					if not praise:
						if not follow:
							t = get_template('jump.html')
							html = t.render(Context({'ans_flag':True,'question':question}))
							return HttpResponse(html)
						else:
							follow = request.POST['follow']
							if follow == 'Follow':
								ques_follower = Question_Follower(Follower = u_id)
								ques_follower.save()
								question.Followers.add(ques_follower)
								follow_question = Follow_Question(Follow_Question = question.No)
								follow_question.save()
								now_user.User_FollowQues.add(follow_question)
								now_user.save()
								question.save()
							else:
								if question.Followers:
									ques_choice_follower = Question_Follower.objects.filter(Follower = u_id)[0]
									question.Followers.remove(ques_choice_follower)
									question.save()
								if now_user.User_FollowQues:
									now_user_follow = Follow_Question.objects.filter(Follow_Question=question.No)[0]
									now_user.User_FollowQues.remove(now_user_follow)
									now_user.save()
							user_followed = Question_Follower(Follower = u_id)
							if user_followed not in question.Followers.all():
								follow_re='Follow'
							else:
								follow_re='Not Follow'
							for e_Answer in Answers:
								ans_provider = User.objects.filter(User_No = e_Answer.Ans_Provider.Provider)[0]
								ans_comment_display = []
								comment_list = e_Answer.Ans_Comments.all()
								vote_all = e_Answer.Ans_Voters.all()
								vote_num = len(vote_all)
								for i in comment_list:
									ans_commenter = User.objects.filter(User_No = i.Commenter)[0]
									ans_comment_display.append((i.Context,ans_commenter))
								if U_id not in e_Answer.Ans_Voters.all():
									Praise='good'
									answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
								else:
									Praise='bad'
									answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
							question.save()
							t = get_template('jump.html')
							html = t.render(Context({'ans_flag':True,'question':question}))
							return HttpResponse(html)
					else:
						ok = request.POST['ok']
						answer_choice=Answer.objects.filter(Ans_No=praise)[0]
						if ok=='good':
							ans_voter = Answer_Voter(Voter = u_id)
							ans_voter.save()
							answer_choice.Ans_Voters.add(ans_voter)
							answer_choice.save()
							new_vote=Vote_Ans_of_User(Ans_of_User=answer_choice.Ans_No)
							new_vote.save()
							now_user.User_VoteAns.add(new_vote)
							now_user.save()
						else:
							if answer_choice.Ans_Voters:
								answer_choice_vote = Answer_Voter.objects.filter(Voter = u_id)[0]
								#answer_choice_vote.remove()
								answer_choice.Ans_Voters.remove(answer_choice_vote)
								answer_choice.save()
							if now_user.User_VoteAns:
								now_user_vote=Vote_Ans_of_User.objects.filter(Ans_of_User=answer_choice.Ans_No)[0]
								#now_user_vote.remove()
								now_user.User_VoteAns.remove(now_user_vote)
								now_user.save()
						for e_Answer in Answers:
							ans_provider = User.objects.filter(User_No = e_Answer.Ans_Provider.Provider)[0]
							ans_comment_display = []
							comment_list = e_Answer.Ans_Comments.all()
							vote_all = e_Answer.Ans_Voters.all()
							vote_num = len(vote_all)
							for i in comment_list:
								ans_commenter = User.objects.filter(User_No = i.Commenter)[0]
								ans_comment_display.append((i.Context,ans_commenter))
							if U_id not in e_Answer.Ans_Voters.all():
								Praise='good'
								answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
							else:
								Praise='bad'
								answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
						question.save()
						t = get_template('jump.html')
						html = t.render(Context({'ans_flag':True,'question':question}))
						return HttpResponse(html)
				else:
					comment = request.POST['comment']
					answer_comment = Answer_Comment(Commenter = u_id,Context=comment,VotersNum=0)
					answer_comment.save()
					answer_choice=Answer.objects.filter(Ans_No=Ans_comment)[0]
					answer_choice.Ans_Comments.add(answer_comment)
					answer_choice.save()
					new_comment_answer = Comment_Ans_of_User(Ans_of_User=answer_choice.Ans_No)
					new_comment_answer.save()
					now_user.User_CommentAns.add(new_comment_answer)
					now_user.save()
					question.save()
					question_comment_display=[]
					question_comment_list = question.Comments.all()
					for i in question_comment_list:
						ques_commenter = User.objects.filter(User_No = i.Commenter)[0]
						question_comment_display.append((i.Context,ques_commenter))
					#answers = question.Answers.all()
					for e_Answer in Answers:
						ans_provider = User.objects.filter(User_No = e_Answer.Ans_Provider.Provider)[0]
						ans_comment_display = []
						comment_list = e_Answer.Ans_Comments.all()
						vote_all = e_Answer.Ans_Voters.all()
						vote_num = len(vote_all)
						for i in comment_list:
							ans_commenter = User.objects.filter(User_No = i.Commenter)[0]
							ans_comment_display.append((i.Context,ans_commenter))
						if U_id not in e_Answer.Ans_Voters.all():
							Praise='good'
							answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
						else:
							Praise='bad'
							answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
					t = get_template('jump.html')
					html = t.render(Context({'ans_flag':True,'question':question}))
					return HttpResponse(html)
			else:
				question_comment = Question_Comment(Commenter=u_id,Context=ask_comment,VotersNum=0)
				question_comment.save()
				question.Comments.add(question_comment)
				new_comment_question = Comment_Question(Comment_Question = no)
				if new_comment_question not in Comment_Question.objects.all():
					new_comment_question.save()
				else:
					new_comment_question = Comment_Question.objects.filter(Comment_Question = no)
				test = False
				for i in now_user.User_CommentQues.all():
					if int(new_comment_question.Comment_Question) == int(i.Comment_Question):
						test=True
				if test == False:
					now_user.User_CommentQues.add(new_comment_question)
				now_user.save()
				question.save()
				#answers = question.Answers.all()
				for e_Answer in Answers:
					ans_provider = User.objects.filter(User_No = e_Answer.Ans_Provider.Provider)[0]
					ans_comment_display = []
					comment_list = e_Answer.Ans_Comments.all()
					vote_all = e_Answer.Ans_Voters.all()
					vote_num = len(vote_all)
					for i in comment_list:
						ans_commenter = User.objects.filter(User_No = i.Commenter)[0]
						ans_comment_display.append((i.Context,ans_commenter))
					if U_id not in e_Answer.Ans_Voters.all():
						Praise='good'
						answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
					else:
						Praise='bad'
						answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
				t = get_template('jump.html')
				html = t.render(Context({'ans_flag':True,'question':question}))
				return HttpResponse(html)
		else:
			provider = Answer_Provider(Provider = u_id)
			provider.save()
			new_answer = Answer(Ans_Time = time,Ans_Context=context,Ans_Of_Question = no,Ans_Provider=provider)
			new_answer.save()   
			new_ans_user = Ans_of_User(Ans_of_User=new_answer.Ans_No)
			new_ans_user.save()
			now_user.User_Ans.add(new_ans_user)
			now_user.save()
			question.Answers.add(new_answer)
			question.save()
			#answers = question.Answers.all()
			for e_Answer in Answers:
				ans_provider = User.objects.filter(User_No = e_Answer.Ans_Provider.Provider)[0]
				ans_comment_display = []
				comment_list = e_Answer.Ans_Comments.all()
				vote_all = e_Answer.Ans_Voters.all()
				vote_num = len(vote_all)
				for i in comment_list:
					ans_commenter = User.objects.filter(User_No = i.Commenter)[0]
					ans_comment_display.append((i.Context,ans_commenter))
				if U_id not in e_Answer.Ans_Voters.all():
					Praise='good'
					answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
				else:
					Praise='bad'
					answers.append((e_Answer,Praise,ans_comment_display,vote_num,ans_provider))
			t = get_template('jump.html')
			html = t.render(Context({'ans_flag':True,'question':question}))
			return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def follow_user(request):
	if request.method == 'POST':
		num = request.POST['follow']
		to = User.objects.filter(User_No = num)[0]
		user = User.objects.filter(User_No = request.session['user_id'])[0]
		newFollowed = Followed_User(Followed_User = to.User_No)
		newFollowed.save()
		newFollower = Follower_User(Follower_User = user.User_No)
		newFollower.save()
		to.User_Followers.add(newFollower)
		user.User_Followed.add(newFollowed)
		t = get_template('jump.html')
		html = t.render(Context({'follow_flag':True,'to':to}))
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def cancel_follow(request):
	if request.method == 'POST':
		num = request.POST['follow']
		to = User.objects.filter(User_No = num)[0]
		user = User.objects.filter(User_No = request.session['user_id'])[0]
		cancel_followed = Followed_User.objects.filter(Followed_User = to.User_No)[0]
		cancel_follower = Follower_User.objects.filter(Follower_User = user.User_No)[0]
		to.User_Followers.remove(cancel_follower)
		user.User_Followed.remove(cancel_followed)
		t = get_template('jump.html')
		html = t.render(Context({'unfollow_flag':True,'to':to}))
		return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)
		
def tag_details(request):
	if 'tag_name' in request.GET:
			tag_name = request.GET['tag_name']
			tag_name= int(tag_name.encode('ascii','ignore'))
			tag = Tag.objects.filter(Tag_Name=tag_name)[0]
			tag_description = tag.Tag_Description
			tag_string = Tag.tag_choices[tag_name][1]
			t = get_template('tag_details.html')
			try:
				html = t.render(Context({'tag_string':tag_string,'tag_description':tag_description,'islogin':request.session['isSuccessFlag']}))
			except KeyError:
				html = t.render(Context({'tag_string':tag_string,'tag_description':tag_description,'islogin':False}))
			return HttpResponse(html)
	else:
		t = get_template('404.html')
		html = t.render(Context({}))
		return HttpResponse(html)

def ajax(request):
        if 'q' in request.GET and request.GET['q']:
                q=request.GET['q']
                questions= Question.objects.filter(Title__icontains=q)
                return render(
                        request,
                        'search.html',
                        context_instance = RequestContext(request,
                        {
                            'questions': questions,
                        })
        )
        else:
                return render(
                request,
                'search.html',
                context_instance = RequestContext(request,
                {
                    'questions': [],
                })
        )

def ajax_index(request):
        if 'q' in request.GET and request.GET['q']:
                q=request.GET['q']
                questions= Question.objects.filter(Title__icontains=q)
                return render(
                        request,
                        'search_index.html',
                        context_instance = RequestContext(request,
                        {
                            'questions': questions,
                        })
        )
        else:
                return render(
                request,
                'search_index.html',
                context_instance = RequestContext(request,
                {
                    'questions': [],
                })
        )

def logout(request):
    del request.session['user_id']
    request.session['isSuccessFlag'] = False
    return render_to_response("jump.html")






