from rest_framework.response import Response
from rest_framework.views import APIView
from todo.todo_v1_client.serializers import UserRegistrationSerializer,GenerateOtpSerializer,UserLoginSerializer,TodoSerializer,TodoListSerializer,TodoDetailSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from rest_framework import generics
from todo.models import TodoTask

# <editor-fold desc="User Registration View">
class UserRegistrationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Account Created Successfully"},status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
# </editor-fold>

# <editor-fold desc="User Login OTP View">
class LoginOtpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GenerateOtpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request)
            return Response({"message":"OTP sended to your email"},status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
# </editor-fold>

# <editor-fold desc="User Login View">
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Login Successfull"},status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
# </editor-fold>

# <editor-fold desc="Todo Create View">
class TodoCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"--------------"},status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
# </editor-fold>


# <editor-fold desc="Get all the todo view">
class TodoGetAll(APIView):
    def get(self,request,*args,**kwargs):
        queryset=TodoTask.objects.all()
        serializer=TodoListSerializer(queryset,many=True)
        return Response(data=serializer.data)
# </editor-fold>

# <editor-fold desc="Todo detail view with updation and deletion">
class TodoDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=TodoTask.objects.get(id=id)
        serializer=TodoDetailSerializer(qs)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        object=TodoTask.objects.get(id=id)
        serializer=TodoDetailSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Updated Successfully"},status=HTTP_200_OK)
        else:
            return Response(data=serializer.errors)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=TodoTask.objects.get(id=id)
        qs.delete()
        return Response({"msg":"Deleted Successfully"})
# </editor-fold>

