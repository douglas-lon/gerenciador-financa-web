from datetime import datetime
from flask import render_template, request, redirect, url_for
from main import app, db
from main.models import Pendencias, Conta, Movimentacao, Debito, CategoriaDeDebito, HistoricoMovimentacao, HistoricoDebitos
from main.forms import AdicionarMovimentacao, AdicionarDebito
from main.utils import is_number

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html')
	
@app.route('/conta/',  methods=["GET", "POST"])
def conta():
    if request.method == 'POST':
        formData = request.form.get('hINP', '')
        if formData.strip() != '':
            conta = Conta(nome=formData)
            db.session.add(conta)
            db.session.commit()
    
    contas = Conta.query.all()

    lista_total = []
    for conta in contas:
        m_total = 0
        for m in conta.movimentacao:
            m_total += float(m.valor)
        lista_total.append(m_total)

    return render_template('conta.html',lista_contas=contas, lista_total=lista_total)

@app.route('/conta_criada/', methods=['GET', 'POST'])
def conta_criada():
    conta_nome = request.args.get('nome', str)

    form = AdicionarMovimentacao()
    if form.validate_on_submit():
        conta = Conta.query.filter_by(nome=conta_nome).first_or_404()
        novo_valor = is_number(form.valor.data)

        if novo_valor:
            movimentacao = Movimentacao(
            detalhe=form.detalhe.data,
            data=form.data.data,
            valor=novo_valor,
            conta=conta
            )
            db.session.add(movimentacao)
            db.session.commit()

            h = HistoricoMovimentacao(
                data_adicionada=datetime.now(),
                detalhe= f'Add: {form.detalhe.data}',
                data=form.data.data,
                valor=novo_valor,
                conta=conta.nome
            )
            db.session.add(h)
            db.session.commit()

        else:
            form.valor.errors.append('Digite um valor valido')

        

    conta = Conta.query.filter_by(nome=conta_nome).first_or_404()
    lista_movimentacao = conta.movimentacao
    
    return render_template('conta_criada.html', 
        conta=conta, form=form, 
        lista_movimentacao=lista_movimentacao
    )


@app.route('/att_m', methods=['POST'])
def att_m():
    nome = request.args.get('nome', str)
    id = request.args.get('id', int)
    data = request.args.get('data', str)
    detalhe = request.args.get('detalhe', str)
    valor = request.args.get('valor', str)
    data = data.split('-')
    data = datetime(int(data[0]), int(data[1]), int(data[2]))

    novo_valor = is_number(valor)
    if novo_valor:
        m = Movimentacao.query.get_or_404(id)
        m.data = data
        m.detalhe = detalhe
        m.valor = valor
        db.session.commit()

        h = HistoricoMovimentacao(
                data_adicionada=datetime.now(),
                detalhe=f'Edit: {detalhe}',
                data=data,
                valor=valor,
                conta=m.conta.nome
            )
        db.session.add(h)
        db.session.commit()

    return redirect(url_for('conta_criada', nome=nome.strip()))

@app.route('/excluir_cm/', methods=["POST"])
def excluir_cm():

    redirect_to = request.args.get('what', str)
    id = request.args.get('id', int)
    conta_nome = request.args.get('nome', str)

    if redirect_to == 'conta':
        c = Conta.query.get_or_404(id)
        db.session.delete(c)
        db.session.commit()
        h = HistoricoMovimentacao(
                data_adicionada=datetime.now(),
                detalhe= 'Conta Excluida',
                data=datetime.now(),
                valor=0,
                conta=c.nome
            )
        db.session.add(h)
        db.session.commit()
        return redirect(url_for('conta'))
    elif redirect_to == 'movimentacao':
        m = Movimentacao.query.get_or_404(id)
        h = HistoricoMovimentacao(
                data_adicionada=datetime.now(),
                detalhe= 'Excluido',
                data=m.data,
                valor=m.valor,
                conta=m.conta.nome
            )
        
        db.session.delete(m)
        db.session.commit()

        db.session.add(h)
        db.session.commit()
        return redirect(url_for('conta_criada', nome=conta_nome))

    return redirect(url_for('home'))
    
@app.route('/debitos/', methods=["GET", "POST"])
def debitos():
    
    if request.method == 'POST':
        formData = request.form.get('hINP', '')
        if formData.strip() != '':
            debito = CategoriaDeDebito(nome=formData)
            db.session.add(debito)
            db.session.commit() 
    
    categorias = CategoriaDeDebito.query.all()
    totals = [0,0]
    debitos = []
    for cat in categorias:
        debitos.append(cat.debito)
    
    debito_conta = [debitos.copy()]
    for j, deb in enumerate(debitos):
        if deb:
            debito_conta[j] = 0
            for i in deb:
                debito_conta[j] += float(i.total)
                totals[0] += float(i.total)
                totals[1] +=float(i.valor_parcela)

    return render_template('debitos.html', lista_debitos=categorias, totals=totals, debitos_conta=debito_conta)

