# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import firebase_admin
from firebase_admin import credentials, firestore

class Uk49ScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # draws --> remove created key
        draws = ['lunch_draw', 'tea_draw']
        for draw in draws:
            draw_list = adapter.get(draw)
            count = 0
            for num_dict in draw_list:
                del num_dict["created_at"]
                adapter[draw][count] = num_dict
                count +=1

        return item

class SaveToFirebasePipeline:
    def __init__(self):
        # Firebase --> initialization
        self.cred = credentials.Certificate("./ned-app-key.json")
        firebase_admin.initialize_app(self.cred)
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Months from July to December
        months = {10: 'oct', 11: 'nov', 12: 'dec'}

        # connect firestore
        db = firestore.client()

        # Firestore - create collection and store data
        draw_date = adapter.get('date')
        dd_list = draw_date.split('-')      # ['YYYY', 'MM', 'DD']
        print(f'========>>   {dd_list}')

        # Firebase --> collection references
        month_ref = db.collection(f'results-{months[int(dd_list[1])]}')

        # Firebase --> create a new document
        month_ref.document(draw_date).set(item)

        return item



