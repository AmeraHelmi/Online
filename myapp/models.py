from django.db import models

STUDENT = 'Student'
INSTRUCTOR = 'Instructor'
TITLE_CHOICES = (
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
      
    )
# Create your models here.

class Course(models.Model):
	course_name=models.CharField(max_length=1500)
	def __unicode__(self):
		return self.course_name


class User(models.Model):
	user_name=models.CharField(max_length=1500)
	user_age=models.IntegerField(null=True,blank=True)
	user_email=models.CharField(max_length=1500,default="test@test.com")
	user_password=models.CharField(max_length=1500,default="test")
	user_role=models.CharField(max_length=1500,choices=TITLE_CHOICES,default=STUDENT)
	# user_img=models.ImageField(upload_to='media/users/',null=True,blank=True,default='media/users/user.jpg/')
	def __unicode__(self):
		return self.user_name

 
class UploadFile(models.Model):
    """This holds a single user uploaded file"""
    myfile = models.FileField(upload_to='media/files/')
    course=models.ForeignKey(Course)
    def __unicode__(self):
    	return self.course.course_name
    

class New(models.Model):
	new_title=models.CharField(max_length=1500)
	date = models.DateTimeField()
	def __unicode__(self):
		return self.new_title
	
		
class  Test(models.Model):
	name=models.CharField(max_length=1500)
	content=models.FileField(blank=True)
	def __unicode__(self):
		return self.name



class Question(models.Model):
	question_text=models.CharField(max_length=200)
	num=models.IntegerField()
	course=models.ForeignKey(Course)
	# img = models.ImageField(upload_to='media/Questions/',null=True,blank=True)
	def __unicode__(self):
		return self.question_text



class Choice(models.Model):
	choice_text=models.CharField(max_length=1500)
	status=models.BooleanField(default=False)
	question=models.ForeignKey(Question)                                                                                                                                                         
	def __unicode__(self):
		return self.choice_text



class Exam(models.Model):
	title=models.CharField(max_length=1500)
	questions = models.ManyToManyField(Question, through='MCQ')
	course=models.ForeignKey(Course)
	def __unicode__(self):
		return self.title

class Trie(models.Model):
	grade=models.IntegerField()
	exam=models.ForeignKey(Exam)
	user=models.ForeignKey(User)
	exam_date = models.DateField(auto_now_add=True)
	

class MCQ(models.Model):
    question = models.ForeignKey(Question)
    exam = models.ForeignKey(Exam)
    date_joined = models.DateField(auto_now_add=True)

