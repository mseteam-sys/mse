from django.db import models
from django.db.models import Model



class Member(models.Model):
    username = models.CharField(max_length=100,unique=True,primary_key=True)
    userimage = models.ImageField(upload_to="media/images/members/",blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    password = models.CharField(max_length=100,blank=True,null=True)
    fullname = models.CharField(max_length=100,blank=True,null=True)
    ru = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname

class Teacher(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(upload_to="media/images/teachers/",blank=True,null=True)
    expertise = models.CharField(max_length=1000,blank=True,null=True)
    link = models.CharField(max_length=1000,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    sem_id = models.CharField(max_length=100,primary_key=True,unique=True)
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_code = models.CharField(max_length=100,primary_key=True,unique=True)
    sem_id = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    course_code = models.CharField(max_length=100,blank=True,null=True)
    sem_id = models.CharField(max_length=100,blank=True,null=True)
    file = models.FileField(upload_to="media/files/resources/",blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    size = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    blog_id = models.CharField(max_length=100,primary_key=True,unique=True)
    title = models.TextField(blank=True,null=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    minutecount = models.IntegerField(default=0)
    blog_category = models.CharField(max_length=100,blank=True,null=True)
    banner = models.ImageField(upload_to="media/images/blogs/banners/",blank=True,null=True)
    main_body = models.TextField(blank=True,null=True)
    second_body = models.BooleanField(default=False)
    second_image = models.ImageField(upload_to="media/images/blogs/images",blank=True,null=True)
    second_text = models.TextField(blank=True,null=True)
    third_body = models.BooleanField(default=False)
    third_image = models.ImageField(upload_to="media/images/blogs/images",blank=True,null=True)
    third_text = models.TextField(blank=True,null=True)
    fourth_body = models.BooleanField(default=False)
    fourth_image = models.ImageField(upload_to="media/images/blogs/images",blank=True,null=True)
    fourth_text = models.TextField(blank=True,null=True)
    fifth_body = models.BooleanField(default=False)
    fifth_image = models.ImageField(upload_to="media/images/blogs/images",blank=True,null=True)
    fifth_text = models.TextField(blank=True,null=True)
    sixth_body = models.BooleanField(default=False)
    sixth_image = models.ImageField(upload_to="media/images/blogs/images",blank=True,null=True)
    sixth_text = models.TextField(blank=True,null=True)
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    comment_id = models.CharField(max_length=100,primary_key=True,unique=True)
    blog_id = models.CharField(max_length=100,blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    fullname = models.CharField(max_length=100,blank=True,null=True)
    userimage = models.ImageField(upload_to="media/images/comments/",blank=True,null=True)
    comment_body = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_body
    
class CommentReply(models.Model):
    reply_comment_id = models.CharField(max_length=100,primary_key=True,unique=True)
    comment_id = models.ForeignKey(BlogComment,on_delete=models.CASCADE,related_name="replies")
    username = models.CharField(max_length=100,blank=True,null=True)
    fullname = models.CharField(max_length=100,blank=True,null=True)
    userimage = models.ImageField(upload_to="media/images/comments/",blank=True,null=True)
    reply_comment_body = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply_comment_body

class BookCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    book_id = models.CharField(max_length=100,primary_key=True,unique=True)
    book_category = models.CharField(max_length=100,blank=True,null=True)
    book_image = models.ImageField(upload_to="media/images/books/",blank=True,null=True)
    book_title = models.CharField(max_length=100,blank=True,null=True)
    book_writer = models.CharField(max_length=100,blank=True,null=True)
    book_size = models.FloatField(default=0.0)
    book_file = models.FileField(upload_to="media/files/books/",blank=True,null=True)

    def __str__(self):
        return self.book_title

class Question(models.Model):
    question_id = models.CharField(max_length=100,primary_key=True,unique=True)
    question_title = models.CharField(max_length=200,blank=True,null=True)
    question_description = models.TextField(blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    total_answer = models.IntegerField(default=0)

    def __str__(self):
        return self.question_title
    
class Answer(models.Model):
    answer_id = models.CharField(max_length=100,primary_key=True,unique=True)
    question_id = models.CharField(max_length=100,blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    fullname = models.CharField(max_length=100,blank=True,null=True)
    userimage = models.ImageField(upload_to="media/images/answers/",blank=True,null=True)
    answer_description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username

class AnswerReply(models.Model):
    reply_answer_id = models.CharField(max_length=100,primary_key=True,unique=True)
    answer_id = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name="replies")
    username = models.CharField(max_length=100,blank=True,null=True)
    fullname = models.CharField(max_length=100,blank=True,null=True)
    userimage = models.ImageField(upload_to="media/images/answers/",blank=True,null=True)
    reply_answer_description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username