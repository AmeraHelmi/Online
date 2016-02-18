from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core import serializers
from myapp.models import *
import os , random , json , unicodedata , time
from time import gmtime, strftime
# from PIL import Image
from collections import defaultdict
from myapp.forms import *
from random import randrange
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail

##########################################################################

def start(request):
	# main function of index
	news=New.objects.all()
	username=request.session.get('username')
	role=request.session.get('role')
	return render(request,'index.html',{'news':news,'username':username,'role':role})

##########################################################################

def statics_course(request):
	# open statistics of course
	all_courses=Course.objects.all()
	ids_courses=Course.objects.all().values_list('id',flat=True)
	res=[]
	courses_names=[]
	for c_id in ids_courses:
		course_obj=Course.objects.get(id=c_id)
		courses_names.append(course_obj.course_name.encode('UTF-8'))
	for c_id in ids_courses:
		course_obj=Course.objects.get(id=c_id)
		res.append(Exam.objects.filter(course=course_obj).count())

	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'st_courses.html',{'courses':all_courses,'no_exams':res,'ids':courses_names,'username':username,'role':role})

##########################################################################

def statics_student(request):
	# open statistics of student
	all_users=User.objects.all()
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'st_students.html',{'users':all_users,'username':username,'role':role})

##########################################################################

def search_course(request,cid):
	# search course
	obj=Course.objects.get(id=cid)
	no_questions=Question.objects.filter(course=obj).count()
	print("no_questions: ",no_questions)
	no_students=0
	arr_students=[]
	no_exams=Exam.objects.filter(course=obj).count()
	ids_exams=Exam.objects.filter(course=obj).values_list('id',flat=True)
	for i in range(no_exams):
		exam_id=ids_exams[i]
		print("Exam_id: ",exam_id)
		exam_obj=Exam.objects.get(id=exam_id)
		users=Trie.objects.values_list('user',flat=True).filter(exam=exam_obj)
		for j in range(users.count()):
			user_id=users[j]
			if user_id not in arr_students:
				print("user_id: ",user_id)
				arr_students.append(user_id)
		
	print("no_students: ",len(arr_students))
	no_students=len(arr_students)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'course_detail.html',{'course':obj,'username':username,'role':role,'no_questions':no_questions,'no_students':no_students})

##########################################################################

def search_student(request,uid):
	# search student
	obj=User.objects.get(id=uid)
	no_exams=Trie.objects.filter(user=obj).count()
	print("no_exams: ",no_exams)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'student_detail.html',{'user':obj,'username':username,'role':role,'no_exams':no_exams})

##########################################################################

def standard(request):
	# to display page of standards
	username=request.session.get('username')
	role=request.session.get('role')
	return render(request,"standard.html",{'username':username,'role':role})

##########################################################################

def list_files(request):
	# to test list of files
	files=UploadFile.objects.all()
	return render(request,"test_list.html",{'files':files})

##########################################################################

def savefile(request):
	# to test save file
	_file=request.FILES["myfile"]
	handle=open('testfile.txt','w+')
	handle.write(_file)
	handle.close()
	return HttpResponse("Done")

##########################################################################

def what_do(request):
	# to display page of what_do
	username=request.session.get('username')
	role=request.session.get('role')
	return render(request,'what_do.html',{'username':username,'role':role})

##########################################################################

def exam(request):
	# get all question and display random with their answers
	username=request.session.get('username')
	role=request.session.get('role')
	return render(request,'exam.html',{'username':username,'role':role})

##########################################################################

def test_file(request,test_file,cid):
	# to test upload file and extract question and answers 
	handle1=open("questions.txt","w+")
	handle2=open("answers.txt","w+")
	content_question=""
	content_answer=""
	cobj=Course.objects.get(id=cid)
	count=open(test_file).read().count("Q: ")
	print "number of questions is: ",str(count) 
	sections = open("file.txt").read().split("=====================")
	for item in range(count):
		print "question" ,str(item+1)
		print sections[item]
		sub_sections=sections[item].split("?")
		print "question is: ",sub_sections[0]
		content_question="\n question"+str(item+1)+" is:\n "+sub_sections[0]
		content_questions=sub_sections[0].split("Q:")
		if Question.objects.filter(question_text = content_questions[1],course=cobj).exists():
			Question_xx=Question.objects.get(question_text=content_questions[1],course=cobj)
		else:
			x=Question(question_text=content_questions[1],num=(item+1),course=cobj)
			x.save()
		content_answer="answers for question"+str(item+1)+" are:"+sub_sections[1]
		content_answers=sub_sections[1].split("*")
		Question_xx=Question.objects.get(question_text=content_questions[1],course=cobj)
		for answer in content_answers:
			y=Choice(choice_text=answer,question_text=Question_xx,question=Question_xx)
			y.save()
		handle1.write(content_question)
		handle2.write(content_answer)
		print "answers are: ",sub_sections[1]
	handle1.close()
	handle2.close()
	return render(request,'test.html')

