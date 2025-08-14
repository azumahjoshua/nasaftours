# forms.py
from django import forms
from .models import ContactMessage
from .models import TourBooking, Interest, ExtraBagOption

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-amber-500 focus:border-amber-500',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-amber-500 focus:border-amber-500',
                'placeholder': 'Email Address'
            }),
            'message': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-amber-500 focus:border-amber-500',
                'rows': 5,
                'placeholder': 'Your Message'
            }),
        }



class TourBookingForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "checkbox-class"
        }),
        required=False,
        label="What are your interests?"
    )

    extra_bag_options = forms.ModelMultipleChoiceField(
        queryset=ExtraBagOption.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "checkbox-class"
        }),
        required=False,
        label="One Extra Bag Options"
    )

    class Meta:
        model = TourBooking
        fields = [
            'full_name', 'email', 'phone',
            'tour_date', 'start_time', 'number_of_travelers', 'duration_hours',
            'interests', 'extra_bag_options',
            'how_did_you_hear', 'join_mailing_list', 'additional_notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'Enter your full name',
                'aria-label': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'Enter your email',
                'aria-label': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'Enter your phone number',
                'aria-label': 'Phone Number'
            }),
            'tour_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'aria-label': 'Tour Date'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'aria-label': 'Start Time'
            }),
            'number_of_travelers': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'Number of travelers',
                'aria-label': 'Number of Travelers'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'Duration in hours',
                'aria-label': 'Tour Duration'
            }),
            'how_did_you_hear': forms.TextInput(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'How did you hear about us?',
                'aria-label': 'Referral Source'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full py-2 px-4 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'rows': 4,
                'placeholder': 'Any special requests or notes?',
                'aria-label': 'Additional Notes'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interests_by_category = {}
        for interest in Interest.objects.all().select_related('category'):
            cat = interest.category.name
            self.interests_by_category.setdefault(cat, []).append(interest)