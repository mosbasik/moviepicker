# django imports
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# local imports
from main.views import timezone


class Timezone(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # if user's timezone cookie was not included in their request
        if 'timezone' not in request.COOKIES:
            # and if the view being called was not timezone (to avoid loops)
            if view_func is not timezone:
                return redirect('{}?next={}'.format(reverse('timezone'), request.path))
        return None
