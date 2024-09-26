from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.home,name="home"),
    path("terms-and-conditions/",views.terms,name="terms"),
    path("forgot/",views.forgot,name="forgot"),
    path("forgot/<str:pk>/",views.forgot_password,name="forgotpass"),
    path("forgot/reset/<str:pk>/",views.reset_password,name="resetpass"),
    path("privacy-policy/",views.privacy,name="privacy"),
    path("odf/",views.odf,name="odf"),
    path("otp/<str:pk>/",views.verify_otp,name="otp"),
    path("otp/resend/<str:pk>/",views.resend_otp,name="resend"),
    path("about/",views.about,name="about"),
    path("log-out/",views.sign_out,name="log-out"),
    path("log-in/",views.log_in,name="log-in"),
    path("sign-in/",views.sign_in,name="sign-in"),
    path("odf/your-questions/",views.yourq,name="yourq"),
    path("odf/question/<str:pk>/",views.odfq,name="odfq"),
    path("odf/answer-question/<str:pk>/",views.answer_question,name="answer-question"),
    path("odf/reply-answer/<str:pk>/",views.reply_answer,name="reply-answer"),
    path("odf/delete-answer/<str:pk>/",views.delete_answer,name="delete-answer"),
    path("odf/edit-reply-answer/<str:pk>/",views.edit_reply_answer,name="edit-reply-answer"),
    path("odf/edit-delete-answer/<str:pk>/",views.delete_reply_answer,name="delete-reply-answer"),
    path("odf/ask/",views.askq,name="askq"),
    path("ru-mse/",views.mselanding,name="mse"),
    path("ru-mse/courses/<str:pk>/",views.mselanding2,name="mse2"),
    path("ru-mse/courses/resources/<str:pk>/",views.mselanding3,name="mse3"),
    path("ru-mse/upload/",views.uploadresource,name="uploadresource"),
    path("blogs/<str:pk>/",views.blogs,name="blogs"),
    path("books/<str:pk>/",views.books,name="books"),
    path("blogs/blog/<str:pk>/",views.blog,name="blog"),
    path("blogs/blog/like/<str:pk>/",views.blog_like,name="blog-like"),
    path("blogs/blog/comment/<str:pk>/",views.blog_comment,name="blog-comment"),
    path("blogs/blog/comment/delete/<str:pk>/",views.delete_comment,name="delete-comment"),
    path("blogs/blog/comment/reply/delete/<str:pk>/",views.delete_reply_comment,name="delete-reply-comment"),
    path("blogs/blog/comment/reply/edit/<str:pk>/",views.edit_reply_comment,name="edit-reply-comment"),
    path("blogs/blog/reply-comment/<str:pk>/",views.reply_comment,name="reply-comment"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)