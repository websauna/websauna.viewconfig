from pyramid.view import view_config
from websauna.viewconfig import view_overrides


class ParentContext:
    pass


class ChildContext(ParentContext):
    pass


class Parent:

    @view_config(name="edit", context=ParentContext, renderer="foobar.html")
    def traversing_test(self):
        pass



@view_overrides(context=ChildContext)
class ChildWithRoute(Parent):
    pass


# @view_overrides(context=ChildContext)
# class ChildWithContext(Parent):
#     pass
#
#
# @view_overrides(context=ChildContext)
# class ChildWithContextAndViewConfigMix(Parent):
#
#     @view_config(name="edit", context=ChildContext, renderer="foobar.html")
#     def another_func(self):
#         pass
#
#     @view_config(route_name="parent", renderer="foobar.html")
#     def yet_another_func(self):
#         pass
