import os
import re
import uuid
import json
import ssl
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import certifi
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from markupsafe import Markup


def load_env_file(path=".env"):
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SUPABASE_URL"] = os.environ.get("SUPABASE_URL", "")
app.config["SUPABASE_KEY"] = (
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
    or os.environ.get("SUPABASE_ANON_KEY", "")
)
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
    if session.get("user"):
        return session["user"]

    username = session.get("username")
    if not username:
        return None

    return USERS.get(username)


def get_actor_key():
    if session.get("username"):
        return f"user:{session['username']}"

    session.setdefault("visitor_id", uuid.uuid4().hex)
    return f"visitor:{session['visitor_id']}"


def supabase_enabled():
    return bool(app.config["SUPABASE_URL"] and app.config["SUPABASE_KEY"])


def supabase_request(
    method,
    table,
    params=None,
    payload=None,
    prefer=None,
    bearer_token=None,
):
    query = f"?{urlencode(params or {}, doseq=True)}" if params else ""
    url = f"{app.config['SUPABASE_URL'].rstrip('/')}/rest/v1/{table}{query}"
    headers = {
        "apikey": app.config["SUPABASE_KEY"],
        "Authorization": f"Bearer {bearer_token or app.config['SUPABASE_KEY']}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer

    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request_object = Request(url, data=data, headers=headers, method=method)

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        with urlopen(request_object, timeout=10, context=ssl_context) as response:
            body = response.read().decode("utf-8")
    except HTTPError as error:
        details = error.read().decode("utf-8")
        raise RuntimeError(f"Supabase request failed: {error.code} {details}") from error
    except URLError as error:
        raise RuntimeError(f"Supabase request failed: {error.reason}") from error

    if not body:
        return None

    return json.loads(body)


def supabase_auth_user(access_token):
    url = f"{app.config['SUPABASE_URL'].rstrip('/')}/auth/v1/user"
    headers = {
        "apikey": app.config["SUPABASE_KEY"],
        "Authorization": f"Bearer {access_token}",
    }
    request_object = Request(url, headers=headers, method="GET")
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        with urlopen(request_object, timeout=10, context=ssl_context) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8")
        raise RuntimeError(f"Supabase auth failed: {error.code} {details}") from error
    except URLError as error:
        raise RuntimeError(f"Supabase auth failed: {error.reason}") from error


def build_github_oauth_url():
    redirect_to = url_for("auth_callback", _external=True)
    params = urlencode(
        {
            "provider": "github",
            "redirect_to": redirect_to,
        }
    )
    return f"{app.config['SUPABASE_URL'].rstrip('/')}/auth/v1/authorize?{params}"


def profile_from_auth_user(user):
    metadata = user.get("user_metadata") or {}
    username = (
        metadata.get("user_name")
        or metadata.get("preferred_username")
        or metadata.get("login")
        or user.get("email", "github_user").split("@")[0]
    )
    username = re.sub(r"[^a-zA-Z0-9_-]", "_", username).strip("_") or "github_user"

    return {
        "id": user["id"],
        "username": username[:39],
        "display_name": metadata.get("full_name") or metadata.get("name") or username,
        "github": metadata.get("user_name") or metadata.get("preferred_username") or username,
        "bio": "",
        "avatar_url": metadata.get("avatar_url") or metadata.get("picture"),
    }


def profile_from_row(row):
    return {
        "id": row["id"],
        "username": row["username"],
        "display_name": row.get("display_name") or row["username"],
        "github": row.get("github_username") or row["username"],
        "bio": row.get("bio") or "",
        "avatar_url": row.get("avatar_url"),
    }


def upsert_profile(profile, access_token):
    payload = {
        "id": profile["id"],
        "username": profile["username"],
        "display_name": profile["display_name"],
        "github_username": profile["github"],
        "bio": profile["bio"],
        "avatar_url": profile["avatar_url"],
    }
    rows = supabase_request(
        "POST",
        "profiles",
        {"on_conflict": "id"},
        payload=payload,
        prefer="resolution=merge-duplicates,return=representation",
        bearer_token=access_token,
    )
    return profile_from_row(rows[0]) if rows else profile


def fetch_profile(username):
    if not supabase_enabled():
        return USERS.get(username)

    rows = supabase_request(
        "GET",
        "profiles",
        {
            "select": "*",
            "username": f"eq.{username}",
            "limit": "1",
        },
    )
    if not rows:
        return None

    return profile_from_row(rows[0])


def map_comment_row(row):
    profile = row.get("profiles") or {}
    return {
        "id": row["id"],
        "author": row.get("anonymous_author") or profile.get("username") or "anonymous",
        "body": row["body"],
    }


def fetch_comments_for_post(post_id):
    if not supabase_enabled():
        return []

    rows = supabase_request(
        "GET",
        "comments",
        {
            "select": "id,anonymous_author,body,profiles(username)",
            "post_id": f"eq.{post_id}",
            "order": "created_at.asc",
        },
    )
    return [map_comment_row(row) for row in rows]


def map_post_row(row, include_comments=False):
    comments = (
        fetch_comments_for_post(row["id"])
        if include_comments
        else [None] * row.get("comments_count", 0)
    )

    profile = row.get("profiles") or {}
    return {
        "id": row["id"],
        "title": row["title"],
        "subcodeit": row["subcodeit"],
        "author": row.get("anonymous_author") or profile.get("username") or "anonymous",
        "type": row["post_type"],
        "comments": comments,
        "votes": row.get("votes_count", 0),
        "voted_by": set(),
        "tags": row.get("tags") or [],
        "body": row["body"],
        "code_filename": row.get("code_filename") or "",
        "code": row.get("code") or "",
        "repository_url": row.get("repository_url") or "",
    }


def list_posts(query="", subcodeit=None, author=None, author_id=None):
    if not supabase_enabled():
        posts = list(reversed(POSTS))
        if subcodeit:
            posts = [post for post in posts if post["subcodeit"] == subcodeit]
        if author:
            posts = [post for post in posts if post["author"] == author]
        return [post for post in posts if post_matches_query(post, query)]

    params = {
        "select": "*,profiles(username)",
        "order": "created_at.desc",
    }
    if subcodeit:
        params["subcodeit"] = f"eq.{subcodeit}"
    if author:
        params["anonymous_author"] = f"eq.{author}"
    if author_id:
        params["author_id"] = f"eq.{author_id}"

    rows = supabase_request("GET", "posts", params)
    posts = [map_post_row(row) for row in rows]
    return [post for post in posts if post_matches_query(post, query)]


def get_post(post_id):
    if not supabase_enabled():
        return find_memory_post(post_id)

    rows = supabase_request(
        "GET",
        "posts",
        {
            "select": "*,profiles(username)",
            "id": f"eq.{post_id}",
            "limit": "1",
        },
    )
    if not rows:
        return None

    return map_post_row(rows[0], include_comments=True)


def create_post_record(post_data):
    if not supabase_enabled():
        post_data["id"] = get_next_post_id()
        post_data["comments"] = []
        post_data["votes"] = 0
        post_data["voted_by"] = set()
        POSTS.append(post_data)
        return post_data

    row = {
        "title": post_data["title"],
        "subcodeit": post_data["subcodeit"],
        "anonymous_author": None if post_data.get("author_id") else post_data["author"],
        "author_id": post_data.get("author_id"),
        "post_type": post_data["type"],
        "body": post_data["body"],
        "code_filename": post_data["code_filename"] or None,
        "code": post_data["code"] or None,
        "repository_url": post_data["repository_url"] or None,
        "tags": post_data["tags"],
    }
    created_rows = supabase_request(
        "POST",
        "posts",
        payload=row,
        prefer="return=representation",
        bearer_token=session.get("access_token") if post_data.get("author_id") else None,
    )
    return map_post_row(created_rows[0])


def add_comment_record(post_id, author, body, author_id=None):
    if not supabase_enabled():
        selected_post = find_memory_post(post_id)
        if selected_post is None:
            return
        selected_post["comments"].append(
            {
                "id": get_next_comment_id(selected_post),
                "author": author,
                "body": body,
            }
        )
        return

    supabase_request(
        "POST",
        "comments",
        payload={
            "post_id": post_id,
            "author_id": author_id,
            "anonymous_author": None if author_id else author,
            "body": body,
        },
        prefer="return=minimal",
        bearer_token=session.get("access_token") if author_id else None,
    )


def count_votes_for_post(post_id):
    if not supabase_enabled():
        selected_post = find_memory_post(post_id)
        return selected_post["votes"] if selected_post else 0

    rows = supabase_request(
        "GET",
        "post_votes",
        {
            "select": "id",
            "post_id": f"eq.{post_id}",
        },
    )
    return len(rows)


def toggle_vote_record(post_id, actor_key):
    if not supabase_enabled():
        selected_post = find_memory_post(post_id)
        if selected_post is None:
            return 0
        if actor_key in selected_post["voted_by"]:
            selected_post["voted_by"].remove(actor_key)
            selected_post["votes"] -= 1
        else:
            selected_post["voted_by"].add(actor_key)
            selected_post["votes"] += 1
        return selected_post["votes"]

    existing_votes = supabase_request(
        "GET",
        "post_votes",
        {
            "select": "id",
            "post_id": f"eq.{post_id}",
            "anonymous_key": f"eq.{actor_key}",
            "limit": "1",
        },
    )
    if existing_votes:
        supabase_request(
            "DELETE",
            "post_votes",
            {"id": f"eq.{existing_votes[0]['id']}"},
            prefer="return=minimal",
        )
    else:
        supabase_request(
            "POST",
            "post_votes",
            payload={
                "post_id": post_id,
                "anonymous_key": actor_key,
            },
            prefer="return=minimal",
        )

    return count_votes_for_post(post_id)


def get_next_post_id():
    return max((post["id"] for post in POSTS), default=0) + 1


def get_next_comment_id(post):
    return max((comment.get("id", 0) for comment in post["comments"]), default=0) + 1


def normalize_subcodeit(value):
    cleaned = value.strip().lower().removeprefix("/code/")
    return cleaned.strip("/") or "general"


def find_memory_post(post_id):
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
    if not supabase_enabled():
        return list_posts(author=username)

    posts_by_id = {post["id"]: post for post in list_posts(author=username)}
    user = fetch_profile(username)
    if user:
        for post in list_posts(author_id=user["id"]):
            posts_by_id[post["id"]] = post

    return sorted(posts_by_id.values(), key=lambda post: post["id"], reverse=True)


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    posts = list_posts(query=query)

    if query.startswith("/code/"):
        subcodeit_name = normalize_subcodeit(query)
        return redirect(url_for("subcodeit", name=subcodeit_name))

    return render_template("index.html", posts=posts, query=query)


@app.route("/post/<int:post_id>")
def post(post_id):
    selected_post = get_post(post_id)
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
        new_post = create_post_record({
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
            "author_id": current_user.get("id") if current_user else None,
        })

        return redirect(url_for("post", post_id=new_post["id"]))

    return render_template("create_post.html", form_data={})


@app.route("/code/<name>")
def subcodeit(name):
    normalized_name = normalize_subcodeit(name)
    query = request.args.get("q", "").strip()
    posts = list_posts(query=query, subcodeit=normalized_name)

    return render_template(
        "subcodeit.html",
        name=normalized_name,
        posts=posts,
        query=query,
    )


@app.route("/post/<int:post_id>/upvote", methods=["POST"])
def upvote_post(post_id):
    selected_post = get_post(post_id)
    if selected_post is None:
        abort(404)

    votes = toggle_vote_record(post_id, get_actor_key())

    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"post_id": post_id, "votes": votes})

    return redirect(request.referrer or url_for("post", post_id=post_id))


