from django.contrib import admin
from . import models


admin.site.register(models.Level)

admin.site.register(models.CustomUser)


admin.site.register(models.Homework)
admin.site.register(models.Question)
admin.site.register(models.Answer)


admin.site.register(models.HomeworkSubmission)


admin.site.register(models.Group)
admin.site.register(models.Lesson)


admin.site.register(models.Plan)


admin.site.register(models.GroupMessages)
admin.site.register(models.Communicate)


admin.site.register(models.Saved)
admin.site.register(models.SavedList)

