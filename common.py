import yaml

__config = None


def config():
	global __config
	if not __config:
		with open('config.yaml', mode='r') as f:		#Para realizar nuestra “conversion” se hace uso de la
			__config = yaml.safe_load(f)				#funcionyaml.safe_load(f) que recibe el archivo 
	return __config										#como parametro y retorna un diccionario.