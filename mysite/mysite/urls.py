from django.urls import path, include  # Import include to reference app urls

urlpatterns = [
    path('', include('main.urls')),  # This includes the URLs defined in your main app
]
