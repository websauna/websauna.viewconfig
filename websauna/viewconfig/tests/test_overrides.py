from webtest import TestApp

from pyramid.config import Configurator


def test_override_context():
    configurator = Configurator()
    from websauna.viewconfig.tests import testmodule
    configurator.scan(testmodule)
    wsgi = TestApp(configurator.make_wsgi_app())

    resp = wsgi.get("/", status=200)




