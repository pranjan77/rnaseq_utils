# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from rnaseq_utils.rnaseq_utilsImpl import rnaseq_utils
from rnaseq_utils.rnaseq_utilsServer import MethodContext
from rnaseq_utils.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class rnaseq_utilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('rnaseq_utils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'rnaseq_utils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = rnaseq_utils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        """
#        params =  {'workspace_name': "tackerx06:narrative_1684180210411",
#                    "expressionset_ref": "146675/180/1",
#                    "input_type": "genes",
#                    "diff_expression_obj_name": "test_de",
#                     "run_all_combinations": 1,
#                     "condition_pairs": []
#        }
        """
        params =  {'workspace_name': "pranjan77:narrative_1689871898639",
                    "expressionset_ref": "152777/373/1"
        }

                
        ret = self.serviceImpl.run_rnaseq_utils(self.ctx, params)
