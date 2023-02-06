from rest_framework import serializers
from todo.models import TodoTask,UserRegistration,UserLoginOtp
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError


# <editor-fold desc="User Registration with email and phonenumber with proper validation">
class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=True)
    phonenumber = serializers.IntegerField(required=True)

    def validate(self, data):
        email = data.get('email')
        email_user = UserRegistration.objects.filter(email=email)
        if email_user.exists():
            raise serializers.ValidationError("email already exist")

        phonenumber = data.get('phonenumber')
        print(type(phonenumber))
        phnstr = str(phonenumber)
        if len(phnstr) == 10:
            pass
        else:
            raise serializers.ValidationError("Enter a Valid 10 Digits Phone Number")
        phone_user = UserRegistration.objects.filter(phonenumber=phonenumber)
        if phone_user.exists():
            raise serializers.ValidationError("phonenumber already exist")
        return data

    class Meta:
        fields= "__all__"


    def create(self, validated_data):
        print(validated_data)
        try:
            user = UserRegistration.objects.create(
                name = validated_data["name"],
                phonenumber = validated_data["phonenumber"],
                email = validated_data["email"]
            )
        except Exception as e:
            print(e)
            user.delete()
            raise serializers.ValidationError(f"User not created {e}")
        return validated_data
# </editor-fold>

# <editor-fold desc="Generate OTP to User Email Address">
class GenerateOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, data):
        email = data.get('email')
        email_user = UserRegistration.objects.filter(email=email)
        if not email_user.exists():
            raise serializers.ValidationError("Invalid Email Address")
        return data

    class Meta:
        fields="__all__"

    def create(self, validated_data):
        email = validated_data.get("email")
        otp = random.randint(1000, 9999)
        send_mail("Your OTP",
                  f"Your otp is {otp} ",
                  "ivishnu.ms@gmail.com",
                  [email],
                )
        user = UserRegistration.objects.get(email=email)
        user = UserLoginOtp.objects.create(otp=otp,user=user,active=True)
        return validated_data
# </editor-fold>


# <editor-fold desc="User Login Serializer with JWT Authentication">
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp=serializers.IntegerField(required=True)
    access=serializers.CharField(read_only=True)
    refresh=serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        user_otp = data.get('otp')

        try:
            user_check = UserRegistration.objects.get(email=email)
        except:
            raise serializers.ValidationError("Invalid Email")
        try:
            user_check_otp=UserLoginOtp.objects.get(user=user_check,otp=user_otp)
        except:
            raise serializers.ValidationError("Invalid Email or  OTP")
        return data

    class Meta:
        fields = "__all__"


    def create(self, validated_data):
        email=validated_data.get('email')
        user_otp=validated_data.get('otp')

        try:
            user_check=UserRegistration.objects.get(email=email)
        except:
            raise serializers.ValidationError("Invalid Email")

        try:
            login_otp_check = UserLoginOtp.objects.filter(user=user_check, otp=user_otp, active=True)
            if login_otp_check.exists():
                refresh = RefreshToken.for_user(user_check)
                print(refresh)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
        except:
            raise serializers.ValidationError("Login Failed")
        return validated_data
# </editor-fold>

# <editor-fold desc="Create tasks Serializer">
class TodoSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)

    def validate(self, data):
        user_id=data.get("user_id")
        try:
            user = UserRegistration.objects.get(id=user_id)
        except:
            raise serializers.ValidationError("User not exit")

        return data

    class Meta:
        fields= "__all__"

    def create(self, validated_data):
        user_id=validated_data.get("user_id")
        user = UserRegistration.objects.get(id=user_id)
        try:
            todo_task = TodoTask.objects.create(
                title = validated_data.get("title"),
                description = validated_data.get("description"),user=user)
        except Exception as e:
            raise serializers.ValidationError(f" Task Added Successfully {e}")
        return validated_data
# </editor-fold>

# <editor-fold desc="Display all the tasks Serializer">
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoTask
        fields="__all__"
# </editor-fold>

# <editor-fold desc="Get the specific details of the task serializer">
class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoTask
        fields="__all__"
# </editor-fold>
            

   

     
