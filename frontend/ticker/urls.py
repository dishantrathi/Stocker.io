
from django.urls import path
#views.method 
from . import views

from django.conf.urls import handler404,handler500
handler404 = 'ticker.views.handler404'
handler500 = 'ticker.views.handler500'

urlpatterns = [
    path('',views.home, name="home"),
    path('about/team/',views.team, name="team"),
    path('about/careers/',views.careers, name="careers"),
    path('services/',views.services, name="services"),
    path('quoteAPI/v1/<slug:symbol>/', views.quoteAPI, name='quoteAPI'),
    path('equitylist/',views.equitylist, name="equitylist"),
    path('pricing/',views.pricing, name="pricing"),
    path('login/',views.login_user, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('signup/',views.signup_user, name="signup"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('password_change/',views.password_change,name="password_change"),
    path('autoRefreshEqu/<slug:symbol>/',views.autoRefreshEqu, name="autoRefreshEqu"),
    path('equity/<slug:symbol>/',views.equity, name="equity"),
    
    
    
    
    path('quote/',views.quote, name="quote"),
    path('quote_data/<slug:symbol>/', views.quote_data, name='quote_data'),
    path('api_req/<slug:symbol>/', views.api_req, name='api_req'),
    path('chartstd/', views.chartstd, name='chartstd'),
]

