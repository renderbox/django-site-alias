from django.http import HttpResponse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import SiteAlias
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

def my_view(request):
    return HttpResponse(b'Test Response')

class SiteAliasListView(generic.ListView):
    model = SiteAlias

class SiteAliasCreateView(SuccessMessageMixin, generic.CreateView):
    model = SiteAlias
    fields = ('site', 'domain',)
    success_message = _('Alias Created Successfully')
    success_url = reverse_lazy('alias-list')

class SiteAliasUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = SiteAlias
    fields = ('site', 'domain',)
    success_message = _('Alias Updated Successfully')
    success_url = reverse_lazy('alias-list')



class SiteAliasDeleteView(generic.DeleteView):
    model = SiteAlias
    success_url = reverse_lazy('alias-list')
    success_message = _('Alias Deleted Successfully')

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response