from cowin_get_email.databases import user_model
from datetime import datetime
from cowin_get_email.utility import common_util,api
import logging
import json
import config


def getUserOfDistId(distID):

    x,_= user_model.getUserofDistID(distID)
    return x