from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.exceptions import ValidationError


class EmployeeViewSet(ModelViewSet):
    # Set the default queryset and serializer class for the Employee model
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Override the default list method to provide custom behavior
    def list(self, request, *args, **kwargs):
        # Extract 'regid' from query parameters
        reg_id = request.query_params.get('regid', None)

        if reg_id:
            try:
                # Attempt to retrieve an employee with the given 'regid'
                employee = Employee.objects.get(regid=reg_id)
                serializer = self.get_serializer(employee)
                # Return details of the found employee
                return Response({
                    "message": "employee details found",
                    "success": True,
                    "employees": [serializer.data]
                }, status=status.HTTP_200_OK)
            except Exception:
                # Handle the case where no employee is found with the given 'regid'
                return Response({
                    "message": "employee details not found",
                    "success": False,
                    "employees": []
                }, status=status.HTTP_200_OK)
        else:
            # Retrieve all employees and serialize the data
            employees = Employee.objects.all()
            serializer = self.get_serializer(employees, many=True)
            # Return the serialized data for all employees
            return Response({
                "success": True,
                "employees": serializer.data
            }, status=status.HTTP_200_OK)

    # Override the default create method to handle employee creation
    def create(self, request, *args, **kwargs):
        try:
            # Validate the incoming data using the serializer
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Save the validated data and return success response
            serializer.save()
            return Response({
                "message": "employee created successfully",
                "regid": serializer.data['regid'],
                "success": True
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle validation or other errors during employee creation
            error_detail = e.detail
            email_errors = error_detail.get('email', [])

            if 'unique' in str(email_errors).lower():
                # Handle the case where the employee with the same email already exists
                return Response({
                    "message": "employee already exists",
                    "success": False
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "message": "employee creation failed",
                "success": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Override the default update method to handle employee details update
    def update(self, request, *args, **kwargs):
        instance = None
        try:
            # Attempt to retrieve the existing employee instance
            instance = self.get_object()
            # Validate and save the updated data
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "employee details updated successfully",
                "success": True
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            # Handle validation errors in the request body
            return Response({
                "message": "invalid body request",
                "success": False,
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # Handle other errors during employee details update
            if instance:
                return Response({
                    "message": "employee details update failed",
                    "success": False
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                    "message": "no employee found with this regid",
                    "success": False
                    }, status=status.HTTP_200_OK)

    # Override the default destroy method to handle employee deletion
    def destroy(self, request, *args, **kwargs):
        instance = None
        try:
            # Attempt to retrieve the existing employee instance
            instance = self.get_object()
            # Perform the employee deletion
            self.perform_destroy(instance)
            return Response({
                "message": "employee deleted successfully",
                "success": True
            }, status=status.HTTP_200_OK)
        except Exception:
            # Handle errors during employee deletion
            if instance:
                return Response({
                    "message": "employee deletion failed",
                    "success": False
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                "message": "no employee found with this regid",
                "success": False
                }, status=status.HTTP_200_OK)
