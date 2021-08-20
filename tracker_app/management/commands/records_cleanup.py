import concurrent.futures
from django.core.management.base import BaseCommand
from tracker_app.models import Item
from tracker_app.models import Record


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('records_cleanup...')
        before = len(Record.objects.all())
        self.cleanup_all()
        after = len(Record.objects.all())
        print('cleaned up {n} records'.format(n = before - after))

    def cleanup_all(self):
        try:
            all_items = Item.objects.all()
            if len(all_items) > 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.map(self.cleanup_each, all_items)
            else:
                print('nothing to cleanup')
        except Exception as e: 
            print(str(e))


    def cleanup_each(self, item):
        all_records = Record.objects.filter(item=item)
        record_ids_to_keep = map(lambda x: x.id, Record.get_significant_records(item))
        Record.objects.filter(item=item).exclude(id__in=record_ids_to_keep).delete()
