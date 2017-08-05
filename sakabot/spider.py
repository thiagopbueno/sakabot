import scrapy
import json

class Sakabot(scrapy.Spider):

	name = 'Sakabot'
	start_urls = ['https://blogdosakamoto.blogosfera.uol.com.br/']
	posts_links = []

	def parse(self, response):
		POST_SELECTOR = '#conteudo-principal .post.news'

		for article in response.css(POST_SELECTOR):
			TITLE_SELECTOR = 'a ::text'
			URL_SELECTOR = 'a ::attr(href)'
			post =  {
				'title': article.css(TITLE_SELECTOR).extract_first(),
				'url': article.css(URL_SELECTOR).extract_first(),
			}
			Sakabot.posts_links.append(post)
			yield post

		self._dump_posts()

		PREVIOUS_SELECTOR = '.blog-navigation .previous-post ::attr(href)'
		previous_page = response.css(PREVIOUS_SELECTOR).extract_first()
		if previous_page:
			previous_page = previous_page[previous_page.find('http'):]
			yield scrapy.Request(
                response.urljoin(previous_page),
                callback=self.parse
            )

	def _dump_posts(self):
		with open('posts.json', 'w') as outfile:
			json.dump(Sakabot.posts_links, outfile, sort_keys=True, indent=4)
