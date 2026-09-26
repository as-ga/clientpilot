from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app.db.database import Base, build_engine, create_session_factory
from app.db.models import (
    AgentActionRecord,
    AgentRunRecord,
    ClientRecord,
)


class Repository:
    def __init__(self) -> None:
        self.session_factory = None
        try:
            engine = build_engine()
            Base.metadata.create_all(engine)
            self.session_factory = create_session_factory()
        except SQLAlchemyError:
            self.session_factory = None

    def record_run(self, run_id: str, request: str, client_name: str | None, status: str) -> None:
        if self.session_factory is None:
            return
        try:
            with self.session_factory.begin() as session:
                client_id = None
                if client_name:
                    client_id = client_name.lower().replace(" ", "-")
                    session.merge(ClientRecord(id=client_id, name=client_name))
                session.merge(AgentRunRecord(
                    id=run_id, client_id=client_id, user_request=request, status=status))
        except SQLAlchemyError:
            return

    def complete_run(self, run_id: str, status: str, actions: list[dict]) -> None:
        if self.session_factory is None:
            return
        try:
            with self.session_factory.begin() as session:
                run = session.get(AgentRunRecord, run_id)
                if run:
                    run.status = status
                    run.completed_at = datetime.utcnow()
                for action in actions:
                    session.add(AgentActionRecord(run_id=run_id, tool=action["tool"], action=action["action"], status=action["status"], result_summary=str(
                        action.get("result_summary", action.get("result", "")))))
        except SQLAlchemyError:
            return
