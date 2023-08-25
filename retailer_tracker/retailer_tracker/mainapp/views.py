from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
import json
from authapp.models import CustomUser
from mainapp.models import StandardCode
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import uuid
import os
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from authapp.models import CandidateSkill
from authapp.models import CandidateEducation
from mainapp.models import City, Country,HomeImage
from django.core import serializers

# VIEWS.
@login_required
def index(request):
    # bag_data= Bag.objects.all().count()
    context = {
        # 'bag_data': bag_data
    }

    return render(request, 'home.html', context)
@login_required
def profile(request):
    # bag_data= Bag.objects.all().count()
    currentUser=request.user
    nationalityList=StandardCode.objects.filter(code_type='NATIONALITY')
    degreeList=StandardCode.objects.filter(code_type='DEGREE')
    print(degreeList)
    genderList=StandardCode.objects.filter(code_type='GENDER')
    maritalStatusList=StandardCode.objects.filter(code_type='MARITALSTATUS')
    countryList=Country.objects.filter(is_active=True)
    skillList=CandidateSkill.objects.filter(candidate=currentUser)
    tagString=','.join([str(item.skill) for item in skillList if item])
    educationList=CandidateEducation.objects.filter(candidate=currentUser)

    context = {
         'nationalityList': nationalityList,'genderList': genderList,'maritalStatusList': maritalStatusList,'tagString':tagString
         ,'degreeList':degreeList,'countryList':countryList,'educationList':educationList
    }

    return render(request, 'profile/user-profile.html', context)

#APIs
def BaseAPI(request,method):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseBadRequest('Invalid request')
    if request.method != method.upper():
        return HttpResponseBadRequest('Invalid request')
    
@login_required
def ProfileDetailGet_Basic(request):
    BaseAPI(request,"get")
    currentUser=request.user
    userBasicInfo={'about':currentUser.about,'first_name':currentUser.first_name,'middle_name':currentUser.middle_name,
                   'last_name':currentUser.last_name,
    'email':currentUser.email,'date_of_birth':None if currentUser.date_of_birth==None else currentUser.date_of_birth.strftime("%Y-%m-%d"),'passport':currentUser.passport,
    'gender':(None if currentUser.gender==None else currentUser.gender.description)
    ,'nationality': (None if currentUser.nationality==None else   currentUser.nationality.description),
    'marital_status':(None if currentUser.marital_status==None else  currentUser.marital_status.description),
    'profile_image_path':currentUser.profile_image_path,'phone':None if currentUser.phone==None or currentUser.phone==""  else currentUser.phone.as_e164}
    return JsonResponse({'result': userBasicInfo})
@login_required
def ProfileDetailUpdate_Basic(request):
    try:
        BaseAPI(request,"get")
        currentUser=request.user
       
        if len(request.FILES) != 0:
            myfile = request.FILES['profileImage']
            fs = FileSystemStorage()
            print(myfile.name)

            #guid=str(uuid.uuid4())
            guid=str(uuid.uuid4().hex)
            result = os.path.splitext(myfile.name)
            newFileName=guid+result[1]

            current_site = Site.objects.get_current()
            print(request.get_host())

            filename = fs.save(newFileName, myfile)
            print(filename)
            uploaded_file_url = fs.url(filename)
            CustomUser.objects.update_or_create(id=currentUser.id,
                                                           defaults={ 'profile_image_path':uploaded_file_url})

        #data =request.POST["jsonData"]
        data = json.loads(request.POST.get("jsonData"))
        dob=data.get('date_of_birth')
        gender_id=data.get('gender')
        nationality_id=data.get('nationality')
        marital_status_id=data.get('marital_status')
        print(data)
        gender=None if gender_id=="" else StandardCode.objects.get(code=gender_id,code_type='GENDER')
        nationality=None if nationality_id=="" else StandardCode.objects.get(code=nationality_id,code_type='NATIONALITY')
        marital_status=None if marital_status_id=="" else StandardCode.objects.get(code=marital_status_id,code_type='MARITALSTATUS')

        obj, created = CustomUser.objects.update_or_create(id=currentUser.id,
                                                           defaults={ 'about':data.get('about'),'first_name':data.get('first_name'),
                                                            'middle_name':data.get('middle_name'),'last_name':data.get('last_name'),
        'date_of_birth':(None if dob=="" else dob) ,'passport':data.get('passport'),'gender':gender
        ,'nationality':nationality,'marital_status':marital_status,'phone':data.get('phone')}
        )
        result= {"status":"success","message":""}
    except Exception as e:
        print('exception')
        result= {"status":"failed","message":str(e)}
   
    return JsonResponse({'result':result })
