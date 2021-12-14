from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, uos_id, name, student_id, password, **extra_fields):
        if not uos_id:
            raise ValueError('The given username must be set.')
        user = self.model(uos_id=uos_id, name=name, student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, uos_id, name, student_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(uos_id, name, student_id, password, **extra_fields)

    def create_superuser(self, uos_id, name, student_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(uos_id, name, student_id, password, **extra_fields)
        