##########################################################################

def grades(request,uid):
	# get grades of student in exams
	user_obj=User.objects.get(id=uid)
	Trie_objs=Trie.objects.filter(user=user_obj)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'grades.html',{'username':username,'role':role,'grades':Trie_objs,'user_obj':user_obj})

##########################################################################

def profile(request):
	# display profile of specific user
	username=request.session.get("username")
	obj=User.objects.get(user_name=username)
	age=obj.user_age
	uid=obj.id
	email=obj.user_email
	password=obj.user_password
	role=obj.user_role
	# img=obj.user_img
	# return render(request,'profile.html',{'user_id':uid,'username':username,'email':email,'password':password,'role':role,'img':img})
	return render(request,'profile.html',{'user_id':uid,'username':username,'email':email,'password':password,'role':role})

##########################################################################

def profile_id(request,uid):
	# display all users in system
	status="not profiling"
	obj=User.objects.get(id=uid)
	age=obj.user_age
	uid=obj.id
	email=obj.user_email
	password=obj.user_password
	urole=obj.user_role
	# img=obj.user_img
	uname=obj.user_name
	username=request.session.get("username")
	role=request.session.get("role")
	# return render(request,'profile.html',{'status':status,'uname':uname,'role':role,'user_id':uid,'username':username,'email':email,'password':password,'urole':urole,'img':img})
	return render(request,'profile.html',{'status':status,'uname':uname,'role':role,'user_id':uid,'username':username,'email':email,'password':password,'urole':urole})

##########################################################################

def statics_courses(request,cid):
	user_obj=User.objects.get(id=cid)
	user_name=user_obj.user_name
	exams=Trie.objects.filter(user=user_obj).values_list('exam',flat=True)
	courses=[]
	for exam in exams:
		courses.append(exam.course.course_name)
	exams_dates=Trie.objects.filter(user=user_obj).values_list('exam_date',flat=True)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'st_detail.html',{'username':username,'role':role,'courses':courses,'dates':exams_dates,'user_name':user_name})
##########################################################################	

def editanswer(request,aid):
	# edit choice
	obj=Choice.objects.get(id=aid)
	username=request.session.get("username")
	role=request.session.get("role")
	text=obj.choice_text
	status=obj.status
	ans_id=obj.id
	return render(request,'editanswer.html',{'obj_id':ans_id,'username':username,'role':role,'text':text,'status':status})

##########################################################################

def editans(request,aid):
	# edit choise
	obj=Choice.objects.get(id=aid)
	qobj=obj.question
	answers=Choice.objects.filter(question=qobj)
	if request.method == 'POST':
		if request.POST.get("aname"):
			answer_new=request.POST.get("aname")
			if Choice.objects.filter(choice_text=answer_new).exists():
				answers=Choice.objects.filter(question=qobj)
			else:
				obj.choice_text='  '+answer_new
				obj.save()
	answers=Choice.objects.filter(question=qobj)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'q_detail.html',{'question':qobj,'answers':answers,'username':username,'role':role})

##########################################################################

def contacts(request):
	# display page of contacts
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'contact.html',{'username':username,'role':role})

##########################################################################

def course_delete(request,cid):
	# delete specific course
	Course.objects.filter(id=cid).delete()
	all_courses=Course.objects.all()
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'courses.html',{'courses':all_courses,'username':username,'role':role})

##########################################################################

def user_delete(request,uid):
	# delete specific user
	User.objects.filter(id=uid).delete()
	users=User.objects.filter(user_role="Student")
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'list_students.html',{'users':users,'role':role,'username':username})

##########################################################################

def delanswer(request,aid):
	# delete specific choice
	a_obj=Choice.objects.get(id=aid)
	obj=a_obj.question
	Choice.objects.filter(id=aid).delete()
	answers=Choice.objects.filter(question=obj)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'q_detail.html',{'question':obj,'answers':answers,'username':username,'role':role})

