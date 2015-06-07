import pytest
from webtest import TestApp

from pyramid.config import Configurator


def setup_wsgi():
    configurator = Configurator()

    configurator.include("pyramid_jinja2")
    configurator.add_jinja2_renderer('.html')
    configurator.add_jinja2_search_path('websauna.viewconfig:tests/templates', name='.html')

    configurator.add_route("parent_hello", "/parent_hello")
    configurator.add_route("child_hello", "/child_hello")

    from websauna.viewconfig.tests import testmodule
    configurator.set_root_factory(testmodule.Root)
    configurator.scan(testmodule)

    wsgi = TestApp(configurator.make_wsgi_app())
    return wsgi


def test_override_context():
    """Subclasses may override the context for which the view belongs.."""
    wsgi = setup_wsgi()

    resp = wsgi.get("/parent/edit", status=200)
    assert resp.text == '200 OK\n\n\n\n\nEditing: parent\n\n'

    resp = wsgi.get("/child/edit", status=200)
    assert resp.text == '200 OK\n\n\n\n\nEditing: child\n\n'


def test_child_own_view():
    """Subclasses can defined their own view configs."""
    wsgi = setup_wsgi()

    resp = wsgi.get("/child2/show", status=200)
    assert resp.text == '200 OK\n\n\n\n\nShowing: child2\n\n'


def test_grand_child_view():
    """view_overrides work correctly on the second level of inheritance."""
    wsgi = setup_wsgi()

    resp = wsgi.get("/grand_child/edit", status=200)
    assert resp.text == '200 OK\n\n\n\n\nEditing: grand_child\n\n'


def test_invalid_override():
    """Trying to override non-view class causes an error.."""
    configurator = Configurator()

    with pytest.raises(RuntimeError):
        from websauna.viewconfig.tests import brokentestmodule



def test_rendered_override():
    """We can override renderer and route name for dispatched URLs."""
    wsgi = setup_wsgi()

    resp = wsgi.get("/parent_hello", status=200)
    assert resp.text.strip() == 'Hello Parent: ParentRouteView'

    resp = wsgi.get("/child_hello", status=200)
    assert resp.text.strip() == 'Hello Child: ChildRouteView'
