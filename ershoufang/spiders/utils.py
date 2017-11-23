#encoding=utf-8
import re
class NumberUtil(object):
	def __init__(self):
		pass
	@staticmethod	
	def fromString(string):
		formatter = "1234567890."
		for s in string:
			if not s in formatter:
				string = string.replace(s,"")
		return string

class StringUtil(object):
	def __init__(self):
		pass
	@staticmethod
	def filtString(string,regex,flag=True):
		if flag:
			return re.match(string,regex)
		return not re.match(string,regex)
if __name__ == "__main__":
	print(NumberUtil.fromString("124dfsdfdweewewe5555f"))
	print(bool(StringUtil.filtString("ddd","1234")))