##########################################################################

def user_add(request):
	# render add.html to add new user
	if request.method == 'POST':
		role=request.session.get("role")
		username=request.session.get("username")
		return render(request,'add.html',{'username':username,'role':role})

##########################################################################

def useradd(request):
	# add new user
	if request.method == 'POST':
		uname=request.POST.get("uname")
		upass=request.POST.get("upass")
		uemail=request.POST.get("uemail")
		# if 'uimg' in request.FILES:
		# 	uimg=request.FILES['uimg']
		#  	User_obj=User(user_name=uname,user_password=upass,user_email=uemail,user_img=uimg)
		#  	User_obj.save()
		# else:
		User_obj=User(user_name=uname,user_password=upass,user_email=uemail)
		User_obj.save()
		username=request.session.get("username")
		users=User.objects.filter(user_role="Student")
		role=request.session.get("role")
		username=request.session.get("username")

		return render(request,'list_students.html',{'users':users,'role':role,'username':username})
	else:
		role=request.session.get("role")
		username=request.session.get("username")
		return render(request,'add.html',{'username':username,'role':role})

##########################################################################

def user_update(request,uid):
	# update user information
	obj=User.objects.get(id=uid)
	asd=""
	if request.method == 'POST':
		if request.POST.get("uname"):
			obj.user_name=request.POST.get("uname")
			request.session["username"]=request.POST.get("uname")
		if request.POST.get("uemail"):
			obj.user_email=request.POST.get("uemail")
		if request.POST.get("upass"):
			obj.user_password=request.POST.get("upass")
			# logout(request)
			obj.save()
			return logout(request)
		# if 'uimg' in request.FILES:
		# 	obj.user_img=request.FILES['uimg']

		obj.save()
		username=request.session.get("username")
		obj=User.objects.get(user_name=username)
		age=obj.user_age
		uid=obj.id
		email=obj.user_email
		password=obj.user_password
		role=obj.user_role
		# img=obj.user_img
		# return render(request,'profile.html',{'user_id':uid,'username':username,'email':email,'password':password,'role':role,'img':img})
		return render(request,'profile.html',{'user_id':uid,'username':username,'email':email,'password':password,'role':role})

	
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'update.html',{'user':obj,'username':username,'role':role})

##########################################################################

def get_random(request):
	# test random function
	rand_num= random.randint(1, 10)
	if Question.objects.filter(num=rand_num).exists():
		text=Question.objects.get(num=rand_num)
		tt=text.question_text
	else:
		tt="not found"
	return render(request,'rand.html',{'random':rand_num,'text':tt})

##########################################################################

def course_detail(request,cid):
	# display course information
	obj=Course.objects.get(id=cid)
	no_questions=Question.objects.filter(course=obj).count()
	count=3
	i=1
	arr=[]
	if no_questions :
		questions=Question.objects.filter(course=obj)
		for question in questions:
			arr.append(question.id)
		d=defaultdict(list)
		random_index = randrange(0,len(arr))
		randnum=arr[random_index]
		for x in range(0,count):
			random_index = randrange(0,len(arr))
			randnum=arr[random_index]
			if Question.objects.filter(id=randnum).exists():
				i=i+1
				question=Question.objects.get(id=randnum)
				answers=Choice.objects.filter(question=question)
				for answer in answers:
					d[question.question_text].append(answer.choice_text)
					
			else:
				i=i+1
				
		questions=Question.objects.filter(course=obj)
		username=request.session.get("username")
		role=request.session.get("role")
		dic = dict(d)
		return render(request,'single.html',{'course':obj,'questions':questions,'username':username,'role':role,'no_questions':no_questions,'dic':dic,'arr':arr})
	else:
		username=request.session.get("username")
		role=request.session.get("role")
		return render(request,'single.html',{'course':obj,'username':username,'role':role,'no_questions':no_questions})

##########################################################################

def newexam(request,cid):
	# start new exam
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'new_exam.html',{'username':username,'role':role,'course_id':cid})

##########################################################################

def exams(request):
	# get all exams in course
	all_courses=Course.objects.all()
	all_exams=Exam.objects.all()
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'exam.html',{'courses':all_courses,'role':role,'username':username,'all_exams':all_exams})
##########################################################################

def exam_delete(request,cid):
	# delete specific exam
	Exam.objects.filter(id=cid).delete()
	all_courses=Course.objects.all()
	all_exams=Exam.objects.all()
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'exam.html',{'courses':all_courses,'role':role,'username':username,'all_exams':all_exams})

##########################################################################

def take_exam(request,cid):
	#determine exam
	course_obj=Course.objects.get(id=cid)
	# get exam id randomly from Exam table
	ids = Exam.objects.filter(course=course_obj).values_list('id',flat=True)
	print("ids",ids)
	rand_num= random.choice (ids)
	print("random number: ",rand_num)

	questions=MCQ.objects.filter(exam=rand_num)
	ans_arr=[]
	dic={}
	no_questions=questions.count()
	print("number of questions: ",no_questions)
	for question in questions:
 		print("question_text:",question.question.question_text)
 		ans_arr=[]
 		x=question.question.question_text
 		x=unicodedata.normalize('NFKD', x).encode('ascii','ignore')
 		print("str: ",x)
 		qobj=Question.objects.get(id=question.question.id)
 		answers=Choice.objects.filter(question=qobj)
		no_answers=answers.count()
		count=0
		if no_answers:
			for j in range(no_answers):
				ans_arr.append(answers[count])
				count=count+1
	 	else:
				ans_arr=[]
		if ans_arr:
				dic[x]=ans_arr
		
	role=request.session.get("role")
	username=request.session.get("username")
	request.session['exam_id']=rand_num
	return render(request,'take_exam.html',{'exam_id':rand_num,'role':role,'username':username,'questions':questions,'dic':dic})

##########################################################################

def result(request,score):
	# get grade for exam
	user_obj=User.objects.get(user_name=request.session.get("username"))
	exam_obj=Exam.objects.get(id=request.session.get("exam_id"))
	score=int(score)
	date_now=time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
	trie=Trie(grade=score,user=user_obj,exam=exam_obj,exam_date=date_now)
	trie.save()
	news=New.objects.all()
	username=request.session.get('username')
	role=request.session.get('role')
	return render(request,'index.html',{'news':news,'username':username,'role':role})

##########################################################################

def addexam(request,cid):
	# add new exam
	obj=Course.objects.get(id=cid)
	dic={}
	myarray=[]
	ans_arr=[]
	msg=""
	no_questions=Question.objects.filter(course=obj).count()
	print("no_questions",no_questions)
	if request.method == 'POST':
		Qnumber=request.POST.get("Qnumber")
		if no_questions:
			ids = Question.objects.filter(course=obj).values_list('id',flat=True)
			print("ids",ids)
			rand_num= random.choice (ids)
			print("rand_num for first ",rand_num)
			if int(Qnumber) <= (no_questions):
				exam_title="Exam"+str(Qnumber)
				print("Exam_title",exam_title)
				exam_obj=Exam(title=exam_title,course=obj)
				exam_obj.save()
				# print("range",range(int(Qnumber)))
 				for i in range(int(Qnumber)):
					# print(rand_num)
 					qobj=Question.objects.get(course=obj,id=rand_num)
 					# rand_num= random.choice(ids)
 					print("question_text:",qobj.question_text)
 					status=check_element(qobj,myarray)
 					ans_arr=[]
 					while status:
 						rand_num= random.choice(ids)
						# print(rand_num)
 						qobj=Question.objects.get(course=obj,id=rand_num)
 						status=check_element(qobj,myarray)
 					x=qobj.question_text
 					x=unicodedata.normalize('NFKD', x).encode('ascii','ignore')
 					print("str: ",x)
 					mcq_obj=MCQ(exam=exam_obj,question=qobj)
 					mcq_obj.save()	
 			else:
 				msg="no.questions is less than you determined!"

 		else:
 			msg="no questions here"

		all_courses=Course.objects.all()
		all_exams=Exam.objects.all()
		role=request.session.get("role")
		username=request.session.get("username")
		return render(request,'exam.html',{'msg':msg,'courses':all_courses,'role':role,'username':username,'questions':myarray,'all_exams':all_exams})

##########################################################################

def list_exams(request,cid):
	# list all exams
	exams=Exam.objects.all()
	username=request.session.get("username")
	role=request.session.get("role")
	return  render(request,'list_exams.html',{'username':username,'role':role,'exams':exams})

##########################################################################

def check_element(qobj,myarray):
	# check element in array
	if qobj in myarray:
		return True
	else:
		myarray.append(qobj)
		return False

##########################################################################

