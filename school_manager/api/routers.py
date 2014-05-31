from rest_framework.routers import Route, SimpleRouter

class NestedRouter(object):
	def __init__(self, parent_router, parent_prefix, *args, **kwargs):
		self.parent_router = parent_router
		self.parent_prefix = parent_prefix
		this.router = SimpleRouter()
		parent_registry = [registered for registered in self.parent_router.registry if registered[0] == self.parent_prefix]
		