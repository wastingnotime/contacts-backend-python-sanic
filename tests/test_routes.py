import pytest
from main import app


# https://sanic.readthedocs.io/en/latest/sanic/testing.html
# https://stackoverflow.com/questions/56594314/asynchronously-unit-testing-a-sanic-app-throws-runtimeerror-this-event-loop-is

@pytest.yield_fixture
def sanic_app():
    yield app


@pytest.fixture
def test_cli(loop, sanic_app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def test_get_contact_returns_200(test_cli):
    resp = await test_cli.get('/')
    assert resp.status == 200
    json = await resp.json()
    assert len(json) == 2


async def test_get_contact_1_returns_404(test_cli):
    resp = await test_cli.get('/1')
    assert resp.status == 404
