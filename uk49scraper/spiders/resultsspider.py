import scrapy
import json
from uk49scraper.items import ResultsItem


class ResultsspiderSpider(scrapy.Spider):
    name = "resultsspider"
    start_urls = ["https://www.49s.co.uk/49s/results"]

    def parse(self, response):
        # Data Range --> the months want to scrape
        months = {10: 31, 11: 30, 12: 31}

        for month, days in months.items():
            for day in range(1, days+1):
                if day == 25 and month == 12:
                    # Skip --> there was no draws on the 25 of Dec 
                    continue
                else:
                    url = f"https://49s-api.production.sis.onpacegroup.com/numbers/49/events/2023-{month}-{day}"

                yield scrapy.Request(url, callback=self.parse_api)


    # Data Extraction --> get draw results and dates 
    def parse_api(self, response):
        # Response --> store the data that was returned
        raw_data = response.body
        unsorted_data = json.loads(raw_data)
        
        # Item Object --> create an instance of ResultItem object  
        results = ResultsItem()

        # Data Extraction --> get required data from scraped data
        results["date"] = unsorted_data["events"][0]["game"]["date"]
        results["lunch_draw"] = unsorted_data["events"][1]["drawns"]
        results["tea_draw"] = unsorted_data["events"][0]["drawns"]

        yield results
