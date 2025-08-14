from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    # path('booking/', views.booking, name='booking'),
    # path('guides/<slug:slug>', views.profile, name='profile'),
    path('contact/',views.contact, name='contact'),
    # path('blog/', views.blog_list, name='blog'),
    path('blog/', views.blog_list, name='blog_list'), 
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('summernote/', include('django_summernote.urls')),
    path('booking/', views.booking, name='booking'),
    path('book/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('explore/gallery/', views.tour_gallery, name='tour_gallery'),
    path('destinations/', views.destination_list, name='destination-list'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination-detail'),
    # path('explore/destination/', views.destination, name='destination'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