@app.route("/post/<int:post_id>/comment", methods=["POST"])
def comment_post(post_id):
    selected_post = get_post(post_id)
    if selected_post is None:
        abort(404)

    body = request.form.get("body", "").strip()
    if not body:
        return redirect(url_for("post", post_id=post_id))

    current_user = get_current_user()
    add_comment_record(
        post_id,
        current_user["username"] if current_user else "anonymous",
        body,
        author_id=current_user.get("id") if current_user else None,
    )

    return redirect(url_for("post", post_id=post_id))


@app.route("/login")
def login():
    if get_current_user():
        return redirect(url_for("profile_me"))

    return render_template("login.html")


@app.route("/auth/github", methods=["GET", "POST"])
def github_login():
    if not supabase_enabled():
        return render_template(
            "login.html",
            error="Supabase is not configured yet.",
        ), 503

    return redirect(build_github_oauth_url())


@app.route("/auth/callback")
def auth_callback():
    return render_template("auth_callback.html")


@app.route("/auth/session", methods=["POST"])
def auth_session():
    if not supabase_enabled():
        return jsonify({"error": "Supabase is not configured."}), 503

    data = request.get_json(silent=True) or {}
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    if not access_token:
        return jsonify({"error": "Missing Supabase access token."}), 400

    try:
        auth_user = supabase_auth_user(access_token)
        profile = upsert_profile(profile_from_auth_user(auth_user), access_token)
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 502

    session["user"] = profile
    session["username"] = profile["username"]
    session["access_token"] = access_token
    if refresh_token:
        session["refresh_token"] = refresh_token

    return jsonify({"redirect": url_for("profile_me")})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("user", None)
    session.pop("access_token", None)
    session.pop("refresh_token", None)

    return redirect(url_for("index"))


@app.route("/me")
def profile_me():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("login"))

    return redirect(url_for("profile", username=current_user["username"]))


@app.route("/u/<username>")
def profile(username):
    user = fetch_profile(username) if supabase_enabled() else USERS.get(username)
    if user is None:
        user = {
            "username": username,
            "display_name": username,
            "github": username,
            "bio": "CodeIT user.",
            "avatar_url": None,
        }

    return render_template("profile.html", user=user, posts=get_user_posts(username))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
