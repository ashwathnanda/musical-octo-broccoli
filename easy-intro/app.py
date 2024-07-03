from pathlib import Path

from dotenv import load_dotenv
from litestar import Litestar, get
from litestar.exceptions import InternalServerException
from litestar.static_files import create_static_files_router
from openai import RateLimitError

from easy_intro import ice_break_with
from exception_handler import app_exception_handler, router_handler_exception_handler

load_dotenv()

HTML_DIR = Path("templates")


def on_startup() -> None:
    HTML_DIR.mkdir(exist_ok=True)
    HTML_DIR.joinpath("404.html").write_text("<h1>Not found</h1>")


@get("/profile-summary", sync_to_thread=False, exception_handlers={RateLimitError: router_handler_exception_handler})
def profile_summary(user_name: str) -> dict[str, str]:
    try:
        summary, profile_url = ice_break_with(user_name)
        return {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_url,
        }
    except Exception as e:
        raise e


app = Litestar(route_handlers=[
    profile_summary,
    create_static_files_router(
            path="/",
            directories=["templates"],
            html_mode=True)
    ],
    exception_handlers={InternalServerException: app_exception_handler},
    debug=True)
