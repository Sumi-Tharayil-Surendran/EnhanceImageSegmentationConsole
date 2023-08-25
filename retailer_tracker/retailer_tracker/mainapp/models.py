from django.db import models
from django.utils import timezone


# Create your models here.
class MainAppModel(models.Model):
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name="CreatedDate")
    class Meta:
        abstract = True
class Country(MainAppModel):
    #ID = models.CharField(primary_key=True, max_length=100, verbose_name="ID")
    code = models.CharField(
        max_length=200, null=True, verbose_name="Code")
    name = models.CharField(
        max_length=200, null=True, verbose_name="Description")
    is_active = models.BooleanField(
         null=True, verbose_name="IsActive")
    def __str__(self):
        return f"{self.name}"
class City(MainAppModel):
    country=models.ForeignKey("Country",on_delete=models.CASCADE)
    code = models.CharField(
        max_length=200, null=True, verbose_name="Code")
    name = models.CharField(
        max_length=200, null=True, verbose_name="Name")
    is_active = models.BooleanField(
         null=True, verbose_name="IsActive")
    def __str__(self):
        return f"{self.name}"
class StandardCode(MainAppModel):
    #ID = models.CharField(primary_key=True, max_length=100, verbose_name="ID")
    code = models.CharField(
        max_length=200, null=True, verbose_name="Code")
    description = models.CharField(
        max_length=200, null=True, verbose_name="Description")
    code_type = models.CharField(
        max_length=200, null=True, verbose_name="CodeType")
    def __str__(self):
        return f"{self.description}"
    
class Segment(MainAppModel):
    #ID = models.CharField(primary_key=True, max_length=100, verbose_name="ID")
    Name = models.CharField(
        max_length=200, null=True, verbose_name="Name")
    def __str__(self):
        return f"{self.Name}"    
class HomeImage(MainAppModel):
    #ID = models.CharField(primary_key=True, max_length=100, verbose_name="ID")
    ImagePath = models.CharField(
        max_length=400, null=True, verbose_name="ImagePath")
    Segment = models.ForeignKey("Segment",on_delete=models.CASCADE,null=True)
    ConfidenceJson = models.CharField(
        max_length=400, null=True, verbose_name="ConfidenceJson")
    Status = models.IntegerField(
         null=True, verbose_name="Status")
    def __str__(self):
        return f"{self.description}"