@login_required
def ProfilePasswordUpdate(request):
    try:
        BaseAPI(request,"get")
        currentUser=request.user
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        user = authenticate(request, username=currentUser.email, password=data.get('old_password'))
        if user is not None:
            UserModel = get_user_model()
            u = UserModel.objects.get(id=currentUser.id)
            print(u)
            u.set_password(data.get('new_password'))
            u.save()
            result= {"status":"success","message":""}
        else:
            result= {"status":"failed","message":"The old password is not correct"}
    except Exception as e:
        result= {"status":"failed","message":str(e)}
   
    return JsonResponse({'result':result })
@login_required
def CandidateSkillAdd(request):
    try:
        BaseAPI(request,"get")
        currentUser=request.user
        data = json.loads(request.body.decode("utf-8"))
        tag=data.get('tag')
        count=CandidateSkill.objects.filter(candidate=currentUser,skill=tag).count()
        if count==0:
            CandidateSkill.objects.create(candidate=currentUser,skill=tag)
        result= {"status":"success","message":""}
    except Exception as e:
        result= {"status":"failed","message":str(e)}
    return JsonResponse({'result':result })
     
def CandidateSkillRemove(request):
    try:
        BaseAPI(request,"get")
        currentUser=request.user
        data = json.loads(request.body.decode("utf-8"))
        tag=data.get('tag')
        count=CandidateSkill.objects.filter(candidate=currentUser,skill=tag).count()
        if count>0:
            CandidateSkill.objects.filter(candidate=currentUser,skill=tag).delete()
        result= {"status":"success","message":""}
    except Exception as e:
        result= {"status":"failed","message":str(e)}
    return JsonResponse({'result':result })
     
@login_required
def CandidateEducationAdd(request):
    try:
        BaseAPI(request,"POST")
        currentUser=request.user
        data = json.loads(request.body.decode("utf-8"))
        degree=data.get('degree')
        major=data.get('major')
        university=data.get('university')
        city=data.get('city')
        country=data.get('country')
        year=data.get('year')
        gpa=data.get('gpa')
        degreeObj=StandardCode.objects.get(code=degree)
        cityObj=City.objects.get(id=city)
        countryObj=Country.objects.get(id=country)

        obj= CandidateEducation.objects.create(candidate=currentUser,degree=degreeObj,major=major,university=university, 
                                          city=cityObj,country=countryObj,
                                          year=year,gpa=gpa)
        result= {"status":"success","message":{"degree":degreeObj.description,"major":major,"university":university,"city":cityObj.name
                                               ,"country":countryObj.name,"year":year,"gpa":gpa}}
    except Exception as e:
        result= {"status":"failed","message":str(e)}
    return JsonResponse({'result':result })
@login_required     
def CandidateEducationRemove(request):
    try:
        BaseAPI(request,"POS")
        currentUser=request.user
        data = json.loads(request.body.decode("utf-8"))
        id=data.get('id')
        count=CandidateEducation.objects.filter(candidate=currentUser,id=id).count()
        if count>0:
            CandidateEducation.objects.filter(candidate=currentUser,id=id).delete()
        result= {"status":"success","message":""}
    except Exception as e:
        result= {"status":"failed","message":str(e)}
    return JsonResponse({'result':result })
@login_required
def CityGet(request):
    BaseAPI(request,"post")
    data = json.loads(request.body.decode("utf-8"))
    id=data.get('country_id')
    currentUser=request.user
    cityList=City.objects.filter(country_id=id,is_active=True).values()
    return JsonResponse({'result': list(cityList)})
@login_required
def HomeProductGet(request):
    BaseAPI(request,"post")
    data = json.loads(request.body.decode("utf-8"))
    id=data.get('index')
    print(id)
    currentUser=request.user
    lst=HomeImage.objects.filter(id__gte=id,Status=1).values()
    return JsonResponse({'result': list(lst)})
 
        