@app.route('/categoria_debito/', methods=["GET", "POST"])
def categoria_debito():

    form = AdicionarDebito()
    categoria_nome = request.args.get('nome', str)
    categoria = CategoriaDeDebito.query.filter_by(nome=categoria_nome).first_or_404()
    if form.validate_on_submit():
        parcelas_n = is_number(form.parcelas.data)
        valor_parcela_n = is_number(form.valor_parcela.data)

        if parcelas_n and valor_parcela_n:
            deb = Debito(
                dono=form.dono.data,
                detalhe=form.detalhe.data,
                data=form.data.data,
                parcelas=int(parcelas_n),
                valor_parcela=valor_parcela_n,
                parcelas_falta=int(parcelas_n),
                total= str(int(parcelas_n) * float(valor_parcela_n)),
                categoria_id=categoria.id
                )
            db.session.add(deb)
            db.session.commit()
            hD = HistoricoDebitos(
                data_adicionada=datetime.now(),
                detalhe=f'Add: {form.detalhe.data}',
                dono=form.dono.data,
                data=form.data.data,
                parcelas_pagas=int(parcelas_n),
                valor_parcela=valor_parcela_n,
                total_falta= str(int(parcelas_n) * float(valor_parcela_n)),
            )
            db.session.add(hD)
            db.session.commit()
        else:
            form.valor.errors.append('Digite um valor valido')

        

    
    lista_debitos = categoria.debito
    conta_dict = []

    for conta in Conta.query.all():
        total = 0
        for mov in conta.movimentacao:
            total += float(mov.valor)

        conta_dict.append({
            'id': conta.id,
            'nome': conta.nome,
            'total': total
        })

    return render_template('categoria_debito.html',categoria=categoria, 
        lista_debitos=lista_debitos, form=form, lista_contas=conta_dict)


@app.route('/pagar_all/', methods=['POST'])
def pagar_all():
    id = request.args.get('id', int)
    data = request.form
    cat = CategoriaDeDebito.query.get_or_404(id)
    d = Debito.query.filter_by(categoria_id=id).all()
    total_mes = 0
    print(data)

    for debito in d:
        debito.parcelas_falta = debito.parcelas_falta - 1
        debito.total = str(round(float(debito.total), 2) - round(float(debito.valor_parcela), 2))
        total_mes += round(float(debito.valor_parcela),2)

        hD = HistoricoDebitos(
            data_adicionada=datetime.now(),
            detalhe=f"Pag: {debito.detalhe}",
            dono=debito.dono,
            data=debito.data,
            parcelas_pagas= debito.parcelas_falta,
            valor_parcela=debito.valor_parcela,
            total_falta= str(float(debito.valor_parcela) * int(debito.parcelas_falta)),
        )
        db.session.add(hD)
        db.session.commit()

        if debito.parcelas_falta <= 0 or float(debito.total) <=0:
            db.session.delete(debito)
            db.session.commit()
        
    db.session.commit()

    if 'usarContaAll' in data.keys():
        conta = Conta.query.get_or_404(data['contas'])
        movimentacao = Movimentacao(
            detalhe=f'{cat.nome}',
            data=datetime.now().date(),
            valor= f'-{total_mes}',
            conta=conta
            )
        db.session.add(movimentacao)
        db.session.commit()
        
        h = HistoricoMovimentacao(
                data_adicionada=datetime.now(),
                detalhe=f"Pag: {cat.nome} Mês",
                data=datetime.now(),
                valor=f'-{total_mes}',
                conta=conta.nome
            )
        db.session.add(h)
        db.session.commit()
    

    return redirect(url_for('categoria_debito', nome=cat.nome.strip()))
        

@app.route('/pagar_d', methods=['POST'])
def pagar_d():
    data = request.form
    debito = Debito.query.get_or_404(data['idDebito'])
    debito.total = f'{float(debito.total):.2f}'
    
    if debito.parcelas_falta > 0 and float(debito.total) >= float(data['totalPI']):
        debito.parcelas_falta = debito.parcelas_falta - int(data['qtdParcelas'])
        debito.total = str(float(debito.total) - float(data['totalPI']))

        if (float(debito.total) <= 0):
            db.session.delete(debito)
            db.session.commit()
        else:
            db.session.commit()

        hD = HistoricoDebitos(
            data_adicionada=datetime.now(),
            detalhe=f"Pag: {debito.detalhe}",
            dono=debito.dono,
            data=debito.data,
            parcelas_pagas=int(data['qtdParcelas']),
            valor_parcela=debito.valor_parcela,
            total_falta= str(float(debito.valor_parcela) * int(data['qtdParcelas'])),
        )
        db.session.add(hD)
        db.session.commit()
    else:
        return f"Error {float(data['qtdParcelas']) * float(data['totalPI'])}"
        
    
    
    if 'usarConta' in data.keys():
        conta = Conta.query.get_or_404(data['contas'])
        movimentacao = Movimentacao(
            detalhe=data['detalhes'],
            data=datetime.now().date(),
            valor= f'-{float(data["qtdParcelas"]) * float(data["totalPI"])}',
            conta=conta
        )
        db.session.add(movimentacao)
        db.session.commit()
        
        h = HistoricoMovimentacao(
                data_adicionada=datetime.now(),
                detalhe=f"Pag: {data['detalhes']}",
                data=datetime.now(),
                valor=f'-{float(data["qtdParcelas"]) * float(data["totalPI"])}',
                conta=conta.nome
            )
        db.session.add(h)
        db.session.commit()
    
    nome = request.args.get('nome', str)
    

    return redirect(url_for('categoria_debito', nome=nome.strip()))

