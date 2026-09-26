from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ClientRecord(Base):
    __tablename__ = "clients"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    external_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)


class AgentRunRecord(Base):
    __tablename__ = "agent_runs"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    client_id: Mapped[str | None] = mapped_column(
        ForeignKey("clients.id"), nullable=True)
    user_request: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30))
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)


class AgentActionRecord(Base):
    __tablename__ = "agent_actions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("agent_runs.id"))
    tool: Mapped[str] = mapped_column(String(80))
    action: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(30))
    result_summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)


class AuditLogRecord(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("agent_runs.id"))
    event_type: Mapped[str] = mapped_column(String(80))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
