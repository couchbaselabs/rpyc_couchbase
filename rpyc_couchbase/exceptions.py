import re


exception_re = re.compile(r'.*, catch (?P<exception>.*)\)')


class CouchbaseRPCError(BaseException):
    def __init__(self, exception):
        self._exception = exception


class NotFoundError(CouchbaseRPCError):
    pass


class TimeoutError(CouchbaseRPCError):
    pass


class TemporaryFailError(CouchbaseRPCError):
    pass


class ValueFormatError(CouchbaseRPCError):
    pass


class KeyExistsError(CouchbaseRPCError):
    pass


def map_exception(exception):
    exception = exception_re.match(exception.pyexc)
    if exception:
        exception = exception.group('exception')
        if exception and exception in EXCEPTION_MAP:
            raise EXCEPTION_MAP[exception](exception)

    raise RuntimeError('Unable to decode remote '
                       'exception:\n\t{}'.format(repr(exception)))


EXCEPTION_MAP = {
    'NotFoundError': NotFoundError,
    'TimeoutError': TimeoutError,
    'TemporaryFailError': TemporaryFailError,
    'ValueFormatError': ValueFormatError,
    'KeyExistsError': KeyExistsError
}
