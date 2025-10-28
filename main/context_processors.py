from .models import Module

def module_context(request):
    course_slug = request.resolver_match.kwargs.get('course_slug')  # Get course_slug from URL
    modules = Module.objects.filter(course__slug=course_slug)
    return {
        'modules': modules,
        'course_slug':course_slug
    }