def question_detail(request,qid):
	# display question detail
	obj=Question.objects.get(id=qid)
	answers=Choice.objects.filter(question=obj)
	if request.method == 'POST':
		answer_new=request.POST.get("aname")
		if Choice.objects.filter(choice_text=answer_new,question=obj).exists():
			answers=Choice.objects.filter(question=obj)
		else:	

			# enter status in db
			if 'status' in request.POST:
				ss=request.POST['status']
				x=Choice(choice_text=answer_new,question=obj,status=ss)
				x.save()
			else:
				x=Choice(choice_text=answer_new,question=obj)
				x.save()

			answers=Choice.objects.filter(question=obj)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'q_detail.html',{'question':obj,'answers':answers,'username':username,'role':role})

##########################################################################

def registeration(request):
	# to register in system
	if request.method == 'POST':
	 	u_name=request.POST.get("usernamesignup")
		u_email=request.POST.get("emailsignup")
	 	u_pass=request.POST.get("passwordsignup")
	 	u_obj=User(user_name=u_name,user_email=u_email,user_password=u_pass)
	 	u_obj.save()
	 	# request.session['username']=u_name
		# request.session['role']=u_obj.user_role
	news=New.objects.all()
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'index.html',{'news':news,'username':username,'role':role})

##########################################################################

def reg(request):
	# open registeration form
	return render(request,'reg.html')

##########################################################################

def  logout(request):
	# clear session and logout 
	del request.session["username"]
	del request.session["role"]
	news=New.objects.all()
	username=request.session.get("username")
	return render(request,'index.html',{'news':news,'username':username})

##########################################################################

def login(request):
	# login page
	if request.method == 'POST':
		u_email=request.POST.get("user_email")
	 	u_pass=request.POST.get("password")
	 	if User.objects.filter(user_email=u_email,user_password=u_pass).exists():
	 		obj=User.objects.get(user_email=u_email,user_password=u_pass)
	 		request.session["username"]=obj.user_name
	 		request.session["role"]=obj.user_role
	 	else:
	 		request.session["username"]=""
	news=New.objects.all()
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'index.html',{'news':news,'username':username,'role':role})

##########################################################################

def get_name(request):
    # test upload file
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            objfile=UploadFile(myfile=request.FILES['myfile'])
            objfile.save()
            news=New.objects.all()
            username=request.session.get('username')
            role=request.session.get('role')
            return render(request,'index.html',{'news':news,'username':username,'role':role})

    
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadFileForm()

    return render(request, 'test.html', {'form': form})

##########################################################################

def question_list(request,cid):
	# to list all questions
	obj=Course.objects.get(id=cid)
	if request.method == 'POST':
		question_new=request.POST.get("qname")
		if Question.objects.filter(question_text=question_new,course=obj).exists():
			questions=Question.objects.filter(course=obj)
		else:	
			x=Question(question_text=question_new,num=4,course=obj)
			x.save()
			questions=Question.objects.filter(course=obj)
	username=request.session.get("username")
	role=request.session.get("role")
	return render(request,'single.html',{'course':obj,'questions':questions,'role':role,'username':username})

##########################################################################

