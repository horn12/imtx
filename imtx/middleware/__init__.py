from django.db import connection
from django.template import Template, Context
from imtx.settings import *
from imtx.utils import logs

class SQLLogMiddleware:
    """
	SQL query log middleware for keep watch over the db query and save log to file when DEBUG turn on.
    Author: tobias
    url: http://www.djangosnippets.org/snippets/161/
    """
    def process_response ( self, request, response ): 
        if DEBUG:
            if len(connection.queries) > 0:
                time = 0.0
                for q in connection.queries:
                    time += float(q['time'])

                t = Template('''SQL Query:
            Total query count: {{ count }}
            Total execution time: {{ time }}            
                {% for sql in sqllog %}
                {{ sql.time }}: {{ sql.sql|safe }}
                {% endfor %}
        ''')
                logs.debug(t.render(Context({
                    'sqllog':connection.queries,
                    'count':len(connection.queries),
                    'time':time})
                    ))

        return response
