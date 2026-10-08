from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from .redaction import redact_structure
from .scope import CompanyScope


@dataclass(frozen=True)
class EventRecord:
    event_id: UUID
    stream_seq: int


def lock_event_stream(session: Session, scope: CompanyScope) -> None:
    session.execute(
        text(
            """INSERT INTO event_stream_counters(environment_id, company_id, last_seq)
               VALUES (:environment_id, :company_id, 0)
               ON CONFLICT (environment_id, company_id) DO NOTHING"""
        ),
        {"environment_id": scope.environment_id, "company_id": scope.company_id},
    )
    session.execute(
        text(
            """SELECT last_seq FROM event_stream_counters
               WHERE environment_id=:environment_id AND company_id=:company_id FOR UPDATE"""
        ),
        {"environment_id": scope.environment_id, "company_id": scope.company_id},
    ).scalar_one()


def append_event(
    session: Session,
    *,
    scope: CompanyScope,
    event_type: str,
    task_id: UUID | None,
    run_id: UUID | None,
    correlation_id: UUID,
    parent_event_id: UUID | None,
    source: str,
    actor: dict[str, object],
    sensitivity: str,
    payload: dict[str, object],
    evidence_refs: list[dict[str, object]],
    dedup_key: str,
    event_id: UUID | None = None,
    occurred_at: datetime | None = None,
) -> EventRecord:
    lock_event_stream(session, scope)
    seq = session.execute(
        text(
            """UPDATE event_stream_counters SET last_seq = last_seq + 1
               WHERE environment_id = :environment_id AND company_id = :company_id
               RETURNING last_seq"""
        ),
        {"environment_id": scope.environment_id, "company_id": scope.company_id},
    ).scalar_one()

    event_id = event_id or uuid4()
    occurred_at = occurred_at or datetime.now(UTC)
    session.execute(
        text(
            """INSERT INTO events(
                event_id, environment_id, company_id, schema_version, event_type, stream_seq,
                occurred_at, recorded_at, task_id, run_id, agent_id, employee_version_id,
                correlation_id, parent_event_id, source, actor, sensitivity, payload,
                evidence_refs, dedup_key
            ) VALUES (
                :event_id, :environment_id, :company_id, 1, :event_type, :stream_seq,
                :occurred_at, CURRENT_TIMESTAMP, :task_id, :run_id, NULL, NULL,
                :correlation_id, :parent_event_id, :source, CAST(:actor AS jsonb), :sensitivity,
                CAST(:payload AS jsonb), CAST(:evidence_refs AS jsonb), :dedup_key
            )"""
        ),
        {
            "event_id": event_id,
            "environment_id": scope.environment_id,
            "company_id": scope.company_id,
            "event_type": event_type,
            "stream_seq": seq,
            "occurred_at": occurred_at,
            "task_id": task_id,
            "run_id": run_id,
            "correlation_id": correlation_id,
            "parent_event_id": parent_event_id,
            "source": source,
            "actor": json.dumps(redact_structure(actor)),
            "sensitivity": sensitivity,
            "payload": json.dumps(redact_structure(payload)),
            "evidence_refs": json.dumps(redact_structure(evidence_refs)),
            "dedup_key": dedup_key,
        },
    )
    session.execute(
        text(
            """INSERT INTO outbox_events(
                id, event_id, environment_id, company_id, topic, status, available_at, attempts
            ) VALUES (:id, :event_id, :environment_id, :company_id, :topic, 'pending', CURRENT_TIMESTAMP, 0)"""
        ),
        {
            "id": uuid4(),
            "event_id": event_id,
            "environment_id": scope.environment_id,
            "company_id": scope.company_id,
            "topic": event_type.lower(),
        },
    )
    return EventRecord(event_id=event_id, stream_seq=seq)
