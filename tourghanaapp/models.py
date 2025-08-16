from django.db import models
from django.utils.text import slugify
from PIL import Image
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from io import BytesIO
from django.core.files.base import ContentFile
from storages.backends.azure_storage import AzureStorage


class Slide(models.Model):
    title = models.CharField(max_length=200)
    highlight = models.CharField(max_length=200)
    description = models.TextField()
    cta_text = models.CharField(max_length=50)
    cta_link = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="slides/", storage=AzureStorage())
    alt = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Destination(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="The name of the destination (e.g., 'Cape Coast Castle')",
    )
    slug = models.SlugField(
        unique=True,
        help_text="A URL-friendly version of the name (auto-generated if blank)",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Specific location or region (e.g., 'Central Region, Ghana')",
    )
    description = RichTextField(help_text="Detailed description of the destination")
    image = models.ImageField(
        upload_to="destinations/",
        storage=AzureStorage(),
        help_text="Featured image for this destination",
    )
    is_active = models.BooleanField(default=True, help_text="Toggle destination visibility on the website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    content = RichTextUploadingField()  # This allows uploads
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True, storage=AzureStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    @property
    def has_image(self):
        """Check if image exists in storage"""
        return bool(self.image) and self.image.name

    def get_image_url(self):
        """Safely get image URL or return None"""
        if self.has_image:
            try:
                return self.image.url
            except Exception:
                return None
        return None

    def delete(self, *args, **kwargs):
        """Proper cleanup when deleting"""
        if self.has_image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Handle image resizing before saving
        if self.image and not kwargs.get("skip_image_processing", False):
            try:
                img = Image.open(self.image)
                max_width = 1200
                if img.width > max_width:
                    output_size = (max_width, int(max_width * img.height / img.width))
                    img = img.resize(output_size, Image.LANCZOS)

                    output = BytesIO()
                    img.save(output, format="JPEG", quality=85)
                    output.seek(0)

                    self.image.save(
                        os.path.basename(self.image.name),
                        ContentFile(output.read()),
                        save=False,
                        content_type="image/jpeg",  # Explicit content type
                    )
                    output.close()
            except Exception as e:
                print(f"Error processing image: {e}")
                # Consider logging this properly

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class InterestCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category.name}: {self.name}"


class ExtraBagOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    needs = models.TextField()

    def __str__(self):
        return self.name


class TourBooking(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    tour_date = models.DateField()
    start_time = models.TimeField()
    number_of_travelers = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    duration_hours = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    interests = models.ManyToManyField(Interest, blank=True)
    extra_bag_options = models.ManyToManyField(ExtraBagOption, blank=True)
    how_did_you_hear = models.TextField(blank=True, null=True)
    join_mailing_list = models.BooleanField(default=False)
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.full_name} on {self.tour_date}"

    class Meta:
        verbose_name = "Tour Booking"
        verbose_name_plural = "Tour Bookings"
        ordering = ["-created_at"]


class GalleryImage(models.Model):
    @property
    def has_image(self):
        return bool(self.image) and self.image.name

    def get_image_url(self):
        if self.has_image:
            try:
                return self.image.url
            except Exception:
                return None
        return None

    image = models.ImageField(
        upload_to="gallery_images/",
        storage=AzureStorage(),  # Use Azure Storage for gallery images
    )
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Add image optimization similar to BlogPost"""
        if self.image:
            try:
                img = Image.open(self.image)
                if img.width > 1200:
                    output_size = (1200, int(1200 * img.height / img.width))
                    img = img.resize(output_size, Image.LANCZOS)

                    output = BytesIO()
                    img.save(output, format="JPEG", quality=85)
                    output.seek(0)

                    self.image.save(
                        os.path.basename(self.image.name),
                        ContentFile(output.read()),
                        save=False,
                    )
                    output.close()
            except Exception as e:
                print(f"Error processing image: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)  # Better for cloud storage
        super().delete(*args, **kwargs)


# from django.db import models
# from django.utils.text import slugify
# from PIL import Image
# # from django_summernote.fields import SummernoteTextField
# # from ckeditor.fields import RichTextField, RichTextUploadingField
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
# from django.core.validators import MinValueValidator, MaxValueValidator
# import os

# # Create your models here.
# class ContactMessage(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.name} - {self.email}"


# class BlogPost(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True, blank=True)
#     # content = SummernoteTextField()
#     # content = RichTextField()
#     # content = models.TextField()
#     content = RichTextUploadingField()  # This allows uploads
#     image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_featured = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             base_slug = slugify(self.title)
#             slug = base_slug
#             counter = 1
#             while BlogPost.objects.filter(slug=slug).exists():
#                 slug = f"{base_slug}-{counter}"
#                 counter += 1
#             self.slug = slug

#         super().save(*args, **kwargs)

#         # Resize and optimize image if present
#         if self.image:
#             img = Image.open(self.image)
#             # img = self.image.path
#             img = Image.open(img)
#             max_width = 1200
#             if img.width > max_width:
#                 new_height = int(max_width * img.height / img.width)
#                 img = img.resize((max_width, new_height), Image.LANCZOS)
#                 img.save(img, optimize=True, quality=85)

#     def __str__(self):
#         return self.title


# class InterestCategory(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name

# class Interest(models.Model):
#     category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.category.name}: {self.name}"

# class ExtraBagOption(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     needs = models.TextField()

#     def __str__(self):
#         return self.name

# class TourBooking(models.Model):
#     # Personal Information
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20, blank=True, null=True)

#     # Tour Details
#     tour_date = models.DateField()
#     start_time = models.TimeField()
#     number_of_travelers = models.PositiveIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(50)]
#     )
#     duration_hours = models.PositiveIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(12)]
#     )

#     # Relationships
#     interests = models.ManyToManyField(Interest, blank=True)
#     extra_bag_options = models.ManyToManyField(ExtraBagOption, blank=True)

#     # Additional Information
#     how_did_you_hear = models.TextField(blank=True, null=True)
#     join_mailing_list = models.BooleanField(default=False)
#     additional_notes = models.TextField(blank=True, null=True)

#     # Meta information
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Booking for {self.full_name} on {self.tour_date}"

#     class Meta:
#         verbose_name = "Tour Booking"
#         verbose_name_plural = "Tour Bookings"
#         ordering = ['-created_at']


# class GalleryImage(models.Model):
#     image = models.ImageField(upload_to='gallery_images/')
#     title = models.CharField(max_length=200, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title if self.title else f"Image {self.id}"

#     def delete(self, *args, **kwargs):
#         if self.image:
#             if os.path.isfile(self.image.path):
#                 os.remove(self.image.path)
#         super().delete(*args, **kwargs)
