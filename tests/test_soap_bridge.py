"""

"""
import os
import tempfile
import unittest


import jira_cli
from jira_cli.bridge import JiraSoapBridge
from jira_cli.utils import Config
from .common_bridge_cases import BridgeTests, jiravcr


class SoapBridgeTests(unittest.TestCase, BridgeTests):
    def setUp(self):
        tmp_config = tempfile.mktemp()
        self.config = Config(tmp_config)
        jira_cli.utils.CONFIG_FILE = tmp_config
        self.cache_dir = tempfile.mkdtemp()
        jira_cli.cache.CACHE_DIR = self.cache_dir
        self.config.username = "testuser"
        self.config.password = "testpassword"
        self.vcr_directory = "fixtures/soap"
        with jiravcr.use_cassette(os.path.join(self.vcr_directory, "login.yaml")):
            self.bridge = JiraSoapBridge("https://indydevs.atlassian.net",
                                         self.config)
            self.bridge.login(self.config.username, self.config.password)
