"""Aplicação web (Flask). Rodar com: flask --app escala.web run"""
import os

from flask import Flask

from escala.repositorio import RepositorioEmMemoria
from escala.servico import ServicoEscala
from escala.web.api import api
from escala.web.paginas import paginas


def create_app(servico: ServicoEscala | None = None) -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-somente-local")
    app.extensions["escala"] = servico or ServicoEscala(RepositorioEmMemoria())
    app.register_blueprint(api)
    app.register_blueprint(paginas)
    return app
