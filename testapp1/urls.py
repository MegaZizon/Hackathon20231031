from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.signup,name="main_signup"),
    # 회원가입 페이지 뷰
    path('signup/join',views.join,name="main_join"),
    # 회원 등록
    path('verifyCode',views.verifyCode,name="main_verifyCode"),
    # 이메일 인증 코드 전송
    path('verify',views.verify,name="main_verify"),
    # 이메일 인증 코드 확인
    path('logout',views.logout,name="main_logout"),
    # 로그아웃
    path('write/',views.write,name="main_write"),
    # 글쓰기 뷰
    path('write/submit', views.write_submit), 
    # 글 등록
    path('search/<str:searchStr>', views.search), 
    # 제목으로 검색
    path('post/<str:id>', views.post_detail), 
    # 글 상세 페이지 뷰
    path('cost/<str:cost>', views.cost), 
    # 시세 검색
    path('vote/<str:id>', views.post_vote), 
    # 글 추천
    path('mypage/', views.mypage), 
    # 내 정보 페이지 뷰
    path('write/img/<str:filename>', views.upload_img), 
    # 이미지 업로드 Ajax 통신
    path('write/checkPrice/<str:searchStr>', views.check_price), 
    # 시세 검색 Ajax 통신
    path('',views.index,name="main_index"),
    # 메인 페이지
]