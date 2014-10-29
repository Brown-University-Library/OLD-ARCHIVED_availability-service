import json, logging
from backend import Search


formatter = logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)



if __name__ == "__main__":

    z39 = Search( logger )

    #ToDo: collect test items
    book = 'b3386235'
    journal = 'b4074295'
    online_journal = 'b7091233'

    rsp = z39.id(online_journal)

    print(json.dumps(rsp, indent=2))

    print len(rsp[0]['items'])
    print len(rsp[0]['barcodes'])

    z39.close()