def question_upload(request,cid):
	# to upload questions from file
	obj=Course.objects.get(id=cid)
	if request.method == 'POST':
		content=""
		questions_count=0
		sections=""
		content_question=""
		content_answer=""
		sub_sections=""
		form = UploadFileForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            objfile=UploadFile(myfile=request.FILES['myfile'],course=obj)
            objfile.save()
            for f in request.FILES['myfile'].chunks():
            	content+=f
            questions_count=content.count("Q: ")
            print("questions_count: ",questions_count)
            	# till now all things right
            sections=content.split("=========================================================")
            i=1
            for item in range(questions_count):
            	# print ("section:",sections[item])
            	sub_sections=sections[item].split("?")
            	print "question is: ",sub_sections[0].split("Q:\r\n")
            	content_question="\n question"+str(item+1)+" is:\n "+sub_sections[0]
            	content_questions=sub_sections[0].split("Q:")
            	if Question.objects.filter(question_text = content_questions[1],course=obj).exists():
            		Question_xx=Question.objects.get(question_text=content_questions[1],course=obj)
            	else:
            		x=Question(question_text=content_questions[1],num=(item+1),course=obj)
            		x.save()
            	content_answer="answers for question"+str(item+1)+" are: \n"+sub_sections[1]
            	# print("content_answer: ",content_answer)
            	content_answers=sub_sections[1].split("\n")
            	Question_xx=Question.objects.get(question_text=content_questions[1],course=obj)
            	for answer in content_answers:
            		if answer.startswith( '*' ):
            			ss=answer.split('*')
            			print("choice: ",ss[1], " ---> false")
            			if Choice.objects.filter(choice_text=ss[1],question=Question_xx).exists():
            				ss[1]=""
            			else:
            				y=Choice(choice_text=ss[1],question=Question_xx,status=False)
            				y.save()
            		if answer.startswith( '$' ):
            			ss=answer.split('$')
            			print("choice: ",ss[1], " ---> true")
            			if Choice.objects.filter(choice_text=ss[1],question=Question_xx).exists():
            				ss[1]=""
            			else:
            				y=Choice(choice_text=ss[1],question=Question_xx,status=True)
            				y.save()

            # 		if Choice.objects.filter(choice_text=answer,question=Question_xx).exists():
	           # #  			content_answers=""
	           # #  		else:
	           # #  			print "answer: ",answer
	           # #  			y=Choice(choice_text=answer,question=Question_xx)
	           # #  			y.save()

            # # sections=content.split("=====================")
            # for item in range(questions_count):
            # 	print ("section:",sections[item])
            # 	sub_sections=sections[item].split("?")
            # 	print "question is: ",sub_sections[0]
            # 	content_question="\n question"+str(item+1)+" is:\n "+sub_sections[0]
            # 	content_questions=sub_sections[0].split("Q:")
            # 	if Question.objects.filter(question_text = content_questions[1],course=obj).exists():
            # 		Question_xx=Question.objects.get(question_text=content_questions[1],course=obj)
            # 	else:
            # 		x=Question(question_text=content_questions[1],num=(item+1),course=obj)
            # 		x.save()
            # 	content_answer="answers for question"+str(item+1)+" are: \n"+sub_sections[1]
            # 	content_answers=sub_sections[1].split("* ")
            # 	Question_xx=Question.objects.get(question_text=content_questions[1],course=obj)
            # 	for answer in content_answers:
            # 		if answer:
	           #  		if Choice.objects.filter(choice_text=answer,question=Question_xx).exists():
	           #  			content_answers=""
	           #  		else:
	           #  			print "answer: ",answer
	           #  			y=Choice(choice_text=answer,question=Question_xx)
	           #  			y.save()
	           #  	else:
	           #  		answer=""
            username=request.session.get('username')
            role=request.session.get('role')
            questions=Question.objects.filter(course=obj)
            return render(request,'single.html',{'course':obj,'questions':questions,'username':username,'role':role,'sections':sections,'content_question':content_question})
    	else:
        	form = UploadFileForm()

    	return render(request, 'test.html', {'form': form,'cid':cid})			

##########################################################################
	
def courses(request):
	#  to list all courses
	all_courses=Course.objects.all()
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'courses.html',{'courses':all_courses,'role':role,'username':username})

##########################################################################

def students(request):
	#  to list all students
	users=User.objects.filter(user_role="Student")
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'list_students.html',{'users':users,'role':role,'username':username})

##########################################################################

def staff(request):
	#  to display staff page 
	users=User.objects.filter(user_role="Instructor")
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'staff.html',{'users':users,'role':role,'username':username})

##########################################################################

def list_users(request):
	# list all users
	users=User.objects.all()
	role=request.session.get("role")
	username=request.session.get("username")
	return render(request,'list_students.html',{'users':users,'role':role,'username':username})

##########################################################################
def sendemail(request):
	if request.method == 'POST':
		subject=request.POST.get("subject")
		message=request.POST.get("subject")
		from_email=request.POST.get("email")

		if send_mail(subject, message, from_email,['amera.elsayed6@gmail.com'], fail_silently=False):
			news=New.objects.all()
			username=request.session.get('username')
			role=request.session.get('role')
			return render(request,'index.html',{'news':news,'username':username,'role':role})



##########################################################################

def list_course(request):
	# take input from post and add new course then list
	if request.method == 'POST':
		course_new=request.POST.get("cname")
		if Course.objects.filter(course_name=course_new).exists():
			courses=Course.objects.all()
		else:	
			x=Course(course_name=course_new)
			x.save()
			courses=Course.objects.all()
		role=request.session.get("role")
		username=request.session.get("username")
		return render(request,'courses.html',{'courses':courses,'role':role,'username':username})