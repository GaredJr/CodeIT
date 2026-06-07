import os
import re
import uuid
from html import escape
from urllib.parse import urlparse

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from markupsafe import Markup

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SUPABASE_URL"] = os.environ.get("SUPABASE_URL", "")
app.config["SUPABASE_ANON_KEY"] = os.environ.get("SUPABASE_ANON_KEY", "")
app.config["ASSET_VERSION"] = "2026-06-07-3"


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
                "id": 1,
                "author": "devuser",
                "body": "You can debounce the query before calling the API.",
            }
        ],
        "votes": 82,
        "voted_by": set(),
        "tags": ["react", "typescript", "frontend"],
        "body": "I have a search input that calls the API every time I type. What is the cleanest debounce pattern here?",
        "code_filename": "App.tsx",
        "code": """const [query, setQuery] = useState("");

useEffect(() => {
    fetch(`/api/search?q=${query}`);
}, [query]);""",
        "repository_url": "https://github.com/facebook/react",
    },
    {
        "id": 2,
        "title": "Simple Lua inventory system",
        "subcodeit": "roblox",
        "author": "dev_user",
        "type": "Snippet",
        "comments": [],
        "votes": 41,
        "voted_by": set(),
        "tags": ["lua", "roblox", "datastore"],
        "body": "A small inventory pattern for Roblox projects.",
        "code_filename": "inventory.lua",
        "code": """local inventory = {}

function inventory:add(item)
    table.insert(self, item)
end""",
        "repository_url": "",
    },
]

USERS = {
    "gard": {
        "username": "gard",
        "display_name": "Gard",
        "github": "gard",
        "bio": "Building CodeIT.",
    },
    "dev_user": {
        "username": "dev_user",
        "display_name": "Dev User",
        "github": "dev-user",
        "bio": "Sharing small code patterns.",
    },
}


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


@app.template_filter("github_repo_name")
def github_repo_name(repository_url):
    parsed = urlparse(repository_url)
    path_parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(path_parts) >= 2:
        return f"{path_parts[0]}/{path_parts[1].removesuffix('.git')}"

    return repository_url


@app.context_processor
def inject_current_user():
    return {"current_user": get_current_user()}


def get_current_user():
    username = session.get("username")
    if not username:
        return None

    return USERS.get(username)


def get_actor_key():
    if session.get("username"):
        return f"user:{session['username']}"

    session.setdefault("visitor_id", uuid.uuid4().hex)
    return f"visitor:{session['visitor_id']}"


def get_next_post_id():
    return max((post["id"] for post in POSTS), default=0) + 1


def get_next_comment_id(post):
    return max((comment.get("id", 0) for comment in post["comments"]), default=0) + 1


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


def normalize_github_repository_url(value):
    repository_url = value.strip()
    if not repository_url:
        return "", None

    if not repository_url.startswith(("http://", "https://")):
        repository_url = f"https://{repository_url}"

    parsed = urlparse(repository_url)
    hostname = parsed.netloc.lower()
    path_parts = [part for part in parsed.path.strip("/").split("/") if part]

    if hostname != "github.com" or len(path_parts) < 2:
        return "", "Repository link must be a GitHub repository URL."

    owner = path_parts[0]
    repo = path_parts[1].removesuffix(".git")

    return f"https://github.com/{owner}/{repo}", None


def post_matches_query(post, query):
    if not query:
        return True

    haystack = " ".join(
        [
            post["title"],
            post["body"],
            post["subcodeit"],
            post["author"],
            post["type"],
            post.get("code", ""),
            post.get("repository_url", ""),
            " ".join(post["tags"]),
        ]
    ).lower()
    return query.lower() in haystack


def get_user_posts(username):
    return [post for post in reversed(POSTS) if post["author"] == username]


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    posts = [post for post in reversed(POSTS) if post_matches_query(post, query)]

    return render_template("index.html", posts=posts, query=query)


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

        repository_url, repository_error = normalize_github_repository_url(
            request.form.get("repository_url", "")
        )
        if repository_error:
            return render_template(
                "create_post.html",
                error=repository_error,
                form_data=request.form,
            ), 400

        current_user = get_current_user()
        new_post = {
            "id": get_next_post_id(),
            "title": title,
            "subcodeit": normalize_subcodeit(request.form.get("subcodeit", "")),
            "author": (
                current_user["username"]
                if current_user
                else request.form.get("author", "").strip() or "anonymous"
            ),
            "type": request.form.get("post_type", "Discussion"),
            "comments": [],
            "votes": 0,
            "voted_by": set(),
            "tags": parse_tags(request.form.get("tags", "")),
            "body": body,
            "code_filename": request.form.get("code_filename", "").strip(),
            "code": request.form.get("code", "").strip(),
            "repository_url": repository_url,
        }
        POSTS.append(new_post)

        return redirect(url_for("post", post_id=new_post["id"]))

    return render_template("create_post.html", form_data={})


@app.route("/code/<name>")
def subcodeit(name):
    normalized_name = normalize_subcodeit(name)
    query = request.args.get("q", "").strip()
    posts = [
        post
        for post in reversed(POSTS)
        if post["subcodeit"] == normalized_name and post_matches_query(post, query)
    ]

    return render_template(
        "subcodeit.html",
        name=normalized_name,
        posts=posts,
        query=query,
    )


@app.route("/post/<int:post_id>/upvote", methods=["POST"])
def upvote_post(post_id):
    selected_post = find_post(post_id)
    if selected_post is None:
        abort(404)

    actor_key = get_actor_key()
    if actor_key in selected_post["voted_by"]:
        selected_post["voted_by"].remove(actor_key)
        selected_post["votes"] -= 1
    else:
        selected_post["voted_by"].add(actor_key)
        selected_post["votes"] += 1

    return redirect(request.referrer or url_for("post", post_id=post_id))


@app.route("/post/<int:post_id>/comment", methods=["POST"])
def comment_post(post_id):
    selected_post = find_post(post_id)
    if selected_post is None:
        abort(404)

    body = request.form.get("body", "").strip()
    if not body:
        return redirect(url_for("post", post_id=post_id))

    current_user = get_current_user()
    selected_post["comments"].append(
        {
            "id": get_next_comment_id(selected_post),
            "author": current_user["username"] if current_user else "anonymous",
            "body": body,
        }
    )

    return redirect(url_for("post", post_id=post_id))


@app.route("/login")
def login():
    if get_current_user():
        return redirect(url_for("profile_me"))

    return render_template("login.html")


@app.route("/auth/github", methods=["POST"])
def github_login():
    username = "gard"
    USERS.setdefault(
        username,
        {
            "username": username,
            "display_name": "Gard",
            "github": "gard",
            "bio": "Building CodeIT.",
        },
    )
    session["username"] = username

    return redirect(url_for("profile_me"))


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    return redirect(url_for("index"))


@app.route("/me")
def profile_me():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("login"))

    return redirect(url_for("profile", username=current_user["username"]))


@app.route("/u/<username>")
def profile(username):
    user = USERS.get(username)
    if user is None:
        user = {
            "username": username,
            "display_name": username,
            "github": username,
            "bio": "CodeIT user.",
        }

    return render_template("profile.html", user=user, posts=get_user_posts(username))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
