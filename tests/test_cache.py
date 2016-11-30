import os
import unittest
import tempfile
import hiro
import jira_cli.cache


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()
        jira_cli.cache.CACHE_DIR = self.cache_dir
    def test_cache_data_not_exist(self):
        data = jira_cli.cache.CachedData("foobar")
        self.assertTrue(data.get()==None)
        data.update({"foo":"bar"})
        self.assertEqual(jira_cli.cache.CachedData("foobar").get(),
                         {"foo": "bar"})
    def test_cache_invalidate(self):
        with hiro.Timeline().freeze() as timeline:
            data = jira_cli.cache.CachedData("foobar")
            data.update({"foo":"bar"})
            timeline.forward(1 + 60*60*24)
            self.assertTrue(data.get()==None)

    def test_clear_cache(self):
        data = jira_cli.cache.CachedData("foobar")
        data.update({"foo":"bar"})
        self.assertTrue(os.path.isfile(data.path))
        jira_cli.cache.clear_cache(data)
        self.assertFalse(os.path.isfile(data.path))
        jira_cli.cache.clear_cache()
        self.assertFalse(os.path.isdir(self.cache_dir))

    def test_decorated(self):
        @jira_cli.cache.cached("foo")
        def func(a,b):
            return a+b

        self.assertEqual(func(1,2), func(1,2))
        self.assertNotEqual(func(1,2), func(3,4))

        self.assertEqual(len(os.listdir(self.cache_dir)), 2)
