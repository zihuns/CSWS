from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone

from .managers import UserManager
from .validators import UOSStudentIdValidator

class User(AbstractBaseUser, PermissionsMixin):
    uos_id_validator = ASCIIUsernameValidator()
    uos_student_id_validator = UOSStudentIdValidator()

    uos_id = models.CharField(
        'UOS portal ID',
        help_text='Enter UOS portal ID.',
        unique=True,
        max_length=30,
        error_messages={
            'unique': 'Already existing UOS portal ID.'
        },
        validators=[uos_id_validator],
    )
    name = models.CharField(
        'name',
        help_text='Enter your name.',
        max_length=20,
    )
    student_id = models.CharField(
        'UOS student ID',
        help_text='Enter your student ID.',
        max_length=10,
        unique=True,
        error_messages={
            'unique': 'Already existing student ID.'
        },
        validators=[UOSStudentIdValidator],
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        'date joined',
        default=timezone.now,
    )
    objects = UserManager()

    # email = models.EmailField(blank=True)

    #EMAIL_FIELD = 'uos_id' + '@uos.ac.kr'
    USERNAME_FIELD = 'uos_id'
    REQUIRED_FIELDS = ['name', 'student_id']
    # REQUIRED_FIELDS = ['email', 'student_id']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.uos_id

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.uos_id + '@uos.ac.kr'], **kwargs)
