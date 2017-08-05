import scrapy

class Sakabot(scrapy.Spider):

	name = 'Sakabot'
	start_urls = ['https://blogdosakamoto.blogosfera.uol.com.br/']

	def parse(self, response):
		POST_SELECTOR = '#conteudo-principal .post.news'

		for article in response.css(POST_SELECTOR):
			TITLE_SELECTOR = 'a ::text'
			URL_SELECTOR = 'a ::attr(href)'
			yield {
				'title': article.css(TITLE_SELECTOR).extract_first(),
				'url': article.css(URL_SELECTOR).extract_first(),
			}

		PREVIOUS_SELECTOR = '.blog-navigation .previous-post ::attr(href)'
		previous_page = response.css(PREVIOUS_SELECTOR).extract_first()
		if previous_page:
			previous_page = previous_page[previous_page.find('http'):]
			yield scrapy.Request(
                response.urljoin(previous_page),
                callback=self.parse
            )
