from django.urls import path

from mainapp.views import index
from mainapp.views import profile
from mainapp.views import ProfileDetailGet_Basic,ProfileDetailUpdate_Basic,ProfilePasswordUpdate
from mainapp.views import CandidateSkillRemove,CandidateSkillAdd,CandidateEducationAdd,CandidateEducationRemove,CityGet,HomeProductGet


urlpatterns = [
    path("", index, name="index"),  
    path("profile", profile, name="profile"),  
    
    path("api/profile-basic-get", ProfileDetailGet_Basic, name = "profile_basic_get"),
    path("api/profile-basic-update", ProfileDetailUpdate_Basic, name = "profile_basic_update"),
    path("api/profile-password-update", ProfilePasswordUpdate, name = "profile_password_update"),
    path("api/profile-skill-add", CandidateSkillAdd, name = "profile_skill_add"),
    path("api/profile-skill-remove", CandidateSkillRemove, name = "profile_skill_remove"),
        path("api/profile-education-add", CandidateEducationAdd, name = "profile_education_add"),
    path("api/profile-education-remove", CandidateEducationRemove, name = "profile_education_remove"),
    path("api/profile-city-get", CityGet, name = "profile_city_get"),
       path("api/home-product-get", HomeProductGet, name = "HomeProductGet"),
]