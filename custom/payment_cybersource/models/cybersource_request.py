# -*- coding: utf-8 -*-
import json
import logging
import requests

from uuid import uuid4

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.payment.models.payment_acquirer import _partner_split_name

_logger = logging.getLogger(__name__)


class AuthorizeAPI():
    """Authorize.net Gateway API integration.

    This class allows contacting the Authorize.net API with simple operation
    requests. It implements a *very limited* subset of the complete API
    (http://developer.authorize.net/api/reference); namely:
        - Customer Profile/Payment Profile creation
        - Transaction authorization/capture/voiding
    """

    AUTH_ERROR_STATUS = 3

    def __init__(self, acquirer):
        """Initiate the environment with the acquirer data.

        :param record acquirer: payment.acquirer account that will be contacted
        """
        if acquirer.state == 'test':
            self.url = 'https://apitest.authorize.net/xml/v1/request.api'
        else:
            self.url = 'https://api.authorize.net/xml/v1/request.api'

        self.state = acquirer.state
        self.name = acquirer.authorize_login
        self.transaction_key = acquirer.authorize_transaction_key

    def _authorize_request(self, data):
        _logger.info('_authorize_request: Sending values to URL %s, values:\n%s', self.url, data)
        resp = requests.post(self.url, json.dumps(data))
        resp.raise_for_status()
        resp = json.loads(resp.content)
        _logger.info("_authorize_request: Received response:\n%s", resp)
        messages = resp.get('messages')
        if messages and messages.get('resultCode') == 'Error':
            return {
                'err_code': messages.get('message')[0].get('code'),
                'err_msg': messages.get('message')[0].get('text')
            }

        return resp
