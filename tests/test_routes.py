import pytest
from main import app

# https://sanic.dev/en/plugins/sanic-testing/getting-started.html


@pytest.yield_fixture
def sanic_app():
    yield app


@pytest.mark.asyncio
async def test_get_contact_returns_200(sanic_app):
    request, response = await sanic_app.asgi_client.get('/contacts')
    assert request.method.lower() == "get"
    assert response.status == 200
    #assert len(response.json) == 2


@pytest.mark.asyncio
async def test_get_contact_1_returns_404(sanic_app):
    request, response = await sanic_app.asgi_client.get('/1')
    assert request.method.lower() == "get"
    assert response.status == 404
