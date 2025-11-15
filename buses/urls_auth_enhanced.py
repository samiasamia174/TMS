from django.urls import path
from .views_auth_enhanced import enhanced_signup, enhanced_signin
from .views import sign_out

urlpatterns = [
    path('signup/', enhanced_signup, name='signup'),
    path('signin/', enhanced_signin, name='signin'),
    path('sign-out/', sign_out, name='sign_out'),
]
