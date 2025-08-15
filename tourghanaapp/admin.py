from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    ContactMessage,
    BlogPost,
    TourBooking,
    InterestCategory,
    Interest,
    ExtraBagOption,
    GalleryImage,
    Slide,
    Destination,
)
from django.utils.html import format_html


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("title", "highlight", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "highlight", "description")
    list_editable = ("order",)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "location", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


# Register ContactMessage
admin.site.register(ContactMessage)


# Updated BlogPostAdmin with CKEditor
class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogPost
        fields = "__all__"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ("title", "created_at", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px;"/>', obj.image.url)
        return ""

    image_preview.short_description = "Preview"


class InterestInline(admin.TabularInline):
    model = Interest
    extra = 1


class InterestCategoryAdmin(admin.ModelAdmin):
    inlines = [InterestInline]


class TourBookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "tour_date", "start_time", "created_at")
    list_filter = ("tour_date", "created_at")
    search_fields = ("full_name", "email")
    filter_horizontal = ("interests", "extra_bag_options")


admin.site.register(InterestCategory, InterestCategoryAdmin)
admin.site.register(ExtraBagOption)
admin.site.register(TourBooking, TourBookingAdmin)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "created_at")
    search_fields = ("title",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px;"/>', obj.image.url)
        return ""

    image_preview.short_description = "Preview"
