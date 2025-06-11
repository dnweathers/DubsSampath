import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.main import app
from app.db.database import Base, engine, SessionLocal

# Ensure tables are created for testing
@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

def make_payload(sample_id=None):
    return {
        "sample_id": sample_id or f"SAMP-{uuid4().hex[:8]}",
        "source": "patient-x",
        "type": "blood",
        "status": "pending",
        "date_collected": datetime.now(timezone.utc).isoformat()
    }

@pytest.mark.asyncio
async def test_create_sample(client):
    payload = make_payload("SAMP-001")
    response = await client.post("/samples/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["sample_id"] == payload["sample_id"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_all_samples(client):
    response = await client.get("/samples/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_sample_by_id(client):
    payload = make_payload()
    post_resp = await client.post("/samples/", json=payload)
    sample_id = post_resp.json()["id"]

    get_resp = await client.get(f"/samples/{sample_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == sample_id

@pytest.mark.asyncio
async def test_update_sample(client):
    payload = make_payload()
    post_resp = await client.post("/samples/", json=payload)
    sample_id = post_resp.json()["id"]

    update_data = {
        "sample_id": payload["sample_id"],  # keep same sample_id
        "source": "updated-source",
        "type": "blood",
        "status": "in-progress",
        "date_collected": datetime.now(timezone.utc).isoformat()
    }

    put_resp = await client.put(f"/samples/{sample_id}", json=update_data)
    assert put_resp.status_code == 200
    assert put_resp.json()["status"] == "in-progress"
    assert put_resp.json()["source"] == "updated-source"

@pytest.mark.asyncio
async def test_delete_sample(client):
    payload = make_payload()
    post_resp = await client.post("/samples/", json=payload)
    sample_id = post_resp.json()["id"]

    delete_resp = await client.delete(f"/samples/{sample_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/samples/{sample_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_get_nonexistent_sample(client):
    random_id = uuid4()
    response = await client.get(f"/samples/{random_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_sample_invalid_status(client):
    payload = make_payload("SAMP-002")
    invalid_payload = {**payload, "status": "frozen"}  # invalid status

    response = await client.post("/samples/", json=invalid_payload)
    assert response.status_code == 422