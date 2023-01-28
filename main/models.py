from main import db, app

class Conta(db.Model):
    __tablename__ = 'conta'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    movimentacao = db.relationship('Movimentacao', backref='conta',cascade='all, delete')

    def __repr__(self):
        return f'Conta<Nome: {self.nome}>'

class Movimentacao(db.Model):
    __tablename__ = 'movimentacao'
    id = db.Column(db.Integer, primary_key=True)
    detalhe = db.Column(db.String)
    data = db.Column(db.DateTime)
    valor = db.Column(db.String)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id', ondelete='Cascade'), nullable=False)

    def __repr__(self):
        return f'Movimentacao <Valor: {self.valor}, Data: {self.data}, Detalhes: {self.detalhe}, Conta_ID: {self.conta_id}>'

class CategoriaDeDebito(db.Model):
    __tablename__ = 'categoria_de_debito'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    debito = db.relationship('Debito', backref='categoria_de_debito', cascade='all, delete')

    def __repr__(self):
        return f'Categoria De Debito<Nome: {self.nome}>'

class Debito(db.Model):
    __tablename__ = 'debito'
    id = db.Column(db.Integer, primary_key=True)
    dono = db.Column(db.String)
    detalhe = db.Column(db.String)
    data = db.Column(db.DateTime)
    parcelas = db.Column(db.Integer)
    valor_parcela = db.Column(db.String)
    parcelas_falta = db.Column(db.Integer)
    total = db.Column(db.String)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_de_debito.id', ondelete='Cascade'), nullable=False)

    def __repr__(self):
        return (f'Debito<Dono: {self.dono}, Detalhe: {self.detalhe},' 
                f'Data: {self.data}, Parcelas: {self.parcelas}, ValorParcela: {self.valor_parcela}'
                f'ParcelasFalta: {self.parcelas_falta}, Total: {self.total}, CategoriaID: {self.categoria_id}>')

class HistoricoMovimentacao(db.Model):
    __tablename__ = 'historico_movimentacao'
    id = db.Column(db.Integer, primary_key=True)
    data_adicionada = db.Column(db.DateTime)
    detalhe = db.Column(db.String)
    data = db.Column(db.DateTime)
    valor = db.Column(db.String)
    conta = db.Column(db.String)

    def __repr__(self):
        return (f'HistoricoMovimentação<DataAdicionada: {self.data_adicionada},' 
                f'Detalhe: {self.detalhe}, Data: {self.data}, Valor: {self.valor}, Conta: {self.conta}>')

class HistoricoDebitos(db.Model):
    __tablename__ = 'historico_debitos'
    id = db.Column(db.Integer, primary_key=True)
    data_adicionada = db.Column(db.DateTime)
    dono = db.Column(db.String)
    detalhe = db.Column(db.String)
    data = db.Column(db.DateTime)
    parcelas_pagas = db.Column(db.Integer)
    valor_parcela = db.Column(db.String)
    total_falta = db.Column(db.String)

    def __repr__(self):
        return (f'HistoricoDebitos<DataAdicionada: {self.data_adicionada}, Dono: {self.dono}, Detalhe: {self.detalhe},' 
                f'Data: {self.data}, ParcelasPagas: {self.parcelas}, ValorParcela: {self.valor_parcela}'
                f'ParcelasFalta: {self.parcelas_falta}, Total: {self.total}')
    
class Pendencias(db.Model):
    __tablename__ = 'pendencias'
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.String)
    detalhe = db.Column(db.String)
    dono = db.Column(db.String)

    def __repr__(self):
        return f'Pendencias<Id: {self.id}, Valor: {self.valor}, Detalhe: {self.detalhe}, Dono: {self.dono}>'

if __name__ == '__main__':

    with app.app_context():
        db.create_all()