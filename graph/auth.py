
import os
import os.path
import output
import stat
import facebook
import json
import urllib2
import BaseHTTPServer
import webbrowser
import httplib
import mimetools
import mimetypes
import cookielib
import types

from urlparse import urlparse, parse_qs
from urllib import urlencode
from pprint import pprint

APP_ID = ''
APP_SECRET = ''
SERVER_PORT = 8080
REDIRECT_URI = 'http://127.0.0.1:%s/' % SERVER_PORT
ACCESS_TOKEN = None
LOCAL_FILE = locations.authentication
AUTH_SCOPE = []

__all__ = [
    'help',
    'authenticate',
    'graph',
    'graph_post',
    'graph_delete',
    'shell',
    'fql',
    'APP_ID',
    'SERVER_PORT',
    'ACCESS_TOKEN',
    'AUTH_SCOPE',
    'LOCAL_FILE']

def _get_url(path, args=None, graph=True):
    args = args or {}
    if ACCESS_TOKEN:
        args['access_token'] = ACCESS_TOKEN
    subdomain = 'graph' if graph else 'api'
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://%s.facebook.com" % subdomain
    else:
        endpoint = "http://%s.facebook.com" % subdomain
    return endpoint+str(path)+'?'+urlencode(args)

class _MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and not isinstance(data, types.StringTypes):
            files = []
            params = []
            try:
                for key, value in data.items():
                    if isinstance(value, types.FileType):
                        files.append((key, value))
                    else:
                        params.append((key, value))
            except TypeError:
                raise TypeError("not a valid non-string sequence or mapping object")

            if len(files) == 0:
                data = urlencode(params)
            else:
                boundary, data = self.multipart_encode(params, files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request

    https_request = http_request

    def multipart_encode(self, params, files, boundary=None, buffer=None):
        boundary = boundary or mimetools.choose_boundary()
        buffer = buffer or ''
        for key, value in params:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + value + '\r\n'
        for key, fd in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; '
            buffer += 'name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            fd.seek(0)
            buffer += '\r\n' + fd.read() + '\r\n'
        buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer


class _RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        params = parse_qs(urlparse(self.path).query)
        ACCESS_TOKEN = params.get('access_token', [None])[0]
        if ACCESS_TOKEN:
            data = {'scope': AUTH_SCOPE,
                    'access_token': ACCESS_TOKEN}

            self.wfile.write("You have successfully logged in to facebook with Less Visual Socialize. ")
        else:
            self.wfile.write('<html><head>'
                             '<script>location = "?"+location.hash.slice(1);</script>'
                             '</head></html>')


def authenticate():
    """Authenticate with facebook so you can make api calls that require auth.

    Alternatively you can just set the ACCESS_TOKEN global variable in this
    module to an access token you get from facebook.

    If you want to request certain permissions, set the AUTH_SCOPE global
    variable to the list of permissions you want.
    """
    global ACCESS_TOKEN, APP_ID, APP_SECRET, LOCAL_FILE
    needs_auth = True
    if needs_auth:
        output.speak("Logging you into facebook... Plese accept any dialog from facebook")
        webbrowser.open('https://www.facebook.com/dialog/oauth?' +
                        urlencode({'client_id':APP_ID,
                                   'redirect_uri':REDIRECT_URI,
                                   'response_type':'token',
                                   'scope':','.join(AUTH_SCOPE)}))

        httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', SERVER_PORT), _RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()
    # extend short-life access token with a long life one.
    if os.path.exists(LOCAL_FILE):
        os.remove(LOCAL_FILE)
    fb = facebook.GraphAPI(ACCESS_TOKEN)
    data = fb.extend_access_token(APP_ID, APP_SECRET)
    open(LOCAL_FILE, "w").write(json.dumps(data))

def graph(path, params=None):
    """Send a GET request to the graph api.

    For example:

      >>> graph('/me')
      >>> graph('/me', {'fields':'id,name'})

    """
    return json.load(urllib2.urlopen(_get_url(path, args=params)))

def graph_post(path, params=None):
    """Send a POST request to the graph api.

    You can also upload files using this function.  For example:

      >>> graph_post('/me/photos',
      ...            {'name': 'My Photo',
      ...             'source': open("myphoto.jpg")})

    """
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
        _MultipartPostHandler)
    return json.load(opener.open(_get_url(path), params))

def graph_delete(path, params=None):
    """Send a DELETE request to the graph api.

    For example:

      >>> msg_id = graph_post('/me/feed', {'message':'hello world'})['id']
      >>> graph_delete('/'+msg_id)

    """
    if not params:
        params = {}
    params['method'] = 'delete'
    return graph_post(path, params)

def fql(query):
    """Make an fql request.

    For example:

      >>> fql('SELECT name FROM user WHERE uid = me()')

    """
    url = _get_url('/method/fql.query',
                   args={'query': query, 'format': 'json'},
                   graph=False)
    return json.load(urllib2.urlopen(url))


def initialize():
	global ACCESS_TOKEN, LOCAL_FILE
	if os.path.exists(LOCAL_FILE):
		data = json.loads(open(LOCAL_FILE).read())
		ACCESS_TOKEN = data['access_token']
	else:
		authenticate()
	if is_valid == False:
		output.speak("The Current access token is not valid any more, application will update it now")
		os.remove(LOCAL_FILE)
		authenticate()
		
		

def is_valid():
	"""A test function to see wether the access token is valid
	"""
	global ACCESS_TOKEN
	fb = facebook.GraphAPI(ACCESS_TOKEN)
	try:
		fb.get_object("me")
	except facebook.GraphAPIError:
		return False
	return True


