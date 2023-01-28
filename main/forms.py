from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField
from wtforms.validators import DataRequired

class AdicionarMovimentacao(FlaskForm):
    data = DateField('Data: ', validators=[DataRequired('Necessário Data')])
    detalhe = StringField('Detalhes: ', validators=[DataRequired('Necessário Detalhes')])
    valor = StringField('Valor: ', validators=[DataRequired('Necessário Valor')])
    submit = SubmitField('Adicionar')

class AdicionarDebito(FlaskForm):
    dono = StringField('Dono: ', validators=[DataRequired('Necessário Culpado')])
    data = DateField('Data: ', validators=[DataRequired('Necessário Data')])
    detalhe = StringField('Detalhes: ', validators=[DataRequired('Necessário Detalhes')])
    parcelas = StringField('Parcelas: ', validators=[DataRequired('Necessário um parcela')])
    valor_parcela = StringField('Valor da Parcela: ', validators=[DataRequired('Necessário Valor')])
    submit = SubmitField('Adicionar')

