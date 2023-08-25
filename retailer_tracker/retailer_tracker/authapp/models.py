from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .managers import CustomUserManager
from django.core.mail import send_mail
from django.conf import settings
from mainapp.models import StandardCode,City,Country
import json
# from mainapp.models import CandidateEducation
# from mainapp.models import CandidateExperience
# from mainapp.models import CandidateLanguage
# from mainapp.models import CandidateCertification
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    signup_confirmation = models.BooleanField(default=False)
    first_name = models.CharField(max_length = 400, blank = True,null=True)
    middle_name = models.CharField(max_length = 400, blank = True,null=True)
    last_name = models.CharField(max_length = 400, blank = True,null=True)
    date_of_birth = models.DateTimeField(null=True)
    passport = models.CharField(max_length = 200, blank = True,null=True)
    about = models.CharField(max_length = 4000, blank = True,null=True)
    about = models.CharField(max_length = 4000, blank = True,null=True)
    gender = models.ForeignKey(
        StandardCode,  related_name='related_primary_standardcode', on_delete=models.CASCADE, null=True)
    nationality = models.ForeignKey(
    StandardCode,related_name='related_secondary_standardcode',  on_delete=models.CASCADE, null=True)
    marital_status = models.ForeignKey(
    StandardCode, related_name='related_tertiary_standardcode', on_delete=models.CASCADE, null=True)

    # education = models.ManyToManyField(
    # CandidateEducation)
    # experience = models.ManyToManyField(
    # CandidateExperience)
    # language = models.ManyToManyField(
    # CandidateLanguage)
    # certification = models.ManyToManyField(
    # CandidateCertification)
    profile_image_path = models.CharField(max_length = 4000, blank = True,null=True)
    phone = PhoneNumberField(null=True, blank=True)
    reset_try=models.IntegerField( blank = True,null=True,default=0)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id}"

    def get_object(self):
        obj = CustomUser.objects.get(user=self.request.user)
        return obj

    def email_user(self, *args, **kwargs):
        print()
        result = send_mail(
            '{}'.format(args[0]),
            '{}'.format(args[1]),
            #'no.reply@naqel.com.sa',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )
        print(result)
class MainAppModel(models.Model):
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name="CreatedDate")
    class Meta:
        abstract = True
class CandidateSkill(MainAppModel):
    candidate=models.ForeignKey("CustomUser",on_delete=models.CASCADE, verbose_name="candidate")
    skill=models.CharField(
        max_length=200, null=True, verbose_name="skill")
    # created_date = models.DateTimeField(
    #     default=timezone.now, verbose_name="CreatedDate")
class CandidateEducation(MainAppModel):
    candidate=models.ForeignKey("CustomUser",on_delete=models.CASCADE, verbose_name="candidate")
    degree = models.ForeignKey(
        StandardCode, on_delete=models.CASCADE)
    major = models.CharField(
        max_length=200, null=True, verbose_name="Major")
    university = models.CharField(
        max_length=200, null=True, verbose_name="University")
    city = models.ForeignKey(
        City,on_delete=models.CASCADE)
    country = models.ForeignKey(
        Country,on_delete=models.CASCADE)
    year = models.IntegerField(
         null=True, verbose_name="Year")
    gpa = models.IntegerField(
         null=True, verbose_name="GPA")
    # created_date = models.DateTimeField(
    #     default=timezone.now, verbose_name="CreatedDate")
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __str__(self):
        return f"{self.id}"
class CandidateCertification(MainAppModel):
    candidate=models.ForeignKey("CustomUser",on_delete=models.CASCADE, verbose_name="candidate")
    name = models.CharField(
        max_length=200, null=True, verbose_name="Name")
    issued_by = models.CharField(
        max_length=200, null=True, verbose_name="IssuedBy")
    year = models.IntegerField(
         null=True, verbose_name="Year")
    # created_date = models.DateTimeField(
    #     default=timezone.now, verbose_name="CreatedDate")
    # validity = models.IntegerField(
    #      null=True, verbose_name="CodeType")
    def __str__(self):
        return f"{self.id}"
class CandidateExperience(MainAppModel):
    candidate=models.ForeignKey("CustomUser",on_delete=models.CASCADE, verbose_name="candidate")
    employer_name = models.CharField(
        max_length=200, null=True, verbose_name="EmployerName")
    from_date = models.DateField(
         null=True, verbose_name="FromDate")
    to_date = models.DateField(
         null=True, verbose_name="ToDate")
    position = models.CharField(
        max_length=200, null=True, verbose_name="Position")
    reason_for_leaving = models.CharField(
        max_length=500, null=True, verbose_name="ReasonForLeaving")
    # created_date = models.DateTimeField(
    #     default=timezone.now, verbose_name="CreatedDate")
    def __str__(self):
        return f"{self.id}"
class CandidateLanguage(MainAppModel):
    candidate=models.ForeignKey("CustomUser",on_delete=models.CASCADE, verbose_name="candidate")
    proficiency = models.ForeignKey(
        StandardCode, related_name='related_primary_candidate_language' ,  on_delete=models.CASCADE, verbose_name="proficiency",
     null=True)
    years_of_experience = models.CharField(
        max_length=200, null=True, verbose_name="YearsOfExperience")
    last_used =models.ForeignKey(
        StandardCode, related_name='related_secondary_candidate_language', on_delete=models.CASCADE, verbose_name="last_used")
    # created_date = models.DateTimeField(
    #     default=timezone.now, verbose_name="CreatedDate")
    def __str__(self):
        return f"{self.id}"
    

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)
    instance.save()
