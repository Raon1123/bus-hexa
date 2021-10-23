from django.core.management.base import BaseCommand, CommandError

from chroniccrawler.crawler.dayinfo import do_dayinfo
from chroniccrawler.crawler.laneinfo import do_laneinfo
from chroniccrawler.crawler.timetable_usb import do_timetable
from chroniccrawler.crawler.buspos import do_buspos
from chroniccrawler.crawler.arrivalinfo import do_arrivalinfo

from chroniccrawler.models import DayInfo

class Command(BaseCommand):
    help = "Execute request-and-store-on-database tasks.\nPlease pass only one argument per execution."

    def add_arguments(self, parser):
        parser.add_argument('--daily', action='store_true', help='Do daily tasks(date, lane, timetable)')
        parser.add_argument('--timed', action='store_true', help='Do timed tasks(position, arrival)')
        parser.add_argument('--arrival', action='store_true', help='test : do arrival related tasks')
        parser.add_argument('--position', action='store_true', help='test : do bus position related tasks')
        parser.add_argument('--date', action='store_true', help='test : do date related tasks')
        parser.add_argument('--lane', action='store_true', help='test : do lane related tasks')
        parser.add_argument('--timetable', action='store_true', help='test : do timetable related tasks')

    def handle(self, *args, **options):
        if options['daily']:
            do_dayinfo()
            do_laneinfo()
            dayinfo = DayInfo.objects.first()
            do_timetable(dayinfo.kind)
        elif options['timed']:
            pass
        elif options['date']:
            do_dayinfo()
        elif options['lane']:
            do_laneinfo()
        elif options['timetable']:
            dayinfo = DayInfo.objects.first()
            do_timetable(dayinfo.kind)
        elif options['position']:
            do_buspos()
        elif options['arrival']:
            do_arrivalinfo()
