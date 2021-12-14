from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Subject)
admin.site.register(DetailedSubject)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Comment)