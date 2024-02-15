from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.CustomUser
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Level
        fields = '__all__'



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Homework
        fields = '__all__'

# {
#   "title": "Your Homework Title",
#   "level": 1,
#   "questions": [
#     {
#       "text": "Question 1",
#       "answers": [
#         {"text": "Answer 1", "is_correct": true},
#         {"text": "Answer 2", "is_correct": false}
#       ]
#     },
#     {
#       "text": "Question 2",
#       "answers": [
#         {"text": "Answer 3", "is_correct": true},
#         {"text": "Answer 4", "is_correct": false}
#       ]
#     }
#   ]
# }





class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    correct = AnswerSerializer(many=True, read_only=True)
    false = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = models.HomeworkSubmission
        fields = '__all__'




class LessonSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Lesson
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    lesson_group = LessonSerializer(read_only=True, many=True)
    class Meta():
        model = models.Group
        fields = '__all__'





class PlanSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Plan
        fields = '__all__'





class CommunicateSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(read_only=True, source='user')
    class Meta():
        model = models.Communicate
        fields = '__all__'

class GroupMessagesSerializer(serializers.ModelSerializer):
    group_communicate = CommunicateSerializer(read_only=True, many=True)
    class Meta():
        model = models.GroupMessages
        fields = '__all__'




class SavedListSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    class Meta():
        model = models.SavedList
        fields = '__all__'

class SavedSerializer(serializers.ModelSerializer):
    saved_list = SavedListSerializer(many=True, read_only=True)
    saved_list_details = SavedListSerializer(many=True, read_only=True)
    class Meta():
        model = models.Saved
        fields = '__all__'




