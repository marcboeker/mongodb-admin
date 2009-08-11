MongoDB = {
	getDatabases: function(callBack) {
		$.getJSON('/', {}, callBack);
	},

	getCollections: function(db, callBack) {
		$.getJSON('/' + db, {}, callBack);
	},

	getDocuments: function(db, collection, options, callBack) {
		$.getJSON('/' + db + '/' + collection + '/', options, callBack);
	}
};
