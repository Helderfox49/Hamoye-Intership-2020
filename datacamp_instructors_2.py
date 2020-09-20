import scrapy
import urllib.request
from  csv import writer

from os import getcwd, path, mkdir

# Import the CrawlerProcess: for running the spider
from scrapy.crawler import CrawlerProcess

def img_downloader(image_url, filename):
    current_dir = getcwd()
    instructors_dir = path.join(current_dir, 'instructors_images')
    img_name = str(filename)

    if not path.exists(instructors_dir):
        mkdir(path.join(instructors_dir))
    urllib.request.urlretrieve(image_url, path.join(instructors_dir, img_name))


class DC_instructor_spider(scrapy.Spider):
    name = "datacamp_instructor"
    start_urls = ['https://www.datacamp.com/instructors?all=true']
    output = 'instructors_datacamp.csv'

    # def start_requests(self):
    #     urls = ['https://www.datacamp.com/instructors?all=true']
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse_front)
    
    def parse(self, response):
        instructor_links = response.css('div.instructor-block__description a.instructor-block__link::attr(href)')
        link_to_follow = instructor_links.extract()
        for url in link_to_follow:
            yield scrapy.Request(url="https://www.datacamp.com" + url, callback=self.parse_front)

    def parse_front(self, response):
        instructor_div = response.css('div.css-fe452h')
        
        name = instructor_div.css('h1::text').extract_first().strip()
        role = instructor_div.css('h2::text').extract_first().strip()
        bio = instructor_div.css('p::text').extract_first().strip()
        img_url = instructor_div.css('img::attr(src)').extract_first().strip()

        with open(self.output, 'a', newline="") as fhand:
            writer_csv = writer(fhand)
            writer_csv.writerow([name, role, bio])
            yield {'Name': name, 'role': role, 'bio':bio, 'img_url': img_url}

        img_downloader(img_url, name)

