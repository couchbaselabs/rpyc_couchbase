import json
import rpyc_couchbase
import unittest
import zlib


class TestStore(object):
    def __init__(self):
        self.store = rpyc_couchbase.KvStore('localhost', '10.143.205.101',
                                            'Administrator', 'password')
        self.bucket = self.store.open_bucket('test')


class SubclassStore(TestStore):
    def __init__(self):
        super(SubclassStore, self).__init__()
        self.data = {'a': 'bcd'}


class CouchbaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        store = rpyc_couchbase.KvStore('localhost', '10.143.205.101',
                                       'Administrator', 'password')
        bucket = store.open_bucket('test')
        bucket._bucket.flush()
        bucket.insert('test', {'abc': 123})
        bucket.insert('test2', {'def': 456})

    @classmethod
    def tearDownClass(cls):
        store = rpyc_couchbase.KvStore('localhost', '10.143.205.101',
                                       'Administrator', 'password')
        bucket = store.open_bucket('test')
        bucket._bucket.flush()

    def setUp(self):
        self.store = rpyc_couchbase.KvStore('localhost', '10.143.205.101',
                                            'Administrator', 'password')
        self.bucket = self.store.open_bucket('test')

    def tearDown(self):
        del self.store

    def test_get_multi(self):
        docs = self.bucket.get_multi(['test', 'test2'])
        self.assertEqual(len(docs), 2)

    def test_missing_get(self):
        self.assertRaises(rpyc_couchbase.NotFoundError,
                          self.bucket.get, 'missing_document')

    def test_remove(self):
        self.bucket.insert('test_delete', {'abc': 123})
        self.bucket.remove('test_delete')

    # No format applied

    def test_default_upsert(self):
        self.bucket.upsert('test_default_upsert', {'abc': 123})
        self.bucket.remove('test_default_upsert')

    def test_default_insert(self):
        self.bucket.insert('test_default_insert', {'abc': 123})
        self.bucket.remove('test_default_insert')

    def test_default_get(self):
        self.bucket.insert('test_default_get', {'abc': 123})
        doc = self.bucket.get('test_default_get')
        self.assertEqual(doc.key, 'test_default_get')
        self.assertDictEqual(dict(doc.value), {'abc': 123})
        self.bucket.remove('test_default_get')

    # Binary format applied

    def test_upsert_binary(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        result = zlib.compress(json.dumps(value), 3)
        self.bucket.upsert('test_binary_upsert', result,
                           format=self.store.FMT_BYTES)
        self.bucket.remove('test_binary_upsert')

    def test_insert_binary(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        result = zlib.compress(json.dumps(value), 3)
        self.bucket.insert('test_binary_insert', result,
                           format=self.store.FMT_BYTES)
        self.bucket.remove('test_binary_insert')

    def test_binary_get(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        result = zlib.compress(json.dumps(value), 3)
        self.bucket.insert('test_binary_get', result,
                           format=self.store.FMT_BYTES)

        doc = self.bucket.get('test_binary_get')
        self.assertEqual(doc.flags, self.store.FMT_BYTES)
        decode = json.loads(zlib.decompress(doc.value))
        self.assertDictEqual(decode, value)
        self.bucket.remove('test_binary_get')

    # JSON format applied

    def test_json_insert(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        self.bucket.insert('test_json_insert', value,
                           format=self.store.FMT_JSON)
        self.bucket.remove('test_json_insert')

    def test_json_upsert(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        self.bucket.upsert('test_json_upsert', value,
                           format=self.store.FMT_JSON)
        self.bucket.remove('test_json_upsert')

    def test_json_get(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        self.bucket.insert('test_json_get', value,
                           format=self.store.FMT_JSON)
        doc = self.bucket.get('test_json_get')
        self.assertEqual(doc.flags, self.store.FMT_JSON)
        self.assertEqual(doc.key, 'test_json_get')
        self.assertDictEqual(doc.value, value)
        self.bucket.remove('test_json_get')


class CouchbaseClassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        store = rpyc_couchbase.KvStore('localhost', '10.143.205.101',
                                       'Administrator', 'password')
        bucket = store.open_bucket('test')
        bucket._bucket.flush()
        bucket.insert('test', {'abc': 123})
        bucket.insert('test2', {'def': 456})

    @classmethod
    def tearDownClass(cls):
        store = rpyc_couchbase.KvStore('localhost', '10.143.205.101',
                                       'Administrator', 'password')
        bucket = store.open_bucket('test')
        bucket._bucket.flush()

    def setUp(self):
        self.storeclass = SubclassStore()

    # JSON format applied

    def test_json_insert(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        self.storeclass.bucket.insert('test_json_insert', value,
                                      format=self.storeclass.store.FMT_JSON)
        self.storeclass.bucket.remove('test_json_insert')

    def test_json_upsert(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        self.storeclass.bucket.upsert('test_json_upsert', value,
                                      format=self.storeclass.store.FMT_JSON)
        self.storeclass.bucket.remove('test_json_upsert')

    def test_json_get(self):
        value = {'abc': 'def', 'ghi': {'list': ['foo', 'bar']}}
        self.storeclass.bucket.insert('test_json_get', value,
                                      format=self.storeclass.store.FMT_JSON)
        doc = self.storeclass.bucket.get('test_json_get')
        self.assertEqual(doc.flags, self.storeclass.store.FMT_JSON)
        self.assertEqual(doc.key, 'test_json_get')
        self.assertDictEqual(doc.value, value)
        self.storeclass.bucket.remove('test_json_get')