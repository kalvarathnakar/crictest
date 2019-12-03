from django.shortcuts import render
from accounts.common_func import format_serializer_errors,CustomAPIResponse
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from django.views.generic import TemplateView
from accounts.serializer import *
from django.shortcuts import render_to_response, render, redirect, HttpResponseRedirect, Http404, HttpResponse
# Create your views here.

class GetStudentDetailsViewSet(APIView):
    def get(self,request):
        student_details_obj_list = StudentEnroll.objects.all()
        kwargs = {}
        student_list=[]
        try:

            for each in student_details_obj_list:
                student_kwargs={
                "username":each.student.user.username,
                "id":each.student.user.id,
                "student_name":each.student.name,
                }
                student_kwargs['teacher']=[]

                teacher_id_list = each.teacher.all().values_list('id',flat=True)
                teacher_obj_list = Teacher.objects.filter(id__in=teacher_id_list)
                teacher_list =[]
                if len(teacher_obj_list)>0:
                    for each_teacher in teacher_obj_list:
                        teacher_kwargs = {
                        "id":each_teacher.user.id,
                        "name":each_teacher.name,
                        "subject":each_teacher.subject.values_list('name',flat=True)
                        }
                        teacher_list.append(teacher_kwargs)
                    student_kwargs['teacher'].extend(teacher_list)
                student_list.append(student_kwargs)
            context_data = {"success":True,"data":{"student_list":student_list}}
            
        except Exception as e:
            context_data = {"success":False,"data":{"errors":str(e)}}
        return Response(CustomAPIResponse(**context_data).response)


            



    def post(self,request):
        pass


class GetStudentReportViewSet(TemplateView):
    template_name = 'student_list.html'
    def get(self,request):
        student_obj_list = StudentEnroll.objects.all()
        variables ={
        "title":"Student List",
        "studen_list":student_obj_list
        }
        return render(request,self.template_name, variables)
class UpdateSubjectDetailsViewSet(APIView):
    def get(self,requesttr,teacher_id=None):
        if teacher_id is not None:
            try:
                teacher_obj = Teacher.objects.get(id=teacher_id)
                kwargs = {
                "name":teacher_obj.name,
                "id":teacher_obj.id,
                "subjects":teacher_obj.subject.values('id','name')
                }
                context_data = {"success":True,"data":{"teacher_details":kwargs}}
            except Exception as e:
                context_data = {"success":False,"data":{"errors":str(e)}}
        else:
            context_data = {"success":False,"data":{"message":"Please check teacher_id"}}
        return Response(CustomAPIResponse(**context_data).response)                


    def post(self,request,teacher_id=None):
        if teacher_id is not None:
            serializer = UpdateSubjectDetailsSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    teacher_obj = Teacher.objects.get(id=teacher_id)
                    teacher_obj.subject.clear()
                    subject_obj_list=Subject.objects.filter(id__in=request.data['subject_id_list'])
                    for each in subject_obj_list:
                        teacher_obj.subject.add(each)
                    context_data = {"success":False,"data":{"message":"subjects successfully updated"}}
                except Exception as e:
                    context_data = {"success":False,"data":{"errors":str(e)}}
            else:
                errors_list =  format_serializer_errors(**serializer.errors)
                context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" : errors_list}}
        else:
            context_data = {"success":False,"data":{"message":"Please check teacher_id"}}
        return Response(CustomAPIResponse(**context_data).response)