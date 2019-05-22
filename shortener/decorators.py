from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


def user_is_instance_owner(view_method):
    def wrap(request, *args, **kwargs):
        Link = apps.get_model('shortener', 'link')
        Klass = apps.get_model('shortener', request.path.split('/')[2])
        instance = get_object_or_404(Klass, pk=kwargs['id'])
        instance_owner = instance.short_url.user if Klass is Link else instance.user
        if request.user == instance_owner:
            return view_method(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
