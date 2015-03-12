import logging
import sys

# Log WARNING and higher to stdout
log = logging.getLogger('scraping')
out_hdlr = logging.StreamHandler(sys.stdout)
fmt = '[%(asctime)s] %(levelname)s - %(name)s: %(message)s'
datefmt = '%m/%d/%Y %I:%M:%S %p'
out_hdlr.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
out_hdlr.setLevel(logging.WARNING)
log.addHandler(out_hdlr)
