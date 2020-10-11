from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from .models import Course

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet

from django.forms.models import modelform_factory
from django.apps import apps 
from .models import Module, Content

class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        return redirect('module_content_list', module.id)

##
#This is the first part of ContentCreateUpdateView . It will allow you to create
#and update different models' contents
##
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None 
    model = None 
    obj = None 
    template_name = 'manage/content/form.html'

    def get_model(self,model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                'order',
                                                'created',
                                                'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)

        if id:
            self.obj = get_object_or_404(self.model,
                                        id=id,
                                        owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):

        form = self.get_form(self.model,
                            instance=self.obj,
                            data=request.POST,
                            files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
        if not id:
            # new content
            Content.objects.create(module=self.module,
                                item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})

##
# The CourseModuleUpdateView view handles the formset to add, update, and
# delete modules for a specific course.
##
class CourseModuleUpdateView(TemplateResponseMixin,View):
    template_name = 'manage/formset.html'
    course = None 

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)
    
    def get(self, reuqest, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'coures': self.course,
                                        'formset': formset})

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
    template_name = 'manage/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'manage/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.view_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.view_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'manage/delete.html'
    permission_required = 'courses.view_course'

class OwnerCourseMixin(OwnerMixin, 
                        LoginRequiredMixin, 
                        PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug' , 'overview' ]
    success_url = reverse_lazy('manage_course_list')

class ManageCourseListView(ListView):
    model = Course
    template_name = 'manage/list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
