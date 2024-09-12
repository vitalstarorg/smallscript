from .SObject import sscontext, nil, undefined, true_, false_
from .SObject import SObject, Holder, Package, Scope, String, List, Map, Float, Integer, Number, Logger
import os
import logging

loglevel = os.environ.get('LOG_LEVEL', 'WARNING')
logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

handler = logging.StreamHandler()
handler.setLevel(loglevel)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

__all__ = [ # Classes
            'SObject', 'Holder', 'Package', 'Scope', 'String', 'List', 'Map',
           'Float', 'Integer', 'Number', 'Logger',

            # Singletons
           'sscontext', 'nil', 'undefined', 'true_', 'false_']