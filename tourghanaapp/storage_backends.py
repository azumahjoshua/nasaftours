import os
from storages.backends.azure_storage import AzureStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class AzureMediaStorage(AzureStorage):
    account_name = os.getenv("AZURE_ACCOUNT_NAME", "nasaftoursstoragedev")
    account_key = os.getenv("AZURE_ACCOUNT_KEY")
    azure_container = "media"
    expiration_secs = None
    file_overwrite = False
    location = ""  # This ensures files go to the root of the container

    def get_valid_name(self, name):
        """Sanitize the filename for Azure storage"""
        name = super().get_valid_name(name)
        # Remove any special characters that might cause issues
        return name.replace(" ", "_").lower()

    def url(self, name, expire=None):
        """Generate proper URL for Azure storage"""
        url = super().url(name, expire=expire)
        # Ensure the URL uses HTTPS
        return url.replace("http://", "https://") if url else url


@deconstructible
class CkeditorAzureStorage(AzureMediaStorage):
    """Special storage for CKEditor uploads"""

    location = "ckeditor"  # Files will be stored in 'media/ckeditor/'

    def get_available_name(self, name, max_length=None):
        """Prevent file overwrites by adding suffixes"""
        if self.exists(name):
            name_parts = os.path.splitext(name)
            counter = 1
            while self.exists(name):
                name = f"{name_parts[0]}_{counter}{name_parts[1]}"
                counter += 1
        return name


# import os
# from storages.backends.azure_storage import AzureStorage
# from django.utils.deconstruct import deconstructible

# @deconstructible
# class AzureMediaStorage(AzureStorage):
#     account_name = os.getenv("AZURE_ACCOUNT_NAME", "nasaftoursstoragedev")
#     account_key = os.getenv("AZURE_ACCOUNT_KEY")
#     azure_container = 'media'
#     expiration_secs = None
#     file_overwrite = False
#     location = ''

#     def get_valid_name(self, name):
#         """
#         Clean the filename to remove any special characters that might cause issues with Azure
#         """
#         name = super().get_valid_name(name)
#         # Azure-specific sanitization if needed
#         return name

#     def url(self, name, expire=None):
#         """
#         Override URL generation to use Azure CDN if configured
#         """
#         url = super().url(name, expire=expire)
#         # Add any custom URL processing here if needed
#         return url

# class CkeditorAzureStorage(AzureMediaStorage):
#     """
#     Special storage for CKEditor uploads to keep them organized
#     """
#     azure_container = 'media'  # Same container but different path
#     location = 'ckeditor'  # All CKEditor uploads go to media/ckeditor/

#     def get_available_name(self, name, max_length=None):
#         """
#         Prevent overwriting existing files with similar names
#         """
#         if self.exists(name):
#             name_parts = os.path.splitext(name)
#             counter = 1
#             while self.exists(name):
#                 name = f"{name_parts[0]}_{counter}{name_parts[1]}"
#                 counter += 1
#         return name
