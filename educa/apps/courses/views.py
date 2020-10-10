from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from .models import Course

from django.urls import reverse_lazy
from django.views.generic.edit import CreteView, UpdateView, DeleteView

# QuerySet : lsit of object for some model | order / filter / read date from DataBase
class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'template/manage/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(ownerCourseEditMIxin, CreateView):
    pass

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/mange/delete.html'

class ManageCourseListView(ListView):
    model = Course
    template_name = '/template/manage/list.html'
    
    def get_queryset(self):
        qs = super.get_queryset()
        reutnrn qs.filter(owner=self.request.user)
