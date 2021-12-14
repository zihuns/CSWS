import datetime
import os
import zipfile
import sys
from mimetypes import guess_type
import json
from filecmp import cmp

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView 
from django.http import Http404, HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils import timezone
from django.views import View
from django.core.files import File
from django.http import JsonResponse


from .models import Course
from .models import Subject, DetailedSubject, Assignment, Post, Comment, AssignmentSubmission
from .forms import PostForm, CommentForm, AssignmentForm, AssignmentSubmissionForm
from accounts.models import User
from project.settings import BASE_DIR


YEARS = []
for r in range(2019, datetime.datetime.now().year+1):
     YEARS.append(r)

# 파일 확장자
extensions = {
    "C":"c","CPP":"cpp","CLOJURE":"clj","CSS":"css","CSHARP":"cs",
    "GO":"go","HASKELL":"hs","JAVA":"java","JAVASCRIPT":"js",
    "LISP":"scm","OBJECTIVEC":"m","PERL":"pl","PHP":"php",
    "PYTHON":"py","RUBY":"rb","R":"r","RUST":"rs","SCALA":"scala",
    "TEXT":"txt"
}


#--- 게시판 홈 화면
class HomeView(View):
    template_name = 'boards/home.html'

    def get(self, request):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 수강중인 과목들
        courses = Course.objects.all().filter(student=request.user).order_by('-subject__year', 'subject__subject__subject_no')
        return render(request, self.template_name, {'courses': courses, 'years': list(reversed(YEARS)),})



#--- 과목 메인 화면
class SubjectView(View):
    template_name = 'boards/subject.html'

    def get(self, request, title):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 상세 과목, 과목별 게시판 글 띄우기
        subject = get_object_or_404(Subject, title=title)
        subjects = DetailedSubject.objects.filter(subject=subject).order_by('-year', '-semester', 'class_no')
        posts = Post.objects.filter(subject=subject).order_by('-last_modified_date')[:5]
        return render(request, self.template_name, {'title': title, 'sub': subject, 'subjects': subjects, 'years': list(reversed(YEARS)), 'posts': posts})



#--- 과목 상세 화면
class SubjectDetailView(View):
    template_name = 'boards/subject_detail.html'

    # 공통 객체
    subject = None
    detailed_subject = None

    def get(self, request, title, year, class_no):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(request, title, year, class_no)

        # 과목의 과제 목록 띄우기
        assignments = Assignment.objects.filter(subject=self.detailed_subject).order_by('-due_date', '-created_date')
        return render(request, 'boards/subject_detail.html', {'subject': self.detailed_subject, 'assignments': assignments})


    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, request, title, year, class_no):
        self.subject = get_object_or_404(Subject, title=title)
        self.detailed_subject = get_object_or_404(DetailedSubject, subject=self.subject, year=year, class_no=class_no)


