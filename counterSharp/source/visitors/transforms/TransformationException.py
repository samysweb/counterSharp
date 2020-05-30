class TransformationException(Exception):
	def __init__(self, messageParam, coordParam):
		super().__init__(messageParam+" at "+str(coordParam))