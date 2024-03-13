from emmett import App

app = App(__name__)


@app.route("/")
async def hello():
    return "Hello world!"
