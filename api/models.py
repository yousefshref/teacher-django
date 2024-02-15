from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class Level(models.Model):
    title = models.CharField(max_length=155)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    pp = models.ImageField(upload_to='images/profile-pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username



class Question(models.Model):
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', null=True)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class Homework(models.Model):
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return str(self.pk)



class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    submission_time = models.DateTimeField(auto_now_add=True)
    # answers = models.ManyToManyField(Answer, related_name='submissions')
    correct = models.ManyToManyField(Answer, related_name='corrections', blank=True, null=True)
    false = models.ManyToManyField(Answer, related_name='false', blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)




class Group(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/groups/', null=True)
    date = models.DateField(auto_now_add=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson_group')
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.URLField(null=True)
    tags = models.CharField(max_length=255)


# {
# "title":"test",
# "description":"sssstse",
# "level":1,
# "lesson_group":[
# {
# "title":"ss",
# "description":"sssstse",
# "tags":"test",
# "video":"http://www.google.com/"
# }
# ]
# }

    

class Plan(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)





class GroupMessages(models.Model):
    title = models.CharField(max_length=155)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Communicate(models.Model):
    group = models.ForeignKey(GroupMessages, on_delete=models.CASCADE, related_name='group_communicate')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)







class Saved(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class SavedList(models.Model):
    saved = models.ForeignKey(Saved, on_delete=models.CASCADE, related_name='saved_list_details')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_details')





