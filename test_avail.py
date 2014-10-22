import logging
formatter = logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


from backend import Search
import json


if __name__ == "__main__":

    z39 = Search()

    #ToDo: collect test items
    book = 'b3386235'


    rsp = z39.id(book)

    print(json.dumps(rsp, indent=2))

    z39.close()
