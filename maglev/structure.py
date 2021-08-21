import typing


class Response:
  '''
  This class contains the Response data to be sent in a manageable format.
  The response object does not take external parametrs, but has some attributes which can be set by accessing.
  The attributes are:
  `headers` of type dict, it has the HTTP headers to be sent back to the user.
  `cookies` of type dict, it has the cookies to send back to the user. The cookies to be sent must be of type `maglev.structure.Cookie`
  eg:
  ```py
  response.cookies["sessid"] = Cookie("no_login",20*60)
  ```
  ''' 
  headers = dict()
  cookies = dict()
  headers['content-type'] = 'text/html'
  body = ''
  status = 200
  def append(self,message):
    self.body += message


class Request:
  '''
  This class contains the information requested by the user.
  The functions called by `Router.handler` take this as the first argument.
  It takes:
  `headers` as an array of headers passed by the server, and converts them to a dict.
  `method` as a string which is passed by the server. It is the HTTP request method.
  `path` as a string which is passed by the server. It is the HTTP request path.
  `query` as a dict(string,array). It is obtained from the server as a string and is then parsed into the dictionary with `urllib.parse.parse_qs`

  '''
  params = dict()
  headers = dict()
  cookies = dict()
  query = dict()
  body = dict()
  def __init__(self, method:str, path:str, headers, query, body, *args):
    '''
    Args:
      self: The :class:`maglev.structure.Request`
      method(str): The HTTP method used by the client.
      path(str): The path requested by the client.
      headers(list): The HTTP headers obtained from the ASGI scope, of send.
      query(str): The `GET` query string, obtained from ASGI scope of send.
      body(str): The HTTP request body. 
    '''
    self.method = method
    self.path = path
    self.query = query
    self.query.update( (k,query[k][0]) for k in query )
    self.body = body
    self.body.update( (k,body[k][0]) for k in body )
    for header_pair in headers:
      self.headers[header_pair[0].decode()]=header_pair[1].decode()
    if 'cookie' in self.headers.keys():
      [self.cookies.update({_.split('=')[0]:_.split('=')[1]}) for _ in self.headers['cookie'].split(';')] 
    self.path_array = list(
      filter(
        lambda x: x!='',path.split('/')
        )
      )

class Response404:
    headers = dict()
    cookies = dict()
    headers['content-type'] = 'text/html'
    body = 'Not found!!'
    status = 404


class Cookie:
  '''
  This class is used to send cookies to the user.
  Eg:
  ```py
  @router.get('/')
  async def index(request,response):
    response.cookies["sessid"] = Cookie("no_login",20*60)
    ...
    return response
  ```
  This takes: 
  `value` as string,
  `max_age` as integer (default = 0),
  `same_site` as string (default = "Lax"),
  `secure` as boolean (default=True)
  `http_only` as boolean (default = True)
   It is not a callable class
   '''

  __slots__ = ('value','max_age','cookie_str','same_site','secure','http_only')

  def __init__(
    self, 
    value:str,
    max_age:int=0, 
    same_site:str="Lax", 
    secure:bool=True, 
    http_only:bool=True):
    
    '''
    Args:
      value(str): The value of cookie.
      max_age(int): The max_age of the cookie. Defaults to zero.
      same_site(str): The value of the same_site attribute. Defaults to Lax. Find more about same_site in https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
      secure(bool): Is the cookie a secure cookie or not. Defaults to True
      http_only(bool): States if the cookie is HttpOnly cookie.
    '''
    self.value = value.encode()
    self.max_age = str(max_age).encode()
    self.same_site = same_site.encode()
    self.secure = secure
    self.http_only = http_only
    self.cookie_str = self.value + b'; Max-Age=' + self.max_age + b'; SameSite=' + same_site.encode()
    if secure == True:
      self.cookie_str += b'; Secure'
    if http_only == True:
      self.cookie_str += b'; HttpOnly'

