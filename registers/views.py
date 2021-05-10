import datetime

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from registers.models import Shop
from registers.serializers import ShopSerializer
from celery.task import task
from .utils.mail_util import send_email


class ShopsListView(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class GetRegistersCountByDateViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @action(detail=False, methods=["post"])
    def get_registers_by_date(self, request):
        shops_count = self.serializer_class.count()
        email_report.delay(shops_count)
        result = {"shops_count": shops_count}
        return Response(result)

    def get_queryset(self):
        date_str = self.request.data.get('date')
        date_date = datetime.datetime.strptime(date_str, '%y-%m-%d')
        interval_start = datetime.datetime.combine(date_date.date(), datetime.time.min)
        interval_finish = datetime.datetime.combine(date_date.date(), datetime.time.max)
        return Shop.objects.filter(created_at__range=[interval_start, interval_finish])

    def get_serializer_class(self):
        return ShopSerializer(data=self.get_queryset())


@task(name="send_report")
def email_report(registers_count):
    send_email("report", registers_count.__str__(), ["sajjad.vahedi@ronash.co"])
