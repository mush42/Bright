from db_magic import *

class GraphItem(Entity):
	"""base class for all graph-api data"""
	path = string(blank=False)
	item_id = string(uniqu=True)


class User(GraphItem):
	"""Base class for facebook user"""
	

class Me(User):
	"""Represent current authenticated user profile"""

class Friend(User):
	"""Represent a user with friend relationship"""

class Feed(GraphItem):
	"""Represent Feed in a time line"""

class comment(Feed):
	"""Represent A comment"""

class Event(Feed):
	"""An Event in user's time-line"""

class Group(GraphItem):
	"""A facebook Group"""

class Page(GraphItem):
	"""A facebook Page"""
