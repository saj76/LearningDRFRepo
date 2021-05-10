from django.test import TestCase
from registers.tasks import ReportDailyRegisters


# Create your tests here.
class Test(TestCase):
    def test_task(self):
        ReportDailyRegisters().run()