@app.route('/att_d', methods=["POST"])
def att_d():
    nome = request.args.get('nome', str)
    data = request.args.get('data', str)
    data = data.split('-')
    data = datetime(int(data[0]), int(data[1]), int(data[2]))

    id = request.args.get('id', int)
    detalhe = request.args.get('detalhe', str)
    dono = request.args.get('dono', str)
    valor_parcela = request.args.get('valor_parcela', str)
    parcelas = request.args.get('parcelas', str)

    parcelas_n = is_number(parcelas)
    valor_parcela_n = is_number(valor_parcela)

    if parcelas_n and valor_parcela_n:
        d = Debito.query.get_or_404(id)
        d.dono = dono
        d.data = data
        d.detalhe = detalhe
        d.valor_parcela = valor_parcela_n
        d.parcelas = parcelas_n
        d.parcelas_falta = parcelas_n
        d.total= str(int(parcelas_n) * float(valor_parcela_n))
        db.session.commit()

        hD = HistoricoDebitos(
            data_adicionada=datetime.now(),
            detalhe=f"Edit: {detalhe}",
            dono=dono,
            data=data,
            parcelas_pagas=parcelas_n,
            valor_parcela=valor_parcela_n,
            total_falta= str(int(parcelas_n) * float(valor_parcela_n)),
        )
        db.session.add(hD)
        db.session.commit()

    
    return redirect(url_for('categoria_debito', nome=nome.strip()))


@app.route('/excluir_cd', methods=['POST'])
def excluir_cd():
    redirect_to = request.args.get('what', str)
    id = request.args.get('id', int)
    categoria_nome = request.args.get('nome', str)

    if redirect_to == 'categoria':
        d = CategoriaDeDebito.query.get_or_404(id)
        hD = HistoricoDebitos(
            data_adicionada=datetime.now(),
            detalhe=f"Catégoria Excluida",
            dono=f"Nome: {d.nome}",
            data=datetime.now(),
            parcelas_pagas=0,
            valor_parcela='0',
            total_falta= '0',
        )

        db.session.delete(d)
        db.session.commit()
        
        db.session.add(hD)
        db.session.commit()

        return redirect(url_for('debitos'))
    elif redirect_to == 'debito':
        d = Debito.query.get_or_404(id)
        hD = HistoricoDebitos(
            data_adicionada=datetime.now(),
            detalhe=f"Excluido",
            dono=d.dono,
            data=d.data,
            parcelas_pagas=d.parcelas_falta,
            valor_parcela=d.valor_parcela,
            total_falta= d.total,
        )
        db.session.delete(d)
        db.session.commit()
        db.session.add(hD)
        db.session.commit()
        return redirect(url_for('categoria_debito', nome=categoria_nome))

    return redirect(url_for('home'))

@app.route('/pendencias/',  methods=['GET','POST'])
def pendencias():
    data = request.form

    if data:
        valor = is_number(data['valor'])
        if valor:
            p = Pendencias(
                dono=data['dono'],
                detalhe=data['detalhe'],
                valor=valor
            )
            db.session.add(p)
            db.session.commit()
            
    pendencias = Pendencias.query.all()
    return render_template('pendencias.html', pendencias=pendencias)

@app.route('/excluir_pen/', methods=['POST'])
def excluir_pendencia():
    id = request.args.get('id', int)

    p = Pendencias.query.get_or_404(id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('pendencias'))

@app.route('/resumo/')
def resumo():
    todas_movimentacao = []
    for mov in Conta.query.all():
        if mov.movimentacao:
            for i in mov.movimentacao:
                todas_movimentacao.append(i)

    donos = {
        'Todos': [0,0],
    }
    for deb in CategoriaDeDebito.query.all():
        if deb.debito:
            for i in deb.debito:

                donos['Todos'][0] +=float( i.total)
                donos['Todos'][1] += float(i.valor_parcela)
    
    return render_template('resumo.html', movimentacao=todas_movimentacao, todos_debitos=donos)
	
@app.route('/historico/')
def historico():
    hM = HistoricoMovimentacao.query.all()
    hD = HistoricoDebitos.query.all()
    return render_template('historico.html', hM=hM, hD=hD)