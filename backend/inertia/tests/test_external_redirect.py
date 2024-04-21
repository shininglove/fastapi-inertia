from fastapi import FastAPI, Depends, Response
from typing import Annotated

from starlette.testclient import TestClient

from ..inertia import (
    Inertia,
    inertia_dependency_factory,
)

from ..config import InertiaConfig
from ..exceptions import InertiaVersionConflictException, inertia_exception_handler


app = FastAPI()
app.add_exception_handler(InertiaVersionConflictException, inertia_exception_handler)  # type: ignore[arg-type]

InertiaDep = Annotated[Inertia, Depends(inertia_dependency_factory(InertiaConfig()))]

PROPS = {
    "message": "hello from index",
}

COMPONENT = "IndexPage"

EXTERNAL_URL = "https://some-external-url.com/"


@app.get("/", response_model=None)
async def index(inertia: InertiaDep) -> Response:
    return inertia.location(EXTERNAL_URL)


def test_returns_409_with_appropriate_inertia_location() -> None:
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 409
        assert response.headers.get("X-Inertia-Location") == EXTERNAL_URL
