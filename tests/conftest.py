import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
from main import app
from database import get_session
from auth.models import User
from auth.utils import get_password_hash, create_url_safe_token


AUTH_PREFIX = "/auth"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="signup_user")
def signup_user_fixture(session: Session):
    user = User(
        username="username",
        password=get_password_hash("password"),
        email="email@example.com",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="signin_user")
def signin_user_fixture(client: TestClient, signup_user: User):
    request_data = {"username": "username", "password": "password"}
    response = client.post(f"{AUTH_PREFIX}/signin", json=request_data)
    return response.json()


@pytest.fixture(name="url_safe_token")
def url_safe_token_fixture(signup_user: User):
    data = {"email": signup_user.email}
    return create_url_safe_token(data)
