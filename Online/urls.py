"""Online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from myapp.views import *
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^MCQ/$',start),
    url(r'^standard/$',standard),
    url(r'^what_do/$',what_do),
    url(r'^staff/$',staff),
    url(r'^statics_course/$',statics_course),
    url(r'^statics_student/$',statics_student),
    url(r'^file/$',test_file),
    url(r'^MCQ/courses',courses),
    url(r'^MCQ/contact/$',contacts),
    url(r'^MCQ/profile/$',profile),
    url(r'^random/$',get_random),
    url(r'^editanswer/(?P<aid>\d+)',editanswer),
    url(r'^MCQ/ansedit/(?P<aid>\d+)',editans),
    url(r'^MCQ/c_list/$',list_course),
    url(r'^MCQ/u_list/$',list_users),
    url(r'^cdelete/(?P<cid>\d+)',course_delete),
    url(r'^cexam/(?P<cid>\d+)',exam_delete),
    url(r'search_course/(?P<cid>\d+)',search_course),
    url(r'search_student/(?P<uid>\d+)',search_student),
    url(r'^list_exams/(?P<cid>\d+)',list_exams),
    url(r'^newexam/(?P<cid>\d+)',newexam),
    url(r'^MCQ/addexam/(?P<cid>\d+)',addexam),
    url(r'^udelete/(?P<uid>\d+)',user_delete),
    url(r'^grades/(?P<uid>\d+)',grades),
    url(r'^delanswer/(?P<aid>\d+)',delanswer),
    url(r'^uprofile/(?P<uid>\d+)',profile_id),
    url(r'^update/(?P<uid>\d+)',user_update),
    url(r'^uadd/$',user_add),
    url(r'^exams/$',exams),
    url(r'^statics_courses/(?P<cid>\d+)',statics_courses),
    url(r'^useradd/$',useradd),
    url(r'^Try/(?P<score>\d+)',result),
    url(r'^update/(?P<uid>\d+)',user_update),
    url(r'^cdetail/(?P<cid>\d+)',course_detail),
    url(r'^take_exam/(?P<cid>\d+)',take_exam),
    url(r'^MCQ/q_list/(?P<cid>\d+)',question_list),
    url(r'^MCQ/q_upload/(?P<cid>\d+)',question_upload),
 	url(r'^MCQ/q_detail/(?P<qid>\d+)',question_detail),
 	url(r'^MCQ/reg',reg),
 	url(r'^MCQ/login',reg),
    url(r'^MCQ/user_login',login),
    url(r'^MCQ/user_reg',registeration) ,
    url(r'^MCQ/logout',logout)	,
    url(r'^MCQ/students',students),
    url(r'get_name/',get_name),
    url(r'^MCQ/file/$',savefile),
    url(r'^MCQ/exam/$',exam),
    url(r'^list_files',list_files),
    url(r'^sendemail/$',sendemail),
]

	