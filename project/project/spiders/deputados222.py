import scrapy


class DeputadosSpider(scrapy.Spider):
	name = 'deputados'
	allowed_domains = ['camara.leg.br']
	start_urls = ['https://www.camara.leg.br/deputados/']

	def start_requests(self):
		# opening the file in read mode
		my_file = open("lista_deputados_string_list.txt", "r")
		# reading the file
		urls = my_file.read()

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		pass
