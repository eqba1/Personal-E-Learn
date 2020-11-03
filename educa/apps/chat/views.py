from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

@login_required
def course_chat_room(request, course_id):
    
    try:
        course = request.user.courses_joined.get(id=course_id)
    except:
        return HttpResponseForbidden()

    t = loader.get_template('chat/room.html')
    c = {'course': course}
    return HttpResponse(t.render(c, request))


