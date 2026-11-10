
import pytest

from app import create_app, db
from app.models import Task

@pytest.fixture
def client():

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()

def test_home_page(client):

    response = client.get("/")

    assert response.status_code == 200

    assert b"Python DevOps Task Manager" in response.data

def test_health_endpoint(client):

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json["status"] == "healthy"

def test_add_task(client):

    response = client.post(
        "/add",
        data={"title": "Learn GitHub Actions"}
    )

    assert response.status_code == 302

    with client.application.app_context():

        task = Task.query.first()

        assert task is not None

        assert task.title == "Learn GitHub Actions"

def test_empty_task(client):

    response = client.post(
        "/add",
        data={"title": "   "}
    )

    assert response.status_code == 400

def test_complete_task(client):

    client.post(
        "/add",
        data={"title": "Learn Docker"}
    )

    with client.application.app_context():

        task = Task.query.first()
        task_id = task.id

    response = client.post(
        f"/complete/{task_id}"
    )

    assert response.status_code == 302

    with client.application.app_context():

        task = db.session.get(Task, task_id)

        assert task.completed is True

def test_delete_task(client):

    client.post(
        "/add",
        data={"title": "Learn AWS"}
    )

    with client.application.app_context():

        task = Task.query.first()
        task_id = task.id

    response = client.post(
        f"/delete/{task_id}"
    )

    assert response.status_code == 302

    with client.application.app_context():

        task = db.session.get(Task, task_id)

        assert task is None