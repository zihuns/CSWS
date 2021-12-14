import datetime
import os

from django.db import models
from django.utils import timezone

from accounts.models import User

class Subject(models.Model):
    subject_no = models.IntegerField(
        primary_key=True,
        unique=True,
        null=False,
    )
    title = models.CharField(
        max_length=254,
        unique=True,
        null=False,
    )

    def __str__(self):
        return self.title


class DetailedSubject(models.Model):
    YEAR_CHOICES = []
    for r in range(2019, datetime.datetime.now().year+1):
        YEAR_CHOICES.append((r,r))
    
    SEMESTER = (('A10', 1), ('A20', 2))
    # CLASS_NUMBER = [(i,i) for i in range(1,6)]
    CLASS_NUMBER = []
    for i in range(1, 20):
        if i < 10:
            CLASS_NUMBER.append(('0' + str(i), '0' + str(i)))
        else :
            CLASS_NUMBER.append((str(i), str(i)))
    

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        related_name='detailed_subject',
        # related_query_name='detaild_subjects',
        null=True,
    )
    year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=False,
        default=datetime.datetime.now().year,
    )
    shyr = models.IntegerField(
        choices=((1,1),(2,2),(3,3),(4,4)),
        null=False,
        default=1,
    )
    semester = models.CharField(
        choices=SEMESTER,
        null=False,
        default='A10',
        max_length=3,
    )
    class_no = models.CharField(
        choices=CLASS_NUMBER,
        null=False,
        default='01',
        max_length=20,
    )
    professor = models.CharField(
        max_length=20,
    )
    admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null = True,
    )

    class Meta:
        unique_together = ('subject', 'year', 'semester', 'class_no')
        # unique_together = ('subject', 'year', 'semester', 'class_no')
    
    def __str__(self):
        return self.subject.title + '(' + str(self.year) + ')-' + str(self.class_no) + '분반'
        # return self.subject.title + '-' + self.semester
        # return self.subject.title + '(' + str(self.year) + ') - ' + self.SEMESTERS[self.semester]

class Assignment(models.Model):
    # 7일 뒤로 제출일 디폴트 설정
    due_time = datetime.datetime.combine(datetime.date.today(), datetime.time(23,59,59)) + datetime.timedelta(days=6)

    subject = models.ForeignKey(
        DetailedSubject, 
        on_delete=models.CASCADE,
        related_name='assignments',
        null=False,
    )
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    last_modified_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=due_time)
    point = models.IntegerField(default=100, null=False) # 배점
    code_submit_assignment = models.BooleanField(default=False)
    lang = models.CharField(max_length=30, default=None, null=True)

    def __str__(self):
        return self.title

def get_path(instance, filename):
    # 과목명/세부과목명/과제명/학생이름_파일명
    return '{0}/{1}/{2}/{3}_{4}{5}'.format(instance.assignment.subject.subject.title, instance.assignment.subject.__str__(), 
                instance.assignment, instance.student.student_id, instance.student.name, os.path.splitext(filename)[1])

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        null=False,
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    point = models.IntegerField(null=True) # 학생이 획득한 점수
    original_file_name = models.CharField(max_length=254, null=True)
    file = models.FileField(upload_to=get_path, null=True)
    submission_date = models.DateTimeField(null=True, default=timezone.now)
    code_file_name = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        unique_together = ('assignment', 'student',)

class Course(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='courses'
    )
    subject = models.ForeignKey(
        DetailedSubject,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('student', 'subject')
        
    def __str__(self):
        return self.student.name + self.subject.subject.title

class Post(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='posts',
    )
    title = models.CharField(max_length=254)
    text = models.TextField()
    last_modified_date = models.DateTimeField(default=timezone.now)
    contain_code = models.BooleanField(default=False)
    lang = models.CharField(max_length=30, default=None, null=True)
    code_file_name = models.CharField(max_length=255, default=None, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    text = models.TextField()
    last_modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
