import os
import json
import scrapy
from datetime import datetime


class GreensSpider(scrapy.Spider):
    name = "greens"
    start_urls = [
        "https://www.thegreenscentennial.com/",
    ]

    def __init__(self, *args, **kwargs):
        super(GreensSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = {
            "date": datetime.now().date(),
            "info": []
        }
        
        for greens in response.css("div.floorplan-block"):

            room_type = greens.xpath("div/div/div/div/h2/text()").get()

            rent_value = greens.xpath("@data-rent").get()
            if rent_value:
                rent_value = float(rent_value)

            data["info"].append({
                "type": room_type,
                "price": rent_value
            })

        self.write_to_file(data)

    def write_to_file(self, data):
        # Convert the date to a string in the desired format
        data["date"] = data["date"].isoformat()

        # Determine the root directory of your project
        root_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to "greens.jsonl" in the root directory
        file_path = os.path.join(root_directory, "greens.jsonl")

        # Write data to "greens.jsonl" file in the root directory
        # with open(file_path, "a") as f:
        #     json.dump(data, f)
        #     f.write("\n")

        json_data = json.dumps(data)
        print(json_data)