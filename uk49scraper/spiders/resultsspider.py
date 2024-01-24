import scrapy
import json
from uk49scraper.items import ResultsItem


class ResultsspiderSpider(scrapy.Spider):
    name = "resultsspider"
    start_urls = ["https://www.49s.co.uk/49s/results"]

    # Months from July to December
    months = {10: 31, 11: 30, 12: 31}

    def parse(self, response):
        # Loop for 30 times:

        for month, days in self.months.items():
            for day in range(1, days+1):
                if month != 1:
                    # There was no draws on the 25 of December 
                    if day == 25 and month == 12:
                        continue
                    else:
                        url = f"https://49s-api.production.sis.onpacegroup.com/numbers/49/events/2023-{month}-{day}"
                else:
                    url = f"https://49s-api.production.sis.onpacegroup.com/numbers/49/events/2024-{month}-{day}"

                yield scrapy.Request(url, callback=self.parse_api)


    # TODO - Data Extraction
    # ----------------------
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
