from rest_framework.serializers import ModelSerializer

from core.models import ServiceMan, Order


class ServicemanModelSerializer(ModelSerializer):
    class Meta:
        model = ServiceMan
        fields = "__all__"


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "serviceman_description",
            "customer_description",
            "deliveryman_description",
            "comment",
            "amount_due_by",
            "created",
        ]
