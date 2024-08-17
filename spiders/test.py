import scrapy

class HousesSpider(scrapy.Spider):
    name = 'batdongsanhanoi'
    allowed_domains = ['bdshanoi.com.vn']
    start_urls = ['https://bdshanoi.com.vn/properties/0/0/0/0']

    def parse(self, response):
        self.logger.info('Parsing page: %s', response.url)

        # Extract product information
        products = response.css('ul.ulpro > li')
        for bds in products:
            item = {
                'name': bds.css('a > h4::text').get(),
                'price': bds.css('span::text').get(),
                'location': bds.css('div.ileft::text').get(),
                'floor_area': bds.css('div.iright::text').get(),
                'link': response.urljoin(bds.css('a::attr(href)').get())
            }
            self.logger.info('Extracted item: %s', item)
            yield item

        # Extract and follow pagination links
        pagination_links = response.css('div#mainlink a::attr(href)').getall()
        self.logger.info('Found pagination links: %s', pagination_links)

        # Ensure we are visiting each page
        for link in pagination_links:
            next_page_url = response.urljoin(link)
            self.logger.info('Following pagination link to: %s', next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        self.logger.info('Parsing pagination page: %s', response.url)
        
        products = response.css('ul.ulpro > li')
        for bds in products:
            item = {
                'name': bds.css('a > h4::text').get(),
                'price': bds.css('span::text').get(),
                'location': bds.css('div.ileft::text').get(),
                'floor_area': bds.css('div.iright::text').get(),
                'link': response.urljoin(bds.css('a::attr(href)').get())
            }
            self.logger.info('Extracted item: %s', item)
            yield item

        # Check for more pagination links
        pagination_links = response.css('div#mainlink a::attr(href)').getall()
        self.logger.info('Found additional pagination links: %s', pagination_links)

        # Follow the next page links if they exist
        for link in pagination_links:
            next_page_url = response.urljoin(link)
            self.logger.info('Following additional pagination link to: %s', next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_pagination)

