from django.http.response import HttpResponseRedirect

# MIXINS

class SetSiteFromRequestFormValidMixin:
    
    def form_valid(self, form):
        assert self.request.site is not None, (
            'Please enable a MIDDLEWARE that attaches'
            'the current site the request.' %
            (self.__class__.__name__, )
        )
        self.object = form.save(commit=False)
        self.object.site = self.request.site
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PassRequestToFormKwargsMixin:
    
    def get_form_kwargs(self):
        assert self.request.site is not None, (
            'Please enable a MIDDLEWARE that attaches'
            'the current site the request.' %
            (self.__class__.__name__, )
        )
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class SiteQuerysetMixin:
    model_to_query = None

    def get_queryset(self):
        assert self.model_to_query is not None, (
            'Expected view %s should contain model_to_query '
            'to get filter by site.' %
            (self.__class__.__name__, )
        )
        return self.model_to_query.objects.from_site(self.request.site)