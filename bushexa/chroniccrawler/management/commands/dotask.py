from django.core.management.base import BaseCommand, CommandError

from chroniccrawler.crawler.dayinfo import do_dayinfo
from chroniccrawler.crawler.laneinfo import do_laneinfo
from chroniccrawler.crawler.timetable_usb import do_timetable
from chroniccrawler.crawler.buspos import do_buspos
from chroniccrawler.crawler.arrivalinfo import do_arrivalinfo

class Command(BaseCommand):
    help = "Execute request-and-store-on-database tasks"

    def add_arguments(self, parser):
        parser.add_argument('--arrival', action='store_true', help='do arrival related tasks')
        parser.add_argument('--position', action='store_true', help='do bus position related tasks')
        parser.add_argument('--date', action='store_true', help='do date related tasks')
        parser.add_argument('--lane', action='store_true', help='do lane related tasks')
        parser.add_argument('--timetable', action='store_true', help='do timetable related tasks')

    def handle(self, *args, **options):
        if options['date']:
            do_dayinfo()

        if options['lane']:
            do_laneinfo()

        if options['timetable']:
            do_timetable()

        if options['position']:
            do_buspos()

        if options['arrival']:
            do_arrivalinfo()