#--- 과제 출제시 컴파일
def compile(request, title, year, class_no):
    crust_file_path = os.path.join(BASE_DIR, "boards/crust.py")

    dir_path = os.path.join(BASE_DIR, "media/" + title + "/" + str(year) + "/" + class_no + "/")
    if not os.path.isdir(dir_path):
        os.makedirs(os.path.join(dir_path))

    os.system("cp " + crust_file_path + " " + dir_path)

    input_filename = "input.txt"
    crust_file_name = "crust.py"
    output_filename_template = "output{0}.txt"
    output_filename = None
    source_filename = None
    return_filename = "return.txt"
    exe_filename = "source"
    inputs = []
    response_data = {}

    if request.POST.get('action') == 'post':
        lang = request.POST.get('lang')
        code = request.POST.get('code')
        input = request.POST.get('input')
        source_filename = "source." + extensions[lang]


        def make_input():
            input_file = open(dir_path + input_filename, "w")
            input_file.write(input)
            input_file.close()
            return 
        
        def make_source():
            source_file = open(dir_path + source_filename, "w")
            source_file.write(code)
            source_file.close()
            return

        def run_code(): 
            # output_filename = output_filename_template.format(str(i))
             
            # if(lang == 'C'):
            #     # 컴파일 & 결과파일 생성
            #     os.system('gcc -o ' + dir_path + exe_filename + ' ' + dir_path + source_filename + ' && ' + dir_path + exe_filename + ' > ' + dir_path + output_filename)
            #     os.remove(dir_path + exe_filename) # 실행파일 삭제

            if(lang == 'PYTHON'):
                # 결과파일 생성
                os.system("python3 " + dir_path + crust_file_name)
                # os.system('python3 ' + dir_path + source_filename + ' > ' + dir_path + output_filename) # > write or overwrite , >> append
            
            return

        def make_return_file(input_num):
            with open(dir_path + return_filename, "a") as return_file:
                for i in range(1, input_num + 1):
                    output_filename = output_filename_template.format(str(i))
                    output_file = open(dir_path + output_filename, "r")
                    return_file.write("#" + str(i) + "\n")
                    return_file.write(output_file.read())
                    return_file.write("\n")
                    output_file.close()
                return_file.close()
                
            return


        make_input() # input 파일 생성
        # input_file = open(dir_path + input_filename, "r")
        # num_of_input = int(input_file.readline())
        # # for i in range(1, num_of_input + 1):
        # #     run_code(i) # output 파일 생성
        # input_file.close()
        make_source()
        run_code()

        input_file = open(dir_path + input_filename, "r")
        make_return_file(int(input_file.readline()))
        input_file.close()

        ret = open(dir_path + return_filename, "r")
        ret_content = ret.read()
        ret.close()

        os.remove(dir_path + return_filename) # 리턴파일 삭제
        os.remove(dir_path + crust_file_name)

        response_data['output'] = ret_content

        return JsonResponse(response_data)



#--- 과제 출제 화면
# TODO : 출제한 과제 수정 구현
class AssignmentEditView(View):
    template_name = 'boards/assignment_new.html'

    # 공통 객체
    subject = None
    detailed_subject = None

    dir_path = None
    input_filename = "input.txt"
    output_filename = None
    output_filename_template = "output{0}.txt"
    source_filename = None


    def get(self, request, title, year, class_no):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')
        
        # 공통 객체 할당
        self.set_objects(request, title, year, class_no)

        # 과목의 관리자 아닌 사람이 접근
        if request.user != self.detailed_subject.admin:
            # JS로 잘못된 접근입니다! 같은 창 띄워주면 좋음
            return redirect('boards:subject_detail', title=title, year=year, class_no=class_no)
        
        form = AssignmentForm()

        return render(request, self.template_name, { 'form': form, 'title':title, 'year':year, 'class_no':class_no })


    def post(self, request, title, year, class_no):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(request, title, year, class_no)

        # 과목의 관리자 아닌 사람이 접근
        if request.user != self.detailed_subject.admin:
            # JS로 잘못된 접근입니다! 같은 창 띄워주면 좋음
            return redirect('boards:subject_detail', title=title, year=year, class_no=class_no)
        
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.subject = self.detailed_subject
            assignment.save()

            if assignment.code_submit_assignment:
                assignment.lang = request.POST.get('lang')
                assignment.save()
                self.source_filename = "source." + extensions[assignment.lang]
                
                # 과제 이름으로 폴더 만들어서 기존 input, output, source 파일 이동
                assignment_dir = self.dir_path + str(assignment.pk)
                if not os.path.isdir(assignment_dir):
                    os.makedirs(os.path.join(assignment_dir))
                # test case 갯수 가져옴. output 옮기기 위함
                input_file = open(self.dir_path + self.input_filename, "r")
                num_of_input = int(input_file.readline())
                input_file.close()
                
                for i in range(1, num_of_input + 1): # output 파일 이동
                    self.output_filename = self.output_filename_template.format(i)
                    os.system('mv ' + self.dir_path + self.output_filename + " " + assignment_dir + "/origin_" + self.output_filename) # output 파일 이동
                
                os.system('mv ' + self.dir_path + self.input_filename + " " + assignment_dir) # input 파일 이동
                os.system('mv ' + self.dir_path + self.source_filename + " " + assignment_dir + "/origin_" + self.source_filename) # source 파일 이동

            
            # 과제 생성과 동시에 수강중인 학생들의 AssignmentSubmission row 디비에 저장
            courses = Course.objects.filter(subject=self.detailed_subject)
            for course in courses:
                tmp = AssignmentSubmission()
                tmp.assignment = assignment
                tmp.student = course.student
                tmp.save()

        return redirect('boards:assignment_detail', title=title, year=year, class_no=class_no, pk=assignment.pk)

    
    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, request, title, year, class_no):
        self.subject = get_object_or_404(Subject, title=title)
        self.detailed_subject = get_object_or_404(DetailedSubject, subject=self.subject, year=year, class_no=class_no)
        self.dir_path = os.path.join(BASE_DIR, "media/" + title + "/" + str(year) + "/" + class_no + "/")


