import inspect
import rpyc
from rpyc.lib.compat import pickle

from rpyc_couchbase.exceptions import map_exception


class KvStore(object):
    def __init__(self, remote_host, db_host, username, password):
        self._conn = rpyc.classic.connect(remote_host, keepalive=True)
        self._couchbase = self._conn.modules["couchbase.cluster"]

        self.cluster = self._couchbase.Cluster(
            'couchbase://{}'.format(db_host))
        cb_credentials = self._couchbase.PasswordAuthenticator(
            username=username, password=password)
        self.cluster.authenticate(cb_credentials)

        self.FMT_UTF8 = self._conn.modules['couchbase'].FMT_UTF8
        self.transcoder = self._conn.modules['couchbase.transcoder']
        self.FMT_BYTES = self._conn.modules['couchbase.transcoder'].FMT_BYTES
        self.FMT_JSON = self._conn.modules['couchbase.transcoder'].FMT_JSON

    def __del__(self):
        if hasattr(self, '_conn'):
            self._conn.close()

    def open_bucket(self, name, **kwargs):
        bucket = self.cluster.open_bucket(name, **kwargs)
        return KvBucket(self, bucket)


class ValueResult(object):
    def __init__(self, wrappee):
        for name, value in inspect.getmembers(wrappee):
            if not hasattr(self, name):
                try:
                    setattr(self, name, pickle.loads(pickle.dumps(value)))
                except TypeError:
                    pass


class KvBucket(object):

    def __init__(self, store, bucket):
        self._store = store
        self._bucket = bucket

    def get(self, key, **kwargs):
        try:
            doc = self._bucket.get(key, **kwargs)
            return ValueResult(doc)
        except rpyc.core.vinegar.GenericException as exc:
            map_exception(exc)

    def get_multi(self, keys, **kwargs):
        try:
            docs = self._bucket.get_multi(keys, **kwargs)
            ret = {}
            for key in docs:
                ret[key] = ValueResult(docs[key])
            return ret
        except rpyc.core.vinegar.GenericException as exc:
            map_exception(exc)

    def insert(self, key, value, format=None, **kwargs):
        try:
            return self._bucket.insert(
                key, rpyc.classic.deliver(self._store._conn, value),
                format=format, **kwargs)
        except rpyc.core.vinegar.GenericException as exc:
            map_exception(exc)

    def upsert(self, key, value, format=None, **kwargs):
        try:
            return self._bucket.upsert(
                key, rpyc.classic.deliver(self._store._conn, value),
                format=format, **kwargs)
        except rpyc.core.vinegar.GenericException as exc:
            map_exception(exc)

    def remove(self, key, **kwargs):
        try:
            return self._bucket.remove(key, **kwargs)
        except rpyc.core.vinegar.GenericException as exc:
            map_exception(exc)
