class ScenarioSheet:
	def __init__(self,configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		outhstore = config.get("Google","outhstore")
		outhfile = config.get("Google","outhfile")
		scenariosheetkey=config.get("ScemarioSheet","sheetkey")
