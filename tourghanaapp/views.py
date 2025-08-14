from venv import logger
from django.shortcuts import render,get_object_or_404 ,HttpResponse, redirect
from .forms import ContactMessageForm 
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import ContactMessage, BlogPost , InterestCategory, Interest, ExtraBagOption, GalleryImage, Slide, Destination
from django.utils.text import slugify
from PIL import Image
from .forms import TourBookingForm
from .models import TourBooking
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse


import os
# Create your views here.
def index(request):
    context = {
        # "destinations": Destination.objects.filter(is_active=True),
        # "experts": Expert.objects.filter(is_active=True),
        # "gallery_images": GalleryImage.objects.filter(is_active=True),
        # "testimonials": Testimonial.objects.filter(is_active=True)
        "slides": Slide.objects.filter(is_active=True).order_by('order'),
        "images": GalleryImage.objects.all().order_by('-created_at')[:8],
    }
    return render(request, 'index.html', context)

# def index(request):
#     testimonials = [
#     {
#         "name": "Emily Johnson",
#         "location": "California, USA",
#         "text": "Booking with Nasaf Tours made our trip to Ghana unforgettable! The guide was knowledgeable and the experience was authentic and immersive.",
#         "image": "images/clients/client1.jpg"
#     },
#     {
#         "name": "Kwame Boateng",
#         "location": "Accra, Ghana",
#         "text": "From car rentals to guided tours, everything was seamless. I highly recommend Nasaf Tours to anyone visiting Ghana!",
#         "image": "images/clients/client2.jpg"
#     },
#     {
#         "name": "Amina Bello",
#         "location": "Lagos, Nigeria",
#         "text": "Our family vacation was well-organized and enjoyable thanks to Nasaf Tours. The accommodation and transport exceeded expectations.",
#         "image": "images/clients/client3.jpg"
#     },
# ]

#     gallery_images = [
#     {"url": "images/gallery/gallery1.jpg", "alt": "Cape Coast Castle - Ghana History"},
#     {"url": "images/gallery/gallery2.jpg", "alt": "Elmina Fishing Boats"},
#     {"url": "images/gallery/gallery3.jpg", "alt": "Kwame Nkrumah Mausoleum"},
#     {"url": "images/gallery/gallery4.jpg", "alt": "Volta Lake Aerial View"},
#     {"url": "images/gallery/gallery5.jpg", "alt": "Kakum National Park Canopy Walk"},
#     {"url": "images/gallery/gallery6.jpg", "alt": "Makola Market - Accra"},
#     {"url": "images/gallery/gallery7.jpg", "alt": "Traditional Ghanaian Drummers"},
#     {"url": "images/gallery/gallery8.jpg", "alt": "Labadi Beach Sunset"},
# ]

#     experts = [
#   {
#     "name": "Okyeame Kwame",
#     "description": "Okyeame Kwame is a certified Ghana travel expert with 10+ years of experience guiding tours to Kakum National Park, Cape Coast Castle, and hidden cultural villages.",
#     "image": "/images/experts/Okyeame Kwame.jpeg",
#     "profile_url": ""
#   },
#   {
#     "name": "Kwame Nana Safo",
#     "description": "Kwame Nana Safo is a seasoned tour guide specializing in Ghana's rich history and culture. With over 15 years of experience, he provides personalized tours to historical sites and cultural landmarks.",
#     "image": "/images/experts/Okyeame Kwame.jpeg",
#     "profile_url": ""
#   },
#     {
#     "name": "Kwame Nana Safo",
#     "description": "Kwame Nana Safo is a seasoned tour guide specializing in Ghana's rich history and culture. With over 15 years of experience, he provides personalized tours to historical sites and cultural landmarks.",
#     "image": "/images/experts/Okyeame Kwame.jpeg",
#     "profile_url": ""
#   },

# ]
#     destinations = [
#     {
#         'name': 'Cape Coast Castle – Historic Slave Trade Site in Ghana',
#         'description': 'Explore Cape Coast Castle, a UNESCO World Heritage Site and one of Ghana’s top tourist attractions. Discover the rich history of the transatlantic slave trade in West Africa.',
#         'image': 'images/destinations/Cape-Coast-Castle-Museum.png',
#         'url': ''
#     },
#     {
#         'name': 'Kakum National Park – Canopy Walkway and Rainforest Adventures',
#         'description': 'Visit Kakum National Park, one of the most visited tourist destinations in Ghana. Experience the famous canopy walkway, nature trails, and wildlife in a lush rainforest.',
#         'image': 'images/destinations/Kakum.jpg',
#         'url': ''
#     },
#     {
#         'name': 'Mole National Park – Wildlife Safari in Northern Ghana',
#         'description': 'Embark on a thrilling safari at Mole National Park, the largest wildlife reserve in Ghana. Spot elephants, antelopes, baboons, and more in their natural habitat.',
#         'image': 'images/destinations/Mole National Park.jpg',
#         'url': ''
#     },
#     {
#         'name': 'Lake Volta – Boat Cruises and Eco-Tourism in Ghana',
#         'description': 'Discover Lake Volta, one of the world’s largest man-made lakes. Enjoy boat tours, fishing, and eco-tourism experiences in the heart of Ghana’s Eastern Region.',
#         'image': 'images/destinations/Lake-Volta.jpg',
#         'url' : ''
#     }
#     ]

