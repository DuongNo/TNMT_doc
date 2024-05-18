# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.db.session import engine  # noqa
# from app.models.role import Role  # noqa
