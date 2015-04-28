import inspect
import logging
import os
import sys

LOG_TO_STDOUT = False

log = logging.getLogger('scraping')
fmt = '[%(asctime)s] %(levelname)s - %(name)s: %(message)s'
datefmt = '%m/%d/%Y %I:%M:%S %p'

if LOG_TO_STDOUT:
  out_hdlr = logging.StreamHandler(sys.stdout)
  out_hdlr.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
  out_hdlr.setLevel(logging.WARNING)
  log.addHandler(out_hdlr)

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
