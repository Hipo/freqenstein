from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler
from tornado_smack import App, render_template
from tornado_smack.app import handler, DebuggableHandler
from tornado.stack_context import StackContext, wrap

app = App()

@app.route("/foobar", methods=['POST'])
def foobar():
    return "hello world"

@app.route("/foobar/<id>")
def foobar2(id):
    return "hello world %s" % id

@app.route("/othertemplate")
def sometemplate(self):
    self.render("example.html", students=[{'name': 'a'}], title="hello")

@app.route("/template")
def someothertemplate():
    return render_template("example.html", students=[{'name': 'a'}], title="hello")

class MyBaseHandler(RequestHandler):
    foo = "bar"

@app.route('/exc', handler_bases=(MyBaseHandler,))
def exc(handler):
    """
    if you set a base class for your ExcHandler, in debug mode we'll add DebuggableHandler in between
    handler.__class__.__mro__
    (<class 'tornado_smack.app.ExcHandler'>, <class 'tornado_smack.app.DebuggableHandler'>, <class '__main__.MyBaseHandler'>, <class 'tornado.web.RequestHandler'>, <type 'object'>)
    """
    print ">>>", handler.foo
    raise Exception('foo')

@app.route('/foo/<id>')
def foo(id):
    if str(id)=='3':
        raise Exception('- 3 -')
    handler.write("foo - %s" % id)

@app.route('/async', methods=['GET', 'HEAD'])
@coroutine
def homepage(self):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch("https://google.com/")
    self.write(response.body)

if __name__ == "__main__":
    app.run(debug=True)