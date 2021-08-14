import typing
import inspect
from . import structure


class Router:
  '''Router class has the Methods, paths, and handlers.'''
  def __init__(self):
    self.routes = dict()
    self.routes["GET"] = {}
    self.routes["POST"] = {}
    self.routes["PUT"] = {}
    self.routes["FETCH"] = {}
    self.routes["HEAD"] = {}
    self.routes["PATCH"] = {}
    self.routes["CONNECT"] = {}
    self.routes["OPTIONS"] = {}
    self.routes["TRACE"] = {}

  def add_route(self,path:str,method:str,handler:typing.Callable) -> None:
    self.routes[method][path] = handler
  
  def add_method(self,method:str):
    '''This should be used to adding HTTP methods to the routing dictionary '''
    #self.routes[method] = {}
    raise NotImplementedError

  def get(self,path:str,**opts) -> typing.Callable:
    """
    This is meant to be used as a decorator on a function, that will be executed on a get query to the path.
    Eg: 
    
    @router.get('/'):
    def landing():
        return "Index page"
    """
    def decorator(handler: typing.Callable) -> typing.Callable:
      self.add_route(path=path,method="GET",handler=handler)
      return handler
    return decorator
  
  def post(self,path:str,**opts)-> typing.Callable:
    """
    This is meant to be used as a decorator on a function, that will be executed on a post query to the path.
    Eg: 
    
    @router.post('/form'):
    def landing(req,res):
        form = req.body
        ...
        res.send("OK! Form submitted") 
    """
    def decorator(handler: typing.Callable) -> typing.Callable:
      self.add_route(path=path,method="POST",handler=handler)
      return handler
    return decorator

  async def handle(self,request,response):
    try:
      if request.method == "HEAD":
        response_ = await self.routes["GET"][request.path](request,response)
      else:
        response_ = await self.routes[request.method][request.path](request,response)
      return response_
    except KeyError:
      resp = structure.Response404()
      return resp
    #Value: Response object(9/8/21).