#     slides = [
#   {
#     "title": "Explore the freedom of car rental with",
#     "highlight": "Nasaf Tours Ghana",
#     "description": "Explore Ghana on your own terms with Nasaf Tours. Whether you're flying into Accra for a business trip, embarking on a scenic road adventure through Cape Coast, or simply need a convenient car for city errands, we offer reliable and affordable car rental options. Experience seamless travel, flexible pickup, and well-maintained vehicles tailored for tourists and locals alike.",
#     "cta_text": "Get your car today",
#     "cta_link": "#",
#     "image": "images/car_rent_tour_ghana.png",
#     "alt": "Car rental tour in Ghana"
#   },
#   {
#     "title": "Discover comfortable short stays with",
#     "highlight": "Nasaf Tours Ghana",
#     "description": "Looking for a cozy and affordable room rental in Ghana? Nasaf Tours offers short-stay accommodations in Accra, Kumasi, Takoradi, and beyond — ideal for travelers, digital nomads, and professionals. Whether you're visiting Ghana for a vacation, conference, or weekend getaway, our rooms are furnished, secure, and centrally located to give you the best local experience.",
#     "cta_text": "Reserve your stay",
#     "cta_link": "#",
#     "image": "images/room-rent-airbnb_ghana.png",
#     "alt": "Room rental Ghana"
#   }
# ]

    # return render(request, 'index.html',{
    #     "destinations": destinations,
    #         slides = Slide.objects.filter(is_active=True).order_by('order')
    #     "experts": experts,
    #     "gallery_images": gallery_images,
    #     "testimonials": testimonials
        
    #     })
# Uncomment the following line if you want to use HttpResponse instead of render
# def index(request):
#     return HttpResponse("Hello, world. You're at the tour guid website.")

def about(request):
    return render(request, 'about.html')

# def booking(request):
#     return render(request, 'booking.html')

# def profile(request,slug):
#     return render(request, 'profile.html')

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email
            subject = 'New Contact Message Received'
            message = f"""
            Name: {contact.name}
            Email: {contact.email}
            Message:
            {contact.message}
            """
            recipient_list = [os.environ.get('EMAIL_HOST_USER')] 

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'form': form})

def blog_list(request):
    featured = BlogPost.objects.filter(is_featured=True).order_by('-created_at').first()
    posts = BlogPost.objects.filter(is_featured=False).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {
        'featured_post': featured,
        'posts': posts
    })

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/blog_detail.html', {'post': post})


def booking(request):
    if request.method == 'POST':
        form = TourBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Send confirmation email
            send_confirmation_email(booking, request)
            
            messages.success(request, 'Your tour has been booked successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourBookingForm()
    
    return render(request, 'tours/book_tour.html', {
        'form': form,
        'interests_by_category': form.interests_by_category if hasattr(form, 'interests_by_category') else {}
    })

def send_confirmation_email(booking, request):
    try:
        subject = f"Tour Booking Confirmation - {booking.tour_date}"
        confirmation_url = request.build_absolute_uri(
            reverse('booking_confirmation', args=[booking.id])
        )
        
        context = {
            'booking': booking,
            'confirmation_url': confirmation_url,
        }
        
        text_message = render_to_string('tours/booking_confirmation.txt', context)
        html_message = render_to_string('tours/booking_confirmation.html', context)
        
        send_mail(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {str(e)}")
        # Optionally notify admins or handle the error in another way

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(TourBooking, id=booking_id)
    return render(request, 'tours/booking_confirmation.html', {'booking': booking})

def tour_gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    return render(request, 'explore/gallery.html', {'images': images})


def destination_list(request):
    """
    View to display all active destinations
    """
    destinations = Destination.objects.filter(is_active=True).order_by('name')
    context = {
        'destinations': destinations,
        'meta_title': "Explore Ghana's Top Destinations",
        'meta_description': "Discover the most beautiful and historic destinations in Ghana with Nasaf Tours"
    }
    return render(request, 'destinations/list.html', context)

def destination_detail(request, slug):
    """
    View to display a single destination detail page
    """
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    
    # Get related destinations (excluding current one)
    related_destinations = Destination.objects.filter(
        is_active=True
    ).exclude(
        id=destination.id
    ).order_by('?')[:3]  # Random 3 destinations
    
    context = {
        'destination': destination,
        'related_destinations': related_destinations,
        'meta_title': f"{destination.name} - Ghana Travel Guide",
        'meta_description': destination.description[:160]  # First 160 chars for meta
    }
    return render(request, 'destinations/detail.html', context)

