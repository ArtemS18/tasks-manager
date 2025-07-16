"""INSERT IN BD

Revision ID: 099ba7cdae79
Revises: 4db33ad8c88d
Create Date: 2025-07-12 21:03:05.255809

"""

from datetime import datetime
import hashlib
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.auth.controllers.password import hash_password


# revision identifiers, used by Alembic.
revision: str = "099ba7cdae79"
down_revision: Union[str, None] = "4db33ad8c88d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    now = datetime.utcnow()

    # === USERS ===
    users = [
        {
            "id": i,
            "tg_id": 100000000 + i,
            "name": f"User {i}",
            "login": f"user{i}",
            "status": "active",
            "hashed_password": hash_password("123456789"),
        }
        for i in range(1, 6)
    ]
    conn.execute(
        sa.text("""
            INSERT INTO users (id, tg_id, name, login, status, hashed_password)
            VALUES (:id, :tg_id, :name, :login, :status, :hashed_password)
        """),
        users,
    )

    # === PROJECTS ===
    projects = [
        {
            "id": i,
            "name": f"Project {i}",
            "owner_id": i,
            "created_at": now,
        }
        for i in range(1, 6)
    ]
    conn.execute(
        sa.text("""
            INSERT INTO projects (id, name, owner_id, created_at)
            VALUES (:id, :name, :owner_id, :created_at)
        """),
        projects,
    )

    # === MEMBERS ===
    members = [
        {
            "id": i,
            "user_id": i,
            "project_id": i,
            "role": "owner",
            "status": "active",
            "created_at": now,
        }
        for i in range(1, 6)
    ]
    conn.execute(
        sa.text("""
            INSERT INTO members (id, user_id, project_id, role, status, created_at)
            VALUES (:id, :user_id, :project_id, :role, :status, :created_at)
        """),
        members,
    )

    # === TASKS ===
    tasks = [
        {
            "id": i,
            "text": f"Task {i}",
            "status": "pending",
            "project_id": i,
            "author_id": i,
            "created_at": now,
        }
        for i in range(1, 6)
    ]
    conn.execute(
        sa.text("""
            INSERT INTO tasks (id, text, status, author_id, project_id, created_at)
            VALUES (:id, :text, :status, :author_id, :project_id, :created_at)
        """),
        tasks,
    )

    # === ASSIGNEES ===
    assignees = [
        {
            "id": i,
            "member_id": i,
            "task_id": i,
            "created_at": now,
        }
        for i in range(1, 6)
    ]
    conn.execute(
        sa.text("""
            INSERT INTO assignees (id, member_id, task_id, created_at)
            VALUES (:id, :member_id, :task_id, :created_at)
        """),
        assignees,
    )


def downgrade():
    conn = op.get_bind()

    conn.execute(sa.text("DELETE FROM assignees WHERE id BETWEEN 1 AND 5"))
    conn.execute(sa.text("DELETE FROM tasks WHERE id BETWEEN 1 AND 5"))
    conn.execute(sa.text("DELETE FROM members WHERE id BETWEEN 1 AND 5"))
    conn.execute(sa.text("DELETE FROM projects WHERE id BETWEEN 1 AND 5"))
    conn.execute(sa.text("DELETE FROM users WHERE id BETWEEN 1 AND 5"))
