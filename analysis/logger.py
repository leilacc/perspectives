import inspect
import logging
import os
import sys

# Log WARNING and higher to stdout
log = logging.getLogger('compare_articles')
out_hdlr = logging.StreamHandler(sys.stdout)
fmt = '[%(asctime)s] %(levelname)s - %(name)s: %(message)s'
datefmt = '%m/%d/%Y %I:%M:%S %p'
out_hdlr.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
logging.basicConfig(filename='%s/compare_articles.log' % cwd,
                    level=logging.DEBUG, format=fmt, datefmt=datefmt)
