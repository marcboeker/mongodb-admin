MongoDB.templates = {
	databases: function(data) {
		$(data.databases).each(function(idx, val) {
			var option = $('<option />');
			option.html(val);
			option.val(val);
		
			$('#databases').append(option);
		});
		
		$('#databases').change(function() {
			MongoDB.getCollections(this.value, MongoDB.templates.collections);
		});
	},

	collections: function(data) {
		$('#collections').html('');
		$(data.collections).each(function(idx, val) {
			var option = $('<option />');
			option.html(val);
			option.val(val);
			
			$('#collections').append(option);
		});
		$('#collections').change(function() {
			MongoDB.getDocuments(data.database, this.value, MongoDB.templates.documents);
		});
	},

	buildDocTree: function(obj) {
		var type = typeof obj;
		
		var ul = $('<ul />');
		if (type == 'string' || type == 'number' || type == 'boolean') { 
			var ul_inner = $('<ul />');
			var li = $('<li />');
			var span = $('<span />');

			span.html(obj.toString());
			li.append(span);
			ul_inner.append(li);

			return ul_inner;
		} else if (type == 'object') {
			for (var key in obj) {
				var li = $('<li />');
				var span = $('<span />');
				span.html(key);
				li.append(span);
				li.append(MongoDB.templates.buildDocTree(obj[key]));
				ul.append(li);
			}
			return ul;
		} else if (type == 'array') {
			var ul_inner = $('<ul />');
			$(obj).each(function(idx, val) {
				var li = $('<li />');
				li.append(MongoDB.templates.buildDocTree(val));
				ul_inner.append(li);
			});
			return ul_inner;
		}
		return ul;
	},

	documents: function(data) {
		$('#documents').html('');
		
		var ul = $('<ul />');
		$(data.documents).each(function(idx, val) {
			var li = $('<li />')
			li.html(val._id || '[no name]');
			ul.append(li);
			
			delete val._id;
			li.append(MongoDB.templates.buildDocTree(val).treeview({collapsed: true}));
		});
		$('#documents').append(ul);
		$('#documents').append('<p>Total Documents: ' + data.total_rows + '</p>');
	},
};
