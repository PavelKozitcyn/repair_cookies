import requests
import json
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from django.views.generic import UpdateView, ListView

from core.models import ServiceMan, Order
from core.serializers import ServicemanModelSerializer, OrderModelSerializer
from permissions import ServicemanPermissions, OrderPermissions
from core.services.order_service import update_outer_order


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = (
        OrderPermissions,
    )


class ServicemanViewSet(ModelViewSet):
    queryset = ServiceMan.objects.all()
    serializer_class = ServicemanModelSerializer
    permission_classes = (
        ServicemanPermissions,
    )


class IndexView(ListView):
    model = Order
    template_name = 'index.html'
    context_object_name = "orders"
    fields = ['serviceman']

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['servicemans'] = ServiceMan.objects.all()
        return context


class OrderDetail(UpdateView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'
    fields = ['serviceman', 'serviceman_description', 'status', 'amount_due_by']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        exceptions = []
        data = dict(request.POST)
        pk = self.object.id
        payload = {
            'serviceman': data.get('serviceman')[0],
            'serviceman_description': data.get('serviceman_description')[0],
            'status': data.get('status')[0],
            'amount_due_by': data.get('amount_due_by')[0],
        }

        try:
            service_update = f"{settings.CLIENT_SERVICE}/api/orders/{pk}/"
            update_outer_order(service_update, payload)
        except Exception as exc:
            exceptions.append(exc)

        try:
            service_update = f"{settings.DELIVERY_SERVICE}/api/orders/{pk}/"
            update_outer_order(service_update, payload)
        except Exception as exc:
            exceptions.append(exc)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
