from django.contrib import admin
from .models import *


# Register your models here.


admin.site.register(Member)
admin.site.register(Teacher)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(CommentReply)
admin.site.register(BookCategory)
admin.site.register(BlogCategory)
admin.site.register(Book)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerReply)