from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

# Instancia o objeto SÓ UMA VEZ.
# Cria o objeto DB, mas ainda não o vincula ao App (Lazy Initialization)
# Neste ponto, o db existe, mas não sabe qual é a URL do banco de dados (SQLite, PostgreSQL, etc.).