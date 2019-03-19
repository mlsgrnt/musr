import re
from django.core import validators


class MUSRUsernameValidator(validators.RegexValidator):
    regex = r"^[\w]+$"
    message = "Enter a valid username. This value may contain only English letters and numbers"
    flags = re.ASCII


custom_username_validators = [MUSRUsernameValidator()]
