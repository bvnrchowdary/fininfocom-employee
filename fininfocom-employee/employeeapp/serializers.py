from rest_framework import serializers
from .models import Employee, AddressDetails, WorkExperience, Qualifications, Projects


# Serializer for AddressDetails model
class AddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressDetails
        fields = '__all__'


# Serializer for WorkExperience model
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


# Serializer for Qualifications model
class QualificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualifications
        fields = '__all__'


# Serializer for Projects model
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


# Serializer for Employee model, including nested serializers for related models
class EmployeeSerializer(serializers.ModelSerializer):
    workExperience = WorkExperienceSerializer(many=True)
    addressDetails = AddressDetailsSerializer(many=True)
    qualifications = QualificationsSerializer(many=True)
    projects = ProjectsSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('regid', 'name', 'email', 'age', 'gender', 'phoneNo', 'addressDetails', 'workExperience',
                  'qualifications', 'projects', 'photo')

    # Custom create method to handle nested serializer data creation
    def create(self, validated_data):
        address_details_data = validated_data.pop('addressDetails', [])
        work_experience_data = validated_data.pop('workExperience', [])
        qualifications_data = validated_data.pop('qualifications', [])
        projects_data = validated_data.pop('projects', [])

        employee = Employee.objects.create(**validated_data)

        # Create related instances for AddressDetails, WorkExperience, Qualifications, and Projects
        for address_data in address_details_data:
            AddressDetails.objects.create(employee=employee, **address_data)

        for work_experience in work_experience_data:
            WorkExperience.objects.create(employee=employee, **work_experience)

        for qualification_data in qualifications_data:
            Qualifications.objects.create(employee=employee, **qualification_data)

        for project_data in projects_data:
            Projects.objects.create(employee=employee, **project_data)

        return employee

    # Custom update method to handle nested serializer data update
    def update(self, instance, validated_data):
        address_details_data = validated_data.pop('addressDetails', [])
        work_experience_data = validated_data.pop('workExperience', [])
        qualifications_data = validated_data.pop('qualifications', [])
        projects_data = validated_data.pop('projects', [])

        # Update fields in the main Employee instance
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phoneNo = validated_data.get('phoneNo', instance.phoneNo)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()

        # Update or create related instances for AddressDetails, WorkExperience, Qualifications, and Projects
        self.update_or_create_related_instances(instance, AddressDetails, address_details_data)
        self.update_or_create_related_instances(instance, WorkExperience, work_experience_data)
        self.update_or_create_related_instances(instance, Qualifications, qualifications_data)
        self.update_or_create_related_instances(instance, Projects, projects_data)

        return instance

    # Helper method to update or create related instances in a generic way
    @staticmethod
    def update_or_create_related_instances(instance, model_class, data_list):
        # Delete existing instances
        delete_objs = model_class.objects.filter(employee=instance)
        delete_objs.delete()

        # Create new instances
        if data_list:
            instances_to_create = [model_class(employee=instance, **data) for data in data_list]
            model_class.objects.bulk_create(instances_to_create)
