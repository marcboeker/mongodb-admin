# What's this?

MongoDB admin is a dirty attempt to build a web frontend for MongoDB like 
CouchDBs Futon or PHPMyAdmin. It ist still very very pre-alpha but MongoDB
admin is looking for interested developers that want to make it big.

MongoDB admin is pure JavaScript (jQuery) and HTML/CSS with a REST backend
written in Python. The REST API included in MongoDB has some issues[1], that
make it unpossible at the moment to use MongoDBs full advantages.

[1] Supplying <pre>?filter__id=5sdf34sdfsdf</pre> => results in _id=5, but
<pre>?filter__id=asdf</pre> works well.

# Installation

I assume you have Python 2.6 installed.

## Install python requirements for REST API

<pre>
sudo easy_install cherrypy
sudo easy_install pymongo
</pre>

## Get source

<pre>
git clone git://github.com/marcboeker/mongodb-admin.git
</pre>

## Run REST server

<pre>
cd mongodb-admin
python rest.py
</pre>

# Contribution

Everyone that has interest in maintaining or contribute to this 
project is welcome.