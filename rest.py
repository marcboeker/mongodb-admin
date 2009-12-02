from pymongo.connection import Connection
from pymongo.objectid import ObjectId
from pymongo.dbref import DBRef

import datetime
import json
import os

import cherrypy

conn = Connection('127.0.0.1', pool_size=10)

class ComplexEncoder(json.JSONEncoder):
	"""Advise JSON encoder to encode some datatypes a special way.
	"""
	
	def default(self, obj):
		# Handle MongoDB ObjectId
		if isinstance(obj, ObjectId):
			return obj.url_encode()
		# Datetime values
		elif isinstance(obj, datetime.datetime):
			return str(obj)
		# DBRefs
		elif isinstance(obj, DBRef):
			return json.dumps({
				'$id': obj.id.url_encode(), '$ns': obj.collection
			})
		return json.JSONEncoder.default(self, obj)

class Root(object):
	"""Main entry class.
	"""


	def default(self, *args, **kwargs):
		"""Catch all requests.
		"""
		
		# /db/ => show all collections of a database
		if len(args) == 1:
			db = args[0]
			cursor = conn[db].collection_names()

			# return collections in JSON			
			return json.dumps({
				'database': db,
				'collections': cursor,
				'total_rows': len(cursor)
			})
		# /db/collection/ => show first 10 docs in collection
		elif len(args) == 2:
			db, coll = args
			
			# Supply filter as normal pymongo.collection.find() spec
			if 'filter' in kwargs and len(kwargs['filter']) > 0:
				filter = json.loads(kwargs['filter'])
			else:
				filter = {}
			
			cursor = conn[db][coll].find(filter)

			# Sorting
			if 'sort' in kwargs and len(kwargs['sort']) > 0:
				sort = json.loads(kwargs['sort'])
				cursor = cursor.sort(sort)
			else:
				sort = {}

			# Limiting
			try:
				limit = int(kwargs['limit'])
				cursor = cursor.limit(limit)
			except:
				limit = 0

			# Offset
			try:
				skip = int(kwargs['skip'])
				cursor = cursor.skip(skip)
			except:
				skip = 0

			# I'm shure there is a better way
			docs = []
			for doc in cursor:
				docs.append(doc)
			
			# We got everything? Let's go
			return json.dumps({
				'database': db,
				'collection': coll,
				'offset': skip,
				'documents': docs,
				'total_rows': len(docs),
				'query': filter,
			 }, cls=ComplexEncoder, skipkeys=True)
		# / => show all databases
		else:
			cursor = conn.database_names()
			
			return json.dumps({
				'databases': cursor,
				'total_rows': len(cursor)
			})
	default.exposed = True

# Some cherrypy config vars
cherrypy.config.update({
	#'environment': 'production',
	'log.screen': True,
	'server.process_pool': 10,
	'tools.encode.on': True,
	'tools.encode.encoding': 'utf-8'
})

conf = {'/_': {
	'tools.staticdir.on': True,
	'tools.staticdir.dir': '/'.join([
		os.path.dirname(os.path.abspath(__file__)), 'web'
	])}
}

# Get cherrypy up and running
cherrypy.quickstart(Root(), '/', config=conf)
