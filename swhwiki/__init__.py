from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import Base, DBSession
from .security import SecurityPolicy


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    with Configurator(settings=settings, root_factory=".models.Root") as config:
        config.include("pyramid_jinja2")
        config.set_security_policy(
            SecurityPolicy(
                secret=settings["tutorial.secret"],
            ),
        )
        config.include(".routes")
        config.scan()
    return config.make_wsgi_app()
