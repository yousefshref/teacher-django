from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ast import literal_eval

from django.db.models import Q

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework import generics

from . import serializers
from . import models

from datetime import datetime





@api_view(['POST'])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = models.CustomUser.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)



@api_view(['POST'])
def login(request):
    user = get_object_or_404(models.CustomUser, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("Something went wrong", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = serializers.UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})



class levels(generics.ListAPIView):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_level(request):
    if request.user.is_superuser:
      ser = serializers.LevelSerializer(data=request.data)
      if ser.is_valid():
          ser.save()
          return Response(ser.data)
      return Response(ser.errors)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_level(request, pk):
    if request.user.is_superuser:
        ins = models.Level.objects.get(pk=pk)
        ins.delete()
        return Response({"success":True})




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(request):
    user = models.CustomUser.objects.get(pk=request.user.pk)
    ser = serializers.UserSerializer(user)
    return Response(ser.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(requset, pk):
    instance = models.CustomUser.objects.get(id=pk)
    ser = serializers.UserSerializer(instance, data=requset.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def homework_list(request):
    if request.method == 'GET':
        title = request.GET.get('title') 
        homeworks = models.Homework.objects.filter(level=request.user.level).order_by('-id')
        if title:
            homeworks = homeworks.filter(title__icontains=title)
        serializer = serializers.HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def homework_detail(request, pk):
    try:
        homework = models.Homework.objects.get(pk=pk, level=request.user.level)
    except models.Homework.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.HomeworkSerializer(homework)
        return Response(serializer.data)


# admin
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_homework(request):
    q_ids = []
    for i in request.data['questions']:
        q_c = models.Question.objects.create(text=i['title'])
        q_ids.append(q_c.pk)
        for x in i['answers']:
            a_c = models.Answer.objects.create(question=q_c, text=x['title'], is_correct=x['is_correct'])

    lev = models.Level.objects.get(pk=request.data['level'])
    h_create = models.Homework.objects.create(title=request.data['title'], level=lev)
    h_create.questions.set(q_ids)
    return Response({"success":True})


@api_view(['DELETE'])
def delete_homework(request, pk):
  instance = models.Homework.objects.get(id=pk)
  instance.delete()
  return Response({"success":True})



@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_homework(request, homework_id):
    try:
        homework = models.Homework.objects.get(id=homework_id)
    except models.Homework.DoesNotExist:
        return Response({"error": "Homework not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        request.data['student_name'] = request.user.username
        serializer = serializers.HomeworkSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            student_name = serializer.validated_data['student_name']
            answer_ids = request.data['answers']

            # Fetch answers for the given answer_ids
            selected_answers = models.Answer.objects.filter(id__in=answer_ids)

            # Separate correct and incorrect answers
            correct_answers = selected_answers.filter(is_correct=True)
            incorrect_answers = selected_answers.filter(is_correct=False)

            # Create the HomeworkSubmission instance
            submission = models.HomeworkSubmission.objects.create(
                homework=homework,
                student_name=student_name,
            )

            # Add correct and incorrect answers to the corresponding fields
            submission.correct.set(correct_answers)
            submission.false.set(incorrect_answers)

            # Calculate the score based on the number of correct answers
            score = len(correct_answers)
            submission.score = score
            submission.save()

            # Return a more detailed response
            response_data = {
                "message": "Homework submitted and corrected successfully",
                "submission_id": submission.id,
                "submission_time": submission.submission_time,
                "score": score,
                # "corrections": serializer.data["correct"]
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
      try:
        q = models.HomeworkSubmission.objects.get(homework__id=homework_id, student_name=request.user.username)
        ser = serializers.HomeworkSubmissionSerializer(q)
        return Response(ser.data)
      except:
        return Response({"":""})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def submitted_homeworks(request):
    q = models.HomeworkSubmission.objects.filter(student_name=request.user.username)
    ser = serializers.HomeworkSubmissionSerializer(q, many=True)
    return Response(ser.data)



# {
# "homework":1,
# "answers":[
# 2,5
# ]
# }


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def groups(request):
    q = models.Group.objects.filter(level=request.user.level)    

    search_query = request.GET.get('search')

    if search_query:
        # Split the search query into individual words
        search_terms = search_query.split()

        # Initialize a Q object for the intersection of terms
        intersection_q = Q()

        # Iterate over search terms to build the intersection Q object
        for term in search_terms:
            term_q = Q(title__icontains=term) | Q(description__icontains=term)
            intersection_q &= term_q

        # Filter the queryset based on the intersection Q object
        q = q.filter(intersection_q)

    ser = serializers.GroupSerializer(q, many=True)
    return Response(ser.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def group(request, pk):
    q = models.Group.objects.get(level=request.user.level, pk=pk)    
    ser = serializers.GroupSerializer(q)
    return Response(ser.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def lesson(request, pk):
    q = models.Lesson.objects.get(group__level=request.user.level, pk=pk)    
    ser = serializers.LessonSerializer(q)
    return Response(ser.data)



# admin
@api_view(['POST'])
def create_group(request):
    lessons = request.data['lesson_group']
    ser = serializers.GroupSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        for i in literal_eval(lessons):
            gr = models.Group.objects.get(pk=ser.data['id'])
            models.Lesson.objects.create(
                group=gr,
                title=i['title'],
                description=i['description'],
                video=i['video'],
                tags=i['tags']
            ).save()
        return Response(ser.data)
    return Response(ser.errors)

@api_view(['DELETE'])
def delete_group(request, pk):
  instance = models.Group.objects.get(id=pk)
  instance.delete()
  return Response({"success":True})
    

@api_view(['POST'])
def create_new_lesson(request):
    ser = serializers.LessonSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)
  
@api_view(['DELETE'])
def delete_lesson(request, pk):
  instance = models.Lesson.objects.get(id=pk)
  instance.delete()
  return Response({"success":True})
    






@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def plans(request):
    q = models.Plan.objects.filter(level=request.user.level, date=datetime.today().strftime('%Y-%m-%d'))

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from and date_to:
      q = models.Plan.objects.filter(level=request.user.level, date__range=[date_from, date_to])

    ser = serializers.PlanSerializer(q, many=True)
    return Response(ser.data)

# admin
@api_view(['POST'])
def create_plan(request):
    ser = serializers.PlanSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        insta = models.Plan.objects.get(id=ser.data['id'])
        insta.save()
        return Response(ser.data)
    return Response(ser.errors)

@api_view(['DELETE'])
def delete_plan(request, pk):
    ins = models.Plan.objects.get(pk=pk)
    ins.delete()
    return Response({"success":True})

  

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def group_messages(request):
    q = models.GroupMessages.objects.filter(level=request.user.level)
    ser = serializers.GroupMessagesSerializer(q, many=True)
    return Response(ser.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def one_group_messages(request, pk):
    q = models.GroupMessages.objects.get(pk=pk, level=request.user.level)
    ser = serializers.GroupMessagesSerializer(q)
    return Response(ser.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_group_message(request, pk): 
    ser = serializers.CommunicateSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)

# admin
@api_view(['POST'])
def create_group_messages(request):
    ser = serializers.GroupMessagesSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)

@api_view(['DELETE'])
def delete_group_messages(request, pk):
    ins = models.GroupMessages.objects.get(pk=pk)
    ins.delete()
    return Response({"success":True})






@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class SavedListView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        try:
            # Check if Saved object exists for the user
            saved_instance, created = models.Saved.objects.get_or_create(user=user)

            # If SavedList data is provided in the request, update or create SavedList instances
            saved_list_data = request.data.get('saved_list', [])

            for saved_list_item in saved_list_data:
                lesson_id = saved_list_item.get('lesson')
                
                # Check if Lesson with the provided ID exists
                try:
                    lesson = models.Lesson.objects.get(pk=lesson_id)
                except models.Lesson.DoesNotExist:
                    return Response({'error': f'Lesson with ID {lesson_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Check if SavedList with the provided lesson_id already exists for the user
                saved_list_instance, created = models.SavedList.objects.get_or_create(saved=saved_instance, lesson_id=lesson_id)
                
                # If not created, it means it already exists, so ignore it
                if not created:
                    continue

            # Serialize the Saved object and return the response
            serializer = serializers.SavedSerializer(saved_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_saved_list(request):
    q = models.Saved.objects.filter(user=request.user)
    ser = serializers.SavedSerializer(q, many=True)
    return Response(ser.data)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_list(request, list_pk):
    instance = models.SavedList.objects.get(saved__user=request.user, pk=list_pk)
    instance.delete()
    return Response({"success":True})



# admin
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_students(request):
    if request.user.is_superuser:
        username = request.GET.get('username')
        q = models.CustomUser.objects.all()
        if username:
            q = q.filter(username__icontains=username)
        ser = serializers.UserSerializer(q, many=True)
        return Response(ser.data)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student(request, student_id):
    q = models.CustomUser.objects.get(id=student_id)
    ser = serializers.UserSerializer(q)
    return Response(ser.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student_homeworks(request, student_id):
    username = models.CustomUser.objects.get(id=student_id).username
    q = models.HomeworkSubmission.objects.filter(student_name=username)
    ser = serializers.HomeworkSubmissionSerializer(q, many=True)
    return Response(ser.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student_homework_answers(request, student_id, homework_id):
    username = models.CustomUser.objects.get(id=student_id).username
    homework = models.Homework.objects.get(id=homework_id)
    q = models.HomeworkSubmission.objects.get(student_name=username, homework=homework)
    ser = serializers.HomeworkSubmissionSerializer(q)
    return Response(ser.data)





@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student_saved_list(request, student_id):
  try:
    saved = models.Saved.objects.get(user__id=student_id)
    ser = serializers.SavedSerializer(saved)
    return Response(ser.data)
  except:
      return Response({"Not Found":"No Saved List with this user"})



