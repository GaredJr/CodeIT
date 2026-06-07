import os
import re
from html import escape

from flask import Flask, abort, redirect, render_template, request, url_for
from markupsafe import Markup

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SUPABASE_URL"] = os.environ.get("SUPABASE_URL", "")
app.config["SUPABASE_ANON_KEY"] = os.environ.get("SUPABASE_ANON_KEY", "")
app.config["ASSET_VERSION"] = "2026-06-07-2"


TOKEN_RE = re.compile(
    r"(?P<comment>//[^\n]*|--[^\n]*|#[^\n]*)"
    r"|(?P<string>`[^`]*`|'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")"
    r"|(?P<number>\b\d+(?:\.\d+)?\b)"
    r"|(?P<function>\b[A-Za-z_$][\w$]*(?=\s*\())"
    r"|(?P<property>(?<=\.)[A-Za-z_$][\w$]*)"
    r"|(?P<keyword>\b(?:async|await|break|class|const|def|else|end|export|fetch|for|from|function|if|import|in|let|local|return|self|table|then|useEffect|useState|while)\b)"
    r"|(?P<identifier>\b[A-Za-z_$][\w$]*\b)"
    r"|(?P<operator>[{}()[\].,;:=+\-*/<>])"
)


POSTS = [
    {
        "id": 1,
        "title": "How do I debounce this React input?",
        "subcodeit": "react",
        "author": "gard",
        "type": "Question",
        "comments": [
            {
                "author": "devuser",
                "body": "You can debounce the query before calling the API.",
            }
        ],
        "votes": 82,
        "tags": ["react", "typescript", "frontend"],
        "body": "I have a search input that calls the API every time I type. What is the cleanest debounce pattern here?",
        "code_filename": "App.tsx",
        "code": """const [query, setQuery] = useState("");

useEffect(() => {
    fetch(`/api/search?q=${query}`);
}, [query]);""",
    },
    {
        "id": 2,
        "title": "Simple Lua inventory system",
        "subcodeit": "roblox",
        "author": "dev_user",
        "type": "Snippet",
        "comments": [],
        "votes": 41,
        "tags": ["lua", "roblox", "datastore"],
        "body": "A small inventory pattern for Roblox projects.",
        "code_filename": "inventory.lua",
        "code": """local inventory = {}

function inventory:add(item)
    table.insert(self, item)
end""",
    },
]


@app.template_filter("highlight_code")
def highlight_code(code):
    highlighted = []
    position = 0

    for match in TOKEN_RE.finditer(code):
        highlighted.append(escape(code[position:match.start()]))
        token_type = match.lastgroup
        token = escape(match.group())
        highlighted.append(f'<span class="tok-{token_type}">{token}</span>')
        position = match.end()

    highlighted.append(escape(code[position:]))
    return Markup("".join(highlighted))


def get_next_post_id():
    return max((post["id"] for post in POSTS), default=0) + 1


def normalize_subcodeit(value):
    cleaned = value.strip().lower().removeprefix("/code/")
    return cleaned.strip("/") or "general"


def find_post(post_id):
    return next((post for post in POSTS if post["id"] == post_id), None)


def parse_tags(value):
    return [
        tag.strip().removeprefix("#").lower()
        for tag in value.split(",")
        if tag.strip()
    ]


@app.route("/")
def index():
    return render_template("index.html", posts=list(reversed(POSTS)))


@app.route("/post/<int:post_id>")
def post(post_id):
    selected_post = find_post(post_id)
    if selected_post is None:
        abort(404)

    return render_template("post.html", post=selected_post)


@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()

        if not title or not body:
            return render_template(
                "create_post.html",
                error="Title and body are required.",
                form_data=request.form,
            ), 400

        new_post = {
            "id": get_next_post_id(),
            "title": title,
            "subcodeit": normalize_subcodeit(request.form.get("subcodeit", "")),
            "author": request.form.get("author", "").strip() or "anonymous",
            "type": request.form.get("post_type", "Discussion"),
            "comments": [],
            "votes": 0,
            "tags": parse_tags(request.form.get("tags", "")),
            "body": body,
            "code_filename": request.form.get("code_filename", "").strip(),
            "code": request.form.get("code", "").strip(),
        }
        POSTS.append(new_post)

        return redirect(url_for("post", post_id=new_post["id"]))

    return render_template("create_post.html", form_data={})


@app.route("/code/<name>")
def subcodeit(name):
    normalized_name = normalize_subcodeit(name)
    posts = [post for post in reversed(POSTS) if post["subcodeit"] == normalized_name]

    return render_template("subcodeit.html", name=normalized_name, posts=posts)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
