from fastapi import APIRouter

from app.schemas.client import Client

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.get("", response_model=list[Client])
def list_clients() -> list[Client]:
    return [Client(id="acme-corp", name="Acme Corp", external_id="acme-demo", health="needs_attention")]


@router.get("/{client_id}", response_model=Client)
def get_client(client_id: str) -> Client:
    return Client(id=client_id, name="Acme Corp", external_id="acme-demo", health="needs_attention")
