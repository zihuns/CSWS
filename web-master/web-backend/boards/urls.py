from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
        # 홈 화면
        path('', views.HomeView.as_view(), name='home'),

        # 과목 메인 화면
        path('<title>/', views.SubjectView.as_view(), name='subject'),

        # 과목 상세 화면(과제 목록 확인, 과제 출제)
        path('<title>/<int:year>/<class_no>', views.SubjectDetailView.as_view(), name='subject_detail'),

        # 과제 등록 화면
        path('<title>/<int:year>/<class_no>/assignment/new/', views.AssignmentEditView.as_view(), name='assignment_new'),
        path('<title>/<int:year>/<class_no>/assignment/new/compile', views.compile, name='compile'),
        
        # 과제 상세 화면(과제 상세 확인, 과제 제출, 과제 수정)
        path('<title>/<int:year>/<class_no>/assignment/<int:pk>/', views.AssignmentView.as_view(), name='assignment_detail'),
        path('<title>/<int:year>/<class_no>/assignment/<int:pk>/input', views.assignment_input, name='assignment_input'),
        path('<title>/<int:year>/<class_no>/assignment/<int:pk>/assignment_input_output_setting', views.assignment_input_output_setting, name='assignment_input_output_setting'),
        path('<title>/<int:year>/<class_no>/assignment/<int:pk>/compile', views.assignment_compile, name='assignment_compile'),

        # 과제 점수 등록
        path('<title>/<int:year>/<class_no>/assignment/<int:pk>/jumsu/', views.AssignmentView.as_view(), name='jumsu'),

        # 제출된 과제 일괄 다운로드
        path('<title>/<int:year>/<class_no>/assignment/<int:pk>/download/', views.download_submitted_assignment_files, name='download'),

        # 게시글 상세 화면, 댓글 등록 화면
        path('<title>/boards/<int:pk>/', views.PostView.as_view(), name='post_detail'),
        
        # 게시글 등록 화면
        path('<title>/boards/new/', views.NewPostView.as_view(), name='post_new'),

        # 게시글 수정
        path('<title>/boards/<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),

        # 게시글 수정 화면에서 코드 리턴해주기
        path('<title>/boards/<int:pk>/edit/<filename>', views.PostEditView.as_view(), name='post_edit'),

        # 게시글 삭제
        path('<title>/boards/<int:pk>/delete', views.post_delete, name='post_delete'),

        # 게시글에서 코드 리턴해주기
        path('<title>/boards/<int:pk>/<filename>', views.get_source_code, name='get_source_code'),
        
        # 댓글 수정
        path('<title>/boards/<int:p_pk>/comment_edit/<int:c_pk>/', views.CommentEditView.as_view(), name='comment_edit'),

        # 댓글 삭제
        path('<title>/boards/<int:p_pk>/comment_delete/<int:c_pk>/', views.comment_delete, name='comment_delete'),
]