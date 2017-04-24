import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule, XMLFeedSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector	import Selector
from scrapy.http	import Request
from scrapy.http	import HtmlResponse
from scrapy.http	import XmlResponse
from scrapy.http	import TextResponse
from crawl.items	import CrawlItem

class BlogSpider(CrawlSpider):
	name = 'cocktail'
	allowed_domains = ['www.destinationcocktails.fr']
	start_urls = ['http://www.destinationcocktails.fr']

	# parcour toutes les pages du site
	rules = (
		Rule(SgmlLinkExtractor(allow=('')), callback='parse_items',follow= True),
	)

	def parse_items(self, response):
		if isinstance(response, (XmlResponse, HtmlResponse)):
			sel = Selector(response)
			item = CrawlItem()

			nom = sel.xpath(".//div[@id='fiche_recette_r']//h1//text()").re(r'Cocktail\s:\s*(.*)')
			quantitee = sel.xpath(".//div[@id='fiche_recette_r']//div[@id='ingred']//ul//li//text()").extract()
			preparation = sel.xpath(".//div[@id='fiche_recette_r']//div[@id='recette']//p//text()").extract()



			# Si les items ne sont pas vides
			if nom and quantitee and preparation:

				# Nom de la recette
				item['nom'] = nom
				#item['nom'] = [",".join(nom)] #[w.replace('Cocktail : ', '') for w in nom]
				# Quantitee des ingredients de la recette
				item['quantitee'] = [w.replace(u'\xa0', u' ') for w in quantitee]
				# La preparation
				item['preparation'] = [w.replace(u'\xa0', u' ') for w in preparation]

				yield item
