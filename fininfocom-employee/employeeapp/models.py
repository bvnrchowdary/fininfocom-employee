from django.db import models
from django.db.models import UniqueConstraint


# Model for Employee information
class Employee(models.Model):
    # Auto-incrementing primary key for Employee
    regid = models.AutoField(primary_key=True)
    
    # Employee details
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        # String representation of an Employee (for readability)
        return f'{self.regid}'
    
    class Meta:
        # Unique constraint on the email field to enforce uniqueness
        constraints = [
            UniqueConstraint(
                fields=['email'],
                name='unique_email_constraint'
            ),
        ]


# Model for Employee's Address Details
class AddressDetails(models.Model):
    # Auto-incrementing primary key for AddressDetails
    id = models.AutoField(primary_key=True)
    
    # Foreign key relationship with Employee
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='addressDetails')
    
    # Address details
    hno = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        # String representation of AddressDetails
        return f'{self.id}'


# Model for Employee's Work Experience
class WorkExperience(models.Model):
    # Auto-incrementing primary key for WorkExperience
    id = models.AutoField(primary_key=True)
    
    # Foreign key relationship with Employee
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='workExperience')
    
    # Work experience details
    companyName = models.CharField(max_length=255)
    fromDate = models.DateField()
    toDate = models.DateField()
    address = models.TextField()

    def __str__(self):
        # String representation of WorkExperience
        return f'{self.id}'


# Model for Employee's Qualifications
class Qualifications(models.Model):
    # Auto-incrementing primary key for Qualifications
    id = models.AutoField(primary_key=True)
    
    # Foreign key relationship with Employee
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='qualifications')
    
    # Qualification details
    qualificationName = models.CharField(max_length=255)
    fromDate_qualification = models.DateField()
    toDate_qualification = models.DateField()
    percentage = models.FloatField()

    def __str__(self):
        # String representation of Qualifications
        return f'{self.id}'


# Model for Employee's Projects
class Projects(models.Model):
    # Auto-incrementing primary key for Projects
    id = models.AutoField(primary_key=True)
    
    # Foreign key relationship with Employee
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='projects')
    
    # Project details
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        # String representation of Projects
        return f'{self.id}'
