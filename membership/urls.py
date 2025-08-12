from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('plans/', views.membership_plans, name='plans'),
    path('subscribe/<int:tier_id>/', views.subscribe, name='subscribe'),
    path('test-subscribe/<int:tier_id>/', views.test_subscribe, name='test_subscribe'),
    path('khalti-subscribe/<int:tier_id>/', views.khalti_subscribe, name='khalti_subscribe'),
    path('test-khalti-subscribe/<int:tier_id>/', views.test_khalti_subscribe, name='test_khalti_subscribe'),
    path('khalti-return/<int:membership_id>/', views.khalti_return, name='khalti_return'),
    path('my-membership/', views.my_membership, name='my_membership'),
    path('cancel/', views.cancel_membership, name='cancel_membership'),
    path('reactivate/', views.reactivate_membership, name='reactivate_membership'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
] 