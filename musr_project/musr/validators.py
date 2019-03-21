import re
from django.core import validators


# Ensure that usernames are URL-safe as they will later appear in URLS
class MUSRUsernameValidator(validators.RegexValidator):
    regex = r"^[\w]+$"
    message = "Enter a valid username. This value may contain only English letters and numbers."
    flags = re.ASCII


custom_username_validators = [
    MUSRUsernameValidator(),
    validators.MaxLengthValidator(20),
]
