import re

from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class UOSStudentIdValidator(RegexValidator):
	regex = r'^[a-zA-Z0-9]\d{9}\Z'
	message = _(
		'Enter a valid student id.'
		'10 digits of 10 numbers or 10 digits of 1 alphabet and 9 numbers'
	)
	flags = re.ASCII
