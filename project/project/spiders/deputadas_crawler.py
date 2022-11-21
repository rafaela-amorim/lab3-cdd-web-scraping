import scrapy


class DeputadasSpider(scrapy.Spider):
	name = 'deputadas_crawler'
	allowed_domains = ['camara.leg.br']
	
	def start_requests(self):
		with open("./deputades/lista_deputadas.txt") as file_links:
			links = file_links.readlines()
			links = list(map(lambda x: x.strip()[1:-2], links))

		for url in links: 
			yield scrapy.Request(url=url, callback=self.parse)

	def clean_text(self,t):
		t = t.replace('R$','')
		t = t.strip()
		t = t.replace('\n','')
		return t


	def parse(self, response):
		genero = "F"

		# Informações do deputado
		info = response.xpath("//ul[@class='informacoes-deputado']//li/text()").getall()
		info = list(map(lambda x: x.strip(), info))

		nome = info[0]
		data_nascimento = info[4]

		# Informações sobre presença

		## presença plenario
		presenca = response.xpath('//dd[@class="list-table__definition-description"]/text()').getall()
		presenca = list(map(lambda x: x.strip(), presenca))
		print(presenca)

		presenca_plenario = presenca[0][:-5]
		ausencia_justificada_plenario = presenca[1][:-5]
		ausencia_plenario = presenca[2][:-5]

		## presença comissão
		presenca_comissao = presenca[3][:-9]
		ausencia_justificada_comissao = presenca[4][:-9]
		ausencia_comissao = presenca[5][:-9]

		# Salario do deputado
		salario_bruto = self.clean_text(response.xpath('//a[@class="beneficio__info"]/text()').get())

		# Gastos totais parlamentar
		lista_gasto_total = response.xpath('//ul[@class="gastos-anuais-deputado-container"]//tbody//tr//td/text()').getall()
		lista_gasto_total = [self.clean_text(g) for g in lista_gasto_total]

		#### encontra indice de gabinete
		index_gab = -1
		for index,s in enumerate(lista_gasto_total[2:]):
			if s == 'Total Gasto':
				index_gab = index

		### Gastos totais
		gasto_total_par = lista_gasto_total[1]
		gasto_total_gab = lista_gasto_total[index_gab:][1]

		### busca gastos mensais
		MESES = ['JAN','FEV','MAR','MAI','ABR','JUN','JUL','AGO','SET','OUT','NOV','DEZ']

		parlamentar = [ 'gasto_jan_par', 'gasto_fev_par', 'gasto_mar_par', 'gasto_abr_par' , 'gasto_maio_par',
					'gasto_junho_par', 'gasto_jul_par', 'gasto_agosto_par', 'gasto_set_par',
					'gasto_out_par', 'gasto_nov_par', 'gasto_dez_par' ]
		gabinete = [ 'gasto_jan_gab', 'gasto_fev_gab', 'gasto_mar_gab', 'gasto_abr_gab' ,
			'gasto_maio_gab', 'gasto_junho_gab', 'gasto_jul_gab', 'gasto_agosto_gab',
			'gasto_set_gab', 'gasto_out_gab', 'gasto_nov_gab', 'gasto_dez_gab' ]
		
		grouped_total_par = []
		for i in range(len(lista_gasto_total) // 3):
			grouped_total_par.append(lista_gasto_total[i*3:(i+1)*3])

		mapping_parlamentar = {v1:v2 for v1,v2 in zip(MESES, parlamentar)}
		mapping_gabinete = {v1:v2 for v1,v2 in zip(MESES, gabinete)}

		index_gab = index_gab // 3
		total_gasto_parl= {v[0]:v[1] for v in grouped_total_par[:index_gab]}
		total_gasto_gab = {v[0]:v[1] for v in grouped_total_par[index_gab:]}

		## Reúne gastos mensais existentes
		gastos_parlamentar = {}
		for key,value in mapping_parlamentar.items():
			if key in total_gasto_parl:
				gastos_parlamentar[value] = total_gasto_parl[key]
			else:
				gastos_parlamentar[value] = '-'
		
		gastos_gabinete = {}
		for key,value in mapping_gabinete.items():
			if key in total_gasto_gab:
				gastos_gabinete[value] = total_gasto_gab[key]
			else:
				gastos_gabinete[value] = '-'

		dicio = {
			'nome':nome,
			'genero': genero,
			'presenca_plenario':presenca_plenario,
			'ausencia_justificada_plenario':ausencia_justificada_plenario,
			'ausencia_plenario':ausencia_plenario,
			'presenca_comissao':presenca_comissao,
			'ausencia_justificada_comissao':ausencia_justificada_comissao,
			'ausencia_comissao':ausencia_comissao,
			'data_nascimento':data_nascimento,
			'gasto_total_par':gasto_total_par,
			'gasto_total_gab':gasto_total_gab,
			'salario_bruto':salario_bruto
		}

		dicio.update(gastos_parlamentar)
		dicio.update(gastos_gabinete)

		yield dicio