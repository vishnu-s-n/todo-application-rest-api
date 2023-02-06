from django.urls import path
from .views import UserRegistrationView,LoginOtpView,UserLoginView,TodoCreate,TodoGetAll,TodoDetailView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('user-registration/', UserRegistrationView.as_view(),name="UserRegistrationViewURL"),
    path('user-otp/', LoginOtpView.as_view(),name="LoginOtpViewURL"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-login/', UserLoginView.as_view(), name="UserLoginViewURL"),
    path('todo-create/', TodoCreate.as_view(), name="TodoCreateURL"),
    path('list-todo/',TodoGetAll.as_view(),name="ListTodoURL"),
    path('todo-detail/<int:id>/',TodoDetailView.as_view(),name="TodoDetailViewURL")

]