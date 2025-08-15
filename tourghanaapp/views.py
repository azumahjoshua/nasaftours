from venv import logger
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .forms import ContactMessageForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import (
    ContactMessage,
    BlogPost,
    InterestCategory,
    Interest,
    ExtraBagOption,
    GalleryImage,
    Slide,
    Destination,
)
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
        "slides": Slide.objects.filter(is_active=True).order_by("order"),
        "images": GalleryImage.objects.all().order_by("-created_at")[:8],
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email
            subject = "New Contact Message Received"
            message = f"""
            Name: {contact.name}
            Email: {contact.email}
            Message:
            {contact.message}
            """
            recipient_list = [os.environ.get("EMAIL_HOST_USER")]

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactMessageForm()
    return render(request, "contact.html", {"form": form})


def blog_list(request):
    featured = BlogPost.objects.filter(is_featured=True).order_by("-created_at").first()
    posts = BlogPost.objects.filter(is_featured=False).order_by("-created_at")
    return render(
        request, "blog/blog_list.html", {"featured_post": featured, "posts": posts}
    )


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog/blog_detail.html", {"post": post})


def booking(request):
    if request.method == "POST":
        form = TourBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Send confirmation email
            send_confirmation_email(booking, request)

            messages.success(request, "Your tour has been booked successfully!")
            return redirect("booking_confirmation", booking_id=booking.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TourBookingForm()

    return render(
        request,
        "tours/book_tour.html",
        {
            "form": form,
            "interests_by_category": (
                form.interests_by_category
                if hasattr(form, "interests_by_category")
                else {}
            ),
        },
    )


def send_confirmation_email(booking, request):
    try:
        subject = f"Tour Booking Confirmation - {booking.tour_date}"
        confirmation_url = request.build_absolute_uri(
            reverse("booking_confirmation", args=[booking.id])
        )

        context = {
            "booking": booking,
            "confirmation_url": confirmation_url,
        }

        text_message = render_to_string("tours/booking_confirmation.txt", context)
        html_message = render_to_string("tours/booking_confirmation.html", context)

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
    return render(request, "tours/booking_confirmation.html", {"booking": booking})


def tour_gallery(request):
    images = GalleryImage.objects.all().order_by("-created_at")
    return render(request, "explore/gallery.html", {"images": images})


def destination_list(request):
    """
    View to display all active destinations
    """
    destinations = Destination.objects.filter(is_active=True).order_by("name")
    context = {
        "destinations": destinations,
        "meta_title": "Explore Ghana's Top Destinations",
        "meta_description": "Discover the most beautiful and "
        "historic destinations in Ghana with Nasaf Tours",
    }
    return render(request, "destinations/list.html", context)


def destination_detail(request, slug):
    """
    View to display a single destination detail page
    """
    destination = get_object_or_404(Destination, slug=slug, is_active=True)

    # Get related destinations (excluding current one)
    related_destinations = (
        Destination.objects.filter(is_active=True)
        .exclude(id=destination.id)
        .order_by("?")[:3]
    )  # Random 3 destinations

    context = {
        "destination": destination,
        "related_destinations": related_destinations,
        "meta_title": f"{destination.name} - Ghana Travel Guide",
        "meta_description": destination.description[:160],  # First 160 chars for meta
    }
    return render(request, "destinations/detail.html", context)
