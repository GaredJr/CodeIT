from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    posts = [
        {
            "title": "How do I debounce this React input?",
            "subcodeit": "/code/react",
            "author": "gard",
            "type": "Question",
            "comments": 24,
            "votes": 82,
            "tags": ["react", "typescript", "frontend"],
        },
        {
            "title": "Simple Lua inventory system",
            "subcodeit": "/code/roblox",
            "author": "dev_user",
            "type": "Snippet",
            "comments": 8,
            "votes": 41,
            "tags": ["lua", "roblox", "datastore"],
        },
    ]

    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def post(post_id):
    return render_template("post.html", post_id=post_id)


@app.route("/create")
def create_post():
    return render_template("create_post.html")


@app.route("/code/<name>")
def subcodeit(name):
    return render_template("subcodeit.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)