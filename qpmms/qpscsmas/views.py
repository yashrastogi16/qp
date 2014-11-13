from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.db import connection
from .models import *
from forms import *
import datetime
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
import hashlib
import random
from datetime import datetime, timedelta, date
from django.conf import settings as conf_settings
import os
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.core.mail import send_mail,  EmailMultiAlternatives
from django.contrib import messages

def login(request):
	form = QpadminForm(request.POST)
	content = {}
	content['form'] = form
	content.update(csrf(request))
	if request.method == "POST":
		print "post method00000000000000000000000000000000000000000000000000"
		username = request.POST['userid']
		# password = request.POST['password']
		password = request.POST['password']
		# password = hashpass(in_password)
		user_list = Qpadmin.objects.filter(user_id=username, password1=password)
		if(user_list):
			userobj = user_list[0]
			#s=userlogin(username = userobj.username, userid = userobj.user_id, role = userobj.role, logintime = datetime.now())
			s.save()   
			request.session['user'] = userobj
			# return HttpResponse("This is Admin Home Page")
			return HttpResponseRedirect("/dashboard")
		else:
			content['err_msg'] = 'Invalid Credentials'
		return render_to_response('login.html', content, context_instance=RequestContext(request))

	return render_to_response('login.html', content, context_instance=RequestContext(request))
def dashboard(request):
	content = {}
	content.update(csrf(request))
	return render_to_response('dashboard.html', content, context_instance=RequestContext(request))
def viewemployee(request):
	lists = employee_details.objects.all()
	return render_to_response('viewemployee.html', locals(), context_instance=RequestContext(request))
def registeremployee(request):
	form = employee_detailsForm(request.POST or None)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
	return render_to_response("registeremployee.html",locals(),context_instance=RequestContext(request))
def viewcompanies(request):
	lists = associative_company.objects.all()
	return render_to_response('viewcompanies.html', locals(), context_instance=RequestContext(request))
def registercompanies(request):
	form = associative_companyForm(request.POST or None)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
	return render_to_response("registercompanies.html",locals(),context_instance=RequestContext(request))
def viewdevices(request):
	lists = device_info.objects.all()
	return render_to_response('viewdevices.html', locals(), context_instance=RequestContext(request))
def registerdevices(request):
	form = device_infoForm(request.POST or None)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
	return render_to_response("registerdevices.html",locals(),context_instance=RequestContext(request))
def areports(request):
    content = {}
    list1 = {}
    if request.method == "POST":
        emp1 = request.POST['empid']
        z = employee_details.objects.get(employee_id = emp1)
        # for i in liste:
        # 	z = i.rfidcardno
        # print z
        #print liste.rfidcardno
        list1 = emp_entry.objects.filter(rfidcardno = z)
    content = {'lists' :list1 }
    return render_to_response("areports.html",content,context_instance=RequestContext(request))
def dareports(request):
    content = {}
    alist = []
    bh_list = []
    #cursor = connection.cursor()
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate =  request.POST.get('todate')
        if fromdate:
            bh_obj_list=emp_entry.objects.filter(date_time__range=(fromdate, todate))
            for bh_obj in bh_obj_list: 
                bh_list.append(bh_obj.rfidcardno)
            if bh_obj_list:
                for rfidcardno in set(bh_list):
                    adict = {}
                    #emp = emp_entry.objects.all()
                    #cursor.execute("select * from qpscsmas_emp_entry")
                    emp1= emp_exit.objects.get(rfidcardno = rfidcardno).filter()
                    emp = emp_entry.objects.get(rfidcardno = rfidcardno)
                    #print "employeeeeeee",emp
                    adict['empid'] = emp.empid
                    adict['ip_addr'] = emp.ip_addr
                    adict['ip_addr1'] = emp1.ip_addr
                    adict['status'] = emp.device_location
                    adict['status1'] = emp1.device_location
                    adict['timeforentry']=emp.date_time
                    adict['timeforexit']=emp1.date_time
                    adict['rfidcardno'] =emp1.rfidcardno
                    alist.append(adict)
        content = {'lists' :alist }
        content.update(csrf(request))
    # list1 = emp_entry.objects.all
    # list1 = emp_entry.objects.all
    return render_to_response("dareports.html", content, context_instance=RequestContext(request))

