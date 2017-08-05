import scrapy
import json

BLOG_URL = 'https://blogdosakamoto.blogosfera.uol.com.br/'

class Sakabot(scrapy.Spider):

    name = 'Sakabot'
    start_urls = [BLOG_URL]
    posts_links = []

    def parse(self, response):
        yield from self._parse_post_list(response)
        yield from self._parse_previous_page(response)
        self._dump_posts()

    def _parse_post_list(self, response):
        POSTS_SELECTOR = '#conteudo-principal .post.news'
        for post_link in response.css(POSTS_SELECTOR):
            yield from self._parse_post_link(post_link)

    def _parse_post_link(self, post_link):
        TITLE_SELECTOR = 'a ::text'
        URL_SELECTOR = 'a ::attr(href)'
        post =  {
            'title': post_link.css(TITLE_SELECTOR).extract_first(),
            'url': post_link.css(URL_SELECTOR).extract_first(),
        }
        Sakabot.posts_links.append(post)
        yield scrapy.Request(post['url'], callback=self._parse_post)

    def _parse_post(self, response):
        TEXT_SELECTOR = '#texto p::text'
        content = response.css(TEXT_SELECTOR).extract()
        self._dump_post(response.url, '\n'.join(map(str, content)))

    def _parse_previous_page(self, response):
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

    def _dump_post(self, post_url, content):
        filename = post_url[:-1].replace(BLOG_URL, '').replace('/', '-') + '.txt'
        with open('data/' + filename, 'w') as outfile:
            outfile.write(content)

