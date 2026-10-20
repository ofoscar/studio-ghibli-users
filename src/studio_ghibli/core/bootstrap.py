from sqlmodel import Session, select

from studio_ghibli.core.database import engine
from studio_ghibli.core.security import hash_password
from studio_ghibli.models.user import UserTable
from studio_ghibli.core.config import settings
from studio_ghibli.schemas.user import UserRole

def ensure_admin_exists():
  with Session(engine) as session:
    statement = select(UserTable).where(
      UserTable.username == settings.admin_username
    )
    existing_user = session.exec(statement).first()

    if existing_user is not None:
      if existing_user.role != UserRole.admin:
        raise RuntimeError(
          "ADMIN_USERNAME belongs to a user who is not an admin."
        )
      return

    admin = UserTable(
      name="Administrator",
      username=settings.admin_username,
      password_hash=hash_password(
        settings.admin_password.get_secret_value()
      ),
      role=UserRole.admin,
    )

    session.add(admin)
    session.commit()