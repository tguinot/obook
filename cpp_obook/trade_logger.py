from inspect import getframeinfo
import logging

l_info = lambda c: getframeinfo(c).filename +':'+ str(getframeinfo(c).lineno)

def get_logger(logger_name, filepath):
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.ERROR)

	handler = logging.FileHandler(filepath)
	handler.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	logger.addHandler(handler)

	logger.info('Logger initiated')

	return logger