# 과제의 input 파일 읽어서 리턴하는 함수
def assignment_input(request, title, year, class_no, pk):
    input_filename = os.path.join(BASE_DIR, "media/" + title + "/" + str(year) + "/" + class_no + "/" + str(pk) + "/" + "input.txt")
    input_file = open(input_filename, 'r')
    input = input_file.read()
    input_file.close()
    return HttpResponse(input)


def assignment_input_output_setting(request, title, year, class_no, pk):
    dir_path = os.path.join(BASE_DIR, "media/" + title + "/" + str(year) + "/" + class_no + "/" + str(pk) + "/" )
    
    input_filename = dir_path + "input.txt"
    input_file = open(input_filename, 'r')
    input_file.readline()
    input1 = input_file.readline()
    input2 = input_file.readline()
    input3 = input_file.readline()
    input_file.close()

    output1_filename = dir_path + "origin_output1.txt"
    output1_file = open(output1_filename, 'r')
    output1 = output1_file.read()
    output1_file.close()

    output2_filename = dir_path + "origin_output2.txt"
    output2_file = open(output2_filename, 'r')
    output2 = output2_file.read()
    output2_file.close()

    output3_filename = dir_path + "origin_output3.txt"
    output3_file = open(output3_filename, 'r')
    output3 = output3_file.read()
    output3_file.close()

    res = { 'input1': input1, 'input2': input2, 'input3': input3, 'output1': output1, 'output2': output2, 'output3': output3 }

    return HttpResponse(json.dumps(res))



def assignment_compile(request, title, year, class_no, pk):
    print("진입")
    crust_file_path = os.path.join(BASE_DIR, "boards/crust.py")
    dir_path = os.path.join(BASE_DIR, "media/" + title + "/" + str(year) + "/" + class_no + "/" + str(pk) + "/")
    os.system("cp " + crust_file_path + " " + dir_path)

    input_filename = "input.txt"
    crust_file_name = "crust.py"
    output_filename_template = "output{0}.txt"
    output_filename = None
    origin_output_filename_template = "origin_output{0}.txt"
    origin_output_filename = None
    source_filename = None
    return_filename = "return.txt"
    response_data = {}
    same_count = None

    if request.POST.get('action') == 'post':
        lang = request.POST.get('lang')
        code = request.POST.get('code')
        source_filename = "source." + extensions[lang]

        def make_source():
            source_file = open(dir_path + source_filename, "w")
            source_file.write(code)
            source_file.close()
            return

        def run_code():             
            # if(lang == 'C'):
            #     # 컴파일 & 결과파일 생성
            #     os.system('gcc -o ' + dir_path + exe_filename + ' ' + dir_path + source_filename + ' && ' + dir_path + exe_filename + ' > ' + dir_path + output_filename)
            #     os.remove(dir_path + exe_filename) # 실행파일 삭제

            if(lang == 'PYTHON'):
                # 결과파일 생성
                os.system("python3 " + dir_path + crust_file_name)
                # os.system('python3 ' + dir_path + source_filename + ' > ' + dir_path + output_filename) # > write or overwrite , >> append
            
            return

        def make_return_file(input_num):
            with open(dir_path + return_filename, "a") as return_file:
                same_count = 0
                for i in range(1, input_num + 1):
                    output_filename = output_filename_template.format(str(i))
                    origin_output_filename = origin_output_filename_template.format(str(i))
                    output_file = open(dir_path + output_filename, "r")
                    return_file.write("#" + str(i) + "\n")
                    return_file.write(output_file.read())
                    return_file.write("\n")
                    output_file.close()
                    if cmp(dir_path + output_filename, dir_path + origin_output_filename):
                        same_count = same_count + 1
                
                return_file.write("총 " + str(input_num) +"개 중 " + str(same_count) + "개 맞추셨습니다.")
                return_file.close()
                
            return

        def remove_output_file(input_num):
            for i in range(1, input_num + 1):
                output_filename = output_filename_template.format(str(i))
                os.system("rm " + dir_path + output_filename)

        make_source()
        run_code()

        input_file = open(dir_path + input_filename, "r")
        input_size = int(input_file.readline())
        make_return_file(input_size)
        input_file.close()

        ret = open(dir_path + return_filename, "r")
        ret_content = ret.read()
        ret.close()

        remove_output_file(input_size)
        os.remove(dir_path + return_filename) # 리턴파일 삭제
        os.remove(dir_path + crust_file_name)

        os.system("mv " + dir_path + source_filename + " " + dir_path + request.user.uos_id + "_" + source_filename)


        response_data['output'] = ret_content
        return JsonResponse(response_data)




    input_filename = os.path.join(BASE_DIR, "media/" + title + "/" + str(year) + "/" + class_no + "/" + str(pk) + "/" + "input.txt")
    input_file = open(input_filename, 'r')
    input = input_file.read()
    input_file.close()
    return HttpResponse(input)

