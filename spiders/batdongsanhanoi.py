import scrapy

class BatdongsanHanoi(scrapy.Spider):
    name = 'batdongsanhanoi'
    allowed_domains = ['bdshanoi.com.vn/']
    start_urls = ['https://bdshanoi.com.vn/properties/0/0/0']
    
    
    def parse(self, response):
        products = response.css('ul.ulpro > li')
        for bds in products:
            items = {
                'name' : bds.css('a > h4::text').get(),
                'price' : bds.css('span::text').get(),
                'location' : bds.css('div.ileft::text').get(),
                'floor_area' : bds.css('div.iright::text').get(),
                'link' : bds.css('a::attr(href)').get()
            }
            yield items
        
        current_page_link = response.css('div#mainlink a.active + a::attr(href)').get()
        
        if current_page_link:
            # Extract the current page number from the href attribute
            current_page_number = int(current_page_link.split('/')[-1])

            # Calculate the next page number
            next_page_number = current_page_number + 1

            # Construct the selector for the next page link
            next_page_selector = f'div#mainlink a[href$="/{next_page_number}"]::attr(href)'

            # Get the URL of the next page
            next_page_url = response.css(next_page_selector).get()

            if next_page_url:
                # Follow the next page link
                yield response.follow(next_page_url, callback=self.parse)