def mealreports(request):
	content = {}
	alist = []
	br_list = []
	l_list = []
	d_list = []
	if request.method == "POST":
		fromdate = request.POST['fromdate']
		todate =  request.POST['todate']
		print fromdate
		print todate
		if fromdate:
			br_obj_list=emp_breakfast.objects.filter(date_time__range=(fromdate, todate))
			l_obj_list = emp_lunch.objects.filter(date_time__range=(fromdate, todate))
			d_obj_list = emp_dinner.objects.filter(date_time__range=(fromdate, todate))
			for br_obj in br_obj_list: 
				br_list.append(br_obj.rfidcardno)
			for l_obj in l_obj_list:
				l_list.append(l_obj.rfidcardno)
			for d_obj in d_obj_list:
				d_list.append(d_obj.rfidcardno)
			if br_obj_list:
				for rfid in set(br_list):
					adict = {}
					fbf_count = br_list.count(rfid)
					fl_count  = l_list.count(rfid)
					dd_count  = d_list.count(rfid)
					emp = employee_details.objects.get(rfidcardno = rfid)
					adict['emp_id'] = emp.employee_id
					adict['emp_name'] = emp.first_name
					adict['com'] = emp.company.company_name
					adict['bf_count'] = fbf_count
					adict['l_count'] = fl_count
					adict['d_count'] = dd_count
					alist.append(adict)
					print alist
		content = {'lists' :alist }
	return render_to_response("mealreports.html",content, context_instance=RequestContext(request))

def detailedmealsreport(request):
	content={}
	list1 = []
	content.update(csrf(request))
	comp_list = []
	comp_list.append('Select')
	cmp_list = associative_company.objects.all()
	for i in cmp_list:
		comp_list.append(i)
	content['comp_list']=comp_list
	cursor = connection.cursor()
	listz = []
	if request.method == "POST":
		comp_name = request.POST['company']
		year = request.POST['Year']
		month = request.POST['Month']
		print comp_name
		print year
		print month
		if comp_name == 'Select':
			listz = employee_details.objects.all()
		else:
			cursor.execute("select id from qpscsmas_associative_company where company_name = %s",[comp_name])
			comp_id = cursor.fetchone()[0]
			listz = employee_details.objects.filter(company_id = comp_id)
			print comp_id
			sumb = 0
			suml = 0
			sumd = 0
			for i in listz:
			 	adict = {}
			 	bdict = {}
			 	bdict['emp_id'] = "Total"
			 	bdict['emp_name'] = " "
			 	bdict['com'] = " "
			 	cursor.execute("select employee_id,first_name,company_id from qpscsmas_employee_details where rfidcardno = %s",[i.rfidcardno])
			 	x = cursor.fetchone()
				adict['emp_id'] = x[0]
				adict['emp_name'] = x[1]
				adict['com'] = associative_company.objects.get(id=x[2])
				cursor.execute("select count(breakfast_count) from qpscsmas_emp_breakfast where rfidcardno =%s",[i.rfidcardno])
				adict['bf_count'] = cursor.fetchall()[0][0]
				sumb += adict['bf_count']
				cursor.execute("select count(lunch_count) from qpscsmas_emp_lunch where rfidcardno =%s",[i.rfidcardno])
				adict['l_count'] = cursor.fetchall()[0][0]
				suml += adict['l_count']
				cursor.execute("select count(dinner_count) from qpscsmas_emp_dinner where rfidcardno =%s",[i.rfidcardno])
				adict['d_count'] = cursor.fetchall()[0][0]
				sumd += adict['d_count']
				bdict['bf_count'] = sumb
				bdict['l_count'] = suml
				bdict['d_count'] = sumd
				list1.append(adict)
			list1.append(bdict)
			content = { 'lists' : list1 }
		#if request.method == "GET":
		if request.REQUEST.get('excel'):
			print "Hello"
			print_pref = request.GET['pref']
			if print_pref:
				print "Hello How are you!!!"
	content['comp_list']=comp_list
	return render_to_response("detailedmealsreport.html",content,context_instance=RequestContext(request))

def mtconfigure(request):
	form = meal_timingForm(request.POST or None)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
	return render_to_response("mtconfigure.html",locals(), context_instance=RequestContext(request))
def priceconfigure(request):
	content = {}
	content.update(csrf(request))
	return render_to_response("priceconfigure.html",content, context_instance=RequestContext(request))
def export_to_excel(request):
    lists = employee_details.objects.all()
   	# your excel html format
    template_name = "Export/sample_excel.html"
    
    response = render_to_response(template_name, {'lists': lists})
    # this is the output file
    filename = "report.xls"

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response
def masteradmin(request):
	content = {}
	content.update(csrf(request))
	return render_to_response("masteradmin/dashboard.html",content, context_instance=RequestContext(request))
def custom_404(request):
	return render_to_response("404.html",RequestContext(request))

# def logout(request):
#     user = request.session['user']
#     s=userlogout(username = user.username, userid = user.user_id,d
# role = user.role, logouttime = datetime.now())            
#     s.save()
#     session_keys = request.session.keys()
#     form = UserForm(request.POST)
#     for key in session_keys:
#         del request.session[key]
#     # content.update(csrf(request))
#     return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

