from main import db

class filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    avaliacao = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name
        
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "categoria": self.categoria, "avaliacao": self.avaliacao}


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name