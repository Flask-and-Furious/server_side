
import pytest

from app import app

@pytest.fixture
def api():
    return app.test_client()


@pytest.fixture
def myapp():
    myapp = app()
    myapp.config.from_object('project.config.TestingConfig')
    return myapp


