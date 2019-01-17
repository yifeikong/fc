import os
import statsd

_emitter = None


def fmttags(measurement, tags):
    """
    >>> fmttags("foo", dict(hello="world", true="false"))
    'foo,hello=world,true=false'
    """
    if tags is None:
        return measurement
    tagstr = ",".join([f"{k}={v}" for k, v in tags.items()])
    return ",".join([measurement, tagstr])


class MetricsEmitter:
    def __init__(self, host, port, prefix):
        self._client = statsd.StatsClient(host, port, prefix)

    def emit_counter(self, key, value, *, tags=None, rate=1):
        key = fmttags(key, tags)
        self._client.incr(key, value, rate=rate)

    def emit_timer(self, key, value, *, tags=None, rate=1):
        key = fmttags(key, tags)
        self._client.timing(key, value, rate=rate)

    def emit_store(self, key, value, *, tags=None, rate=1, delta=False):
        key = fmttags(key, tags)
        self._client.gauge(key, value, rate=rate, delta=delta)


def init(*, host=None, port=None, prefix=None):
    global _emitter
    if host is None:
        host = os.getenv("STATSD_HOST")
    if port is None:
        port = os.getenv("STATSD_PORT")
    _emitter = MetricsEmitter(host, port, prefix)


def emit_counter(key, value, *, tags=None, rate=1):
    _emitter.emit_counter(key, value, tags=tags, rate=rate)


def emit_timer(key, value, *, tags=None, rate=1):
    _emitter.emit_timer(key, value, tags=tags, rate=rate)


def emit_store(key, value, *, tags=None, rate=1, delta=False):
    _emitter.emit_timer(key, value, tags=tags, rate=rate, delta=delta)


class TagStatsClient:
    def __init__(self, statsd_client):
        self._statsd_client = statsd_client

    def __getattr__(self, attr):
        def emit(*args, **kwargs):
            tags = kwargs.pop("tags", {})
            stat = fmttags(args[0], tags)
            method = getattr(self._statsd_client, attr)
            method(stat, *args[1:], **kwargs)

        return emit


if __name__ == "__main__":
    import doctest

    doctest.testmod()
