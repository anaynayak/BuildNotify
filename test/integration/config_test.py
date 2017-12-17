import unittest

from PyQt5 import QtCore

from buildnotifylib.config import Config
from buildnotifylib.preferences import Preferences
from buildnotifylib.serverconfig import ServerConfig


class ConfigTest(unittest.TestCase):
    def setUp(self):
        q_settings = QtCore.QSettings("BuildNotifyTest", "BuildNotifyTest")
        q_settings.clear()
        self.config = Config(q_settings)

    def test_should_persist_user_project_excludes(self):
        self.config.set_project_excludes('https://github.com/anaynayak/buildnotify/cctray.xml',
                                         ['buildnotify::test-server'])
        self.assertEquals(['buildnotify::test-server'],
                          self.config.get_project_excludes('https://github.com/anaynayak/buildnotify/cctray.xml'))

    def test_should_persist_empty_user_project_excludes(self):
        self.config.set_project_excludes('https://github.com/anaynayak/buildnotify/cctray.xml', [])
        self.assertEquals([], self.config.get_project_excludes('https://github.com/anaynayak/buildnotify/cctray.xml'))

    def test_should_return_an_empty_list_if_unmapped(self):
        self.assertEquals([], self.config.get_project_excludes('https://github.com/anaynayak/buildnotify/buildnotify.xml'))

    def test_should_store_server_preferences(self):
        self.config.save_server_config(
            ServerConfig('https://github.com/anaynayak/buildnotify/cctray.xml', ['excludedproject'], 'EDT', 'prefix',
                         'user', 'pass'))
        server = self.config.get_server_config("https://github.com/anaynayak/buildnotify/cctray.xml")
        self.assertEquals('user', server.username)
        self.assertEquals('pass', server.password)
        self.assertEquals("https://github.com/anaynayak/buildnotify/cctray.xml", server.url)
        self.assertEquals('EDT', server.timezone)
        self.assertEquals(['excludedproject'], server.excluded_projects)
        self.assertEquals('prefix', server.prefix)
        self.assertEquals(["https://github.com/anaynayak/buildnotify/cctray.xml"], self.config.get_urls())

    def test_should_get_empty_if_missing(self):
        server = self.config.get_server_config('someurl')
        self.assertEquals('', server.username)

    def test_should_return_all_servers(self):
        self.config.save_server_config(ServerConfig('url1', [], 'EDT', 'prefix', 'user', 'pass'))
        self.config.save_server_config(ServerConfig('url2', [], 'EDT', 'prefix', 'user', 'pass'))
        servers = self.config.get_server_configs()
        self.assertEquals(2, len(servers))
        self.assertEquals('http://url1', servers[0].url)
        self.assertEquals('http://url2', servers[1].url)

    def test_should_update_preferences(self):
        self.config.update_preferences(Preferences(['url1'], 300, '/bin/sh', True, False, True, []))

        self.assertEquals(self.config.get_urls(), ['url1'])
        self.assertEquals(self.config.get_interval_in_seconds(), 300)
        self.assertEquals(self.config.get_custom_script(), '/bin/sh')
        self.assertEquals(self.config.get_custom_script_enabled(), True)
        self.assertEquals(self.config.get_sort_by_last_build_time(), False)
        self.assertEquals(self.config.get_sort_by_name(), True)


if __name__ == '__main__':
    unittest.main()
