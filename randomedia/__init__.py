import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template
from random import randint

load_dotenv('.env')


def _join_path(*parts):
    return "/".join(str(part).strip("/") for part in parts if part and str(part).strip("/"))


def _build_url(env_name, path=""):
    base_url = os.getenv(env_name)
    if not base_url:
        raise RuntimeError(f"{env_name} is not configured")
    base_url = base_url.rstrip("/")
    path = path.strip("/")
    return f"{base_url}/{path}" if path else f"{base_url}/"


def _media_root():
    return os.getenv("MEDIA_ROOT", "").strip("/")


def _category_path(category):
    media_root = _media_root()
    category = category.strip("/")
    if media_root and (category == media_root or category.startswith(f"{media_root}/")):
        return category
    return _join_path(media_root, category)


def _api_listing(path):
    response = requests.get(_build_url("API_ROOT_URL", path) + "?ls", timeout=1)
    response.raise_for_status()
    return response.json()


def _nav_categories(directories):
    return [
        {
            "name": directory["href"].strip("/").rsplit("/", 1)[-1],
            "path": _category_path(directory["href"]),
        }
        for directory in directories
    ]


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def render_category(category_path):
        categories = _nav_categories(_api_listing(_media_root()).get("dirs", []))
        media = _api_listing(category_path)
        files = media.get("files", [])

        media_type = None
        media_url = None
        if files:
            selected_media = files[randint(0, len(files) - 1)]
            media_type = (
                "image"
                if selected_media.get("ext", "").lower()
                in ["jpg", "jpeg", "png", "webp", "gif"]
                else "video"
            )
            file_path = _join_path(category_path, selected_media["href"])
            media_url = _build_url("FILE_ROOT_URL", file_path)

        return render_template(
            "home.html",
            categories=categories,
            active_category=category_path,
            media_type=media_type,
            media_url=media_url,
        )

    @app.route("/")
    def index():
        default_category = os.getenv("MEDIA_DEFAULT_CATEGORY")
        if not default_category:
            raise RuntimeError("MEDIA_DEFAULT_CATEGORY is not configured")
        return render_category(_category_path(default_category))

    @app.route("/<path:category>/")
    def from_category(category):
        return render_category(_category_path(category))

    return app