#--- 과제 상세 화면
class AssignmentView(View):
    template_name = 'boards/assignment.html'

    # 공통 객체
    assignment = None
    subject = None
    detailedSubject = None

    # 렌더링할 때 넘길 것들
    form = None
    submitted = None
    submitted_all = None

    # 접속 시간
    time = timezone.now()


    def get(self, request, title, year, class_no, pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(request, title, year, class_no, pk)


        # 관리자가 접근 -> 제출된 파일 목록을 보여줌
        if request.user == self.detailedSubject.admin:
            self.submitted_all = AssignmentSubmission.objects.filter(assignment=self.assignment).order_by('student__student_id')


        # 수강생이 접근 -> 본인이 제출했는지 여부를 보여줌
        else:
            try:
                self.submitted = AssignmentSubmission.objects.get(student=request.user, assignment=self.assignment)
            except AssignmentSubmission.DoesNotExist:
                try:
                    course = Course.objects.get(student=request.user, subject=self.detailedSubject)
                    self.submitted = AssignmentSubmission(assignment=self.assignment, student=request.user)
                    self.submitted.save()

                except Course.DoesNotExist:
                    print("우짤꼬")

             
            # 제출기한 이내 -> 과제 제출 가능
            if self.assignment.due_date >= self.time:
                self.form = AssignmentSubmissionForm(None)
        
        return render(request, self.template_name, { 'assignment': self.assignment, 'form': self.form, 'submitted': self.submitted, 'submitted_all': self.submitted_all, })

    
    def post(self, request, title, year, class_no, pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(request, title, year, class_no, pk)

        # 관리자가 접근 -> 점수 등록
        if request.user == self.detailedSubject.admin:
            jumsus = request.POST.getlist('jumsu')
            pks = request.POST.getlist('pk')
            for i in range(0, len(pks)):
                self.submitted = get_object_or_404(AssignmentSubmission, pk=pks[i].rstrip('/'))
                self.submitted.point = jumsus[i]
                self.submitted.save()


        # 수강생이 접근 -> 과제 제출
        else:
            # 제출기한 이내
            if self.assignment.due_date >= self.time:
                form = AssignmentSubmissionForm(request.POST, request.FILES)

                if form.is_valid():
                    self.submitted = AssignmentSubmission.objects.get(student=request.user, assignment=self.assignment)

                    # 파일 수정
                    if self.submitted.file: 
                        os.remove(self.submitted.file.path)
                    
                    self.submitted.original_file_name = form.cleaned_data['file'].name
                    self.submitted.file = form.cleaned_data['file']
                    self.submitted.submission_date = self.time
                    self.submitted.save()
                
            # 제출기한 지남
            else:
                pass
        
        return redirect('boards:assignment_detail', title=title, year=year, class_no=class_no, pk=pk)
         

    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, request, title, year, class_no, pk):
        self.assignment = get_object_or_404(Assignment, pk=pk)
        self.subject = get_object_or_404(Subject, title=title)
        self.detailedSubject = get_object_or_404(DetailedSubject, subject=self.subject, year=year, class_no=class_no)



#--- 제출된 과제 파일 일괄 다운로드
def download_submitted_assignment_files(request, title, year, class_no, pk):
    # 인증되지 않은 사용자
    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(Subject, title=title)
    detailed_subject = get_object_or_404(DetailedSubject, subject=subject, year=year, class_no=class_no)
    assignment = get_object_or_404(Assignment, pk=pk)
    submitted_all = AssignmentSubmission.objects.filter(assignment=assignment)

    # 과목의 관리자 아닌 사람이 접근
    if request.user != detailed_subject.admin:
        # JS로 잘못된 접근입니다! 같은 창 띄워주면 좋음
        return redirect('boards:subject_detail', title=title, year=year, class_no=class_no)


    # 압축
    zip_name = os.path.join(BASE_DIR, "media/" + assignment.subject.__str__() + "/" + assignment.title + ".zip")
    assignment_zip = zipfile.ZipFile(zip_name, 'w')
    for s in submitted_all:
        if s.file:
            assignment_zip.write(s.file.path, os.path.basename(s.file.name), compress_type=zipfile.ZIP_DEFLATED)
    assignment_zip.close()

    with open(zip_name, "rb") as f:
        response = HttpResponse(f, content_type=guess_type(zip_name)[0])
        response['Content-Length'] = len(response.content)
        # TODO: 밑에 파일 이름 지정해서 다운로드하는거 나중에 시간 나면 더 보기
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % assignment.title
        os.remove(zip_name)
        return response
    


#--- 게시글 상세
class PostView(View):
    template_name = 'boards/post_detail.html'
    form = CommentForm()

    # 공통 객체
    post = None


    def get(self, request, title, pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        self.set_objects(pk)

        comments = Comment.objects.filter(post=self.post).order_by('last_modified_date')
        return render(request, self.template_name, {'post': self.post, 'comments': comments, 'form': self.form })


    # 댓글 쓰기
    def post(self, request, title, pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        self.set_objects(pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post
            comment.author = request.user
            comment.last_modified_date = timezone.now()
            comment.save()
            return redirect('boards:post_detail', title=title, pk=self.post.pk)


    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, pk):
        self.post = get_object_or_404(Post, pk=pk)


# 소스 코드 읽어서 게시글 창으로 리턴하는 함수
def get_source_code(request, title, pk, filename):
    filepath = os.path.join(BASE_DIR, "media/" + title + "/boards/") + filename
    file = open(filepath, 'r')
    code = file.read()
    file.close()
    return HttpResponse(code)


#--- 새로운 게시글 쓰기 뷰
class NewPostView(View):
    template_name = 'boards/post_new.html'

    # 공통 객체
    subject = None

    def get(self, request, title):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        self.set_objects(title)

        form = PostForm()
        return render(request, self.template_name, { 'form': form, 'title': title })            
        
    
    def post(self, request, title):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        self.set_objects(title)

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.subject = self.subject
            post.author = request.user

            if post.contain_code == True:
                post.lang = request.POST.get('lang')
                post.save()

                # 코드 파일로 저장
                code = request.POST.get('code')
                path = os.path.join(BASE_DIR, "media/" + title + "/boards/")
                if not os.path.isdir(path):
                    os.makedirs(os.path.join(path))
                filename = str(post.pk) + '.' + extensions[post.lang]
                f = open(path + filename, "w")
                f.write(code)
                f.close()
                post.code_file_name = filename

            
            post.save()
        return redirect('boards:post_detail', title=post.subject.title, pk=post.pk)


    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, title):
        self.subject = get_object_or_404(Subject, title=title)



#--- 게시글 수정 뷰
# TODO: 수정시 코드창 자동으로 띄우고 작성했던 뜨도록 수정
class PostEditView(View):
    template_name = 'boards/post_edit.html'

    # 공통 객체
    post = None

    def get(self, request, title, pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(pk)

        if request.user != self.post.author:
            # 잘못된 접근입니다 같은 창으로 리다이렉트 해야됨
            return redirect('boards:subject', title=title)

        form = PostForm(instance=self.post)
        return render(request, self.template_name, { 'form': form, 'post': self.post })


    def post(self, request, title, pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(pk)

        if request.user != self.post.author:
            # 잘못된 접근입니다 같은 창으로 리다이렉트 해야됨
            return redirect('boards:subject', title=title)

        form = PostForm(request.POST, instance=self.post)
        if form.is_valid():
            self.post = form.save(commit=False)
            self.post.last_modified_date = timezone.now()

            # 코드 수정
            if self.post.contain_code == True:
                self.post.lang = request.POST.get('lang')

                code = request.POST.get('code')
                path = os.path.join(BASE_DIR, "media/" + title + "/boards/")
                if self.post.code_file_name == None:    
                    filename = str(self.post.pk) + '.' + extensions[self.post.lang]
                    self.post.code_file_name = filename

                filename = self.post.code_file_name

                f = open(path + filename, "w")
                f.write(code)
                f.close()

            self.post.save()
            return redirect('boards:post_detail', title=self.post.subject.title, pk=self.post.pk)

    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, pk):
        self.post = get_object_or_404(Post, pk=pk)



#--- 게시글 삭제 뷰
def post_delete(request, title, pk):
    # 인증되지 않은 사용자
    if not request.user.is_authenticated:
        return redirect('login')

    post_to_delete = get_object_or_404(Post, pk=pk)

    if request.user != post_to_delete.author:
        # 잘못된 접근입니다 같은 창으로 리다이렉트 해야됨
        return redirect('boards:subject', title=title)
    
    post_to_delete.delete()
    return redirect('boards:subject', title=title)



#--- 댓글 수정 뷰
class CommentEditView(View):
    template_name = 'boards/comment_edit.html'
    
    # 공통 객체
    comment = None

    # 수정 창 접근
    def get(self, request, title, p_pk, c_pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(c_pk)

        if request.user != self.comment.author:
            # 잘못된 접근입니다 같은 창으로 리다이렉트 해야됨
            return redirect('boards:post_detail', title=self.comment.post.subject.title, pk=self.comment.post.pk)
        
        form = CommentForm(instance=self.comment)
        return render(request, self.template_name, {'form': form})


    # 수정
    def post(self, request, title, p_pk, c_pk):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')

        # 공통 객체 할당
        self.set_objects(c_pk)

        if request.user != self.comment.author:
            # 잘못된 접근입니다 같은 창으로 리다이렉트 해야됨
            return redirect('boards:post_detail', title=self.comment.post.subject.title, pk=self.comment.post.pk)


        form = CommentForm(request.POST, instance=self.comment)
        if form.is_valid():
            self.comment = form.save(commit=False)
            self.comment.last_modified_date = timezone.now()
            self.comment.save()
            return redirect('boards:post_detail', title=self.comment.post.subject.title, pk=self.comment.post.pk)

    # 공통으로 쓰이는 객체들 할당
    def set_objects(self, c_pk):
        self.comment = get_object_or_404(Comment, pk=c_pk)


# 댓글 삭제
def comment_delete(request, title, p_pk, c_pk):
    # 인증되지 않은 사용자
    if not request.user.is_authenticated:
        return redirect('login')

    comment_to_delete = get_object_or_404(Comment, pk=c_pk)

    if request.user != comment_to_delete.author:
        # 잘못된 접근입니다 같은 창으로 리다이렉트 해야됨
        return redirect('boards:post_detail', title=title, pk=p_pk)
    
    comment_to_delete.delete()
    return redirect('boards:post_detail', title=title, pk=p_pk)
    