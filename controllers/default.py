# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----

from datetime import date


@auth.requires_login()
def index():
    logado = db(db.auth_user.first_name).select()
    x = ''
    for login in logado:
        x = login.first_name

    busca_aluno = ''

    #response.flash = T("Bem vindo  ") + x
    return dict(message=T('Welcome to web2py!'), usuario=x)

# ---- API (example) -----
# @auth.requires_login()


def api_get_user_email():
    if not request.env.request_method == 'GET':
        raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})

# ---- Smart Grid (example) -----
# @auth.requires_membership('admin') # can only be accessed by members of admin groupd


def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:
        raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[
                             tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
# def wiki():
    # auth.wikimenu() # add the wiki to the menu
    # return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# @auth.requires_login()


def entrada():

    return dict(grid=SQLFORM.smartgrid(db.frequencia, linked_tables=['frequencia'], user_signature=False), editable=True, deletable=False, create=True)


@auth.requires_login()
def cadastro():
    # -- Cadastro das Crianças
    form = SQLFORM(db.cadastro)
    if form.accepts(request.vars, session):
        response.flash = 'Informações salvas com sucesso'
    elif form.errors:
        response.flash = 'Deu algum erro!'
    else:
        response.flash = 'Preencha todas as informações'
    return dict(form=form)



def equipe():
    form = SQLFORM(db.equipe)
    if form.accepts(request.vars, session):
        response.flash = 'Informações salvas com sucesso'
    elif form.errors:
        response.flash = 'Deu algum erro!'
    else:
        response.flash = 'Preencha todas as informações'
    return dict(form=form)


def edita_cadastro():
    record = db.cadastro(request.args(0))
    form = SQLFORM(db.cadastro, record, deletable=True)
    if form.accepts(request.vars, session):
        response.flash = 'Dados editados com sucesso!'
    elif form.errors:
        response.flash = 'Deu algum erro!'
    else:
        response.flash = 'Preencha os campos obrigatórios'
    return dict(form=form)


def lst_presenca():

    data_atual = date.today()
    data_registro = data_atual.strftime('%d/%m/%Y')
    cod_presenca = data_atual.strftime('%Y%m%d')

    inf = []

    # Exibe a lista de presença
    dados = db.frequencia
    t = db(dados).select(db.frequencia.cod_presenca,
                         db.frequencia.nome, orderby=[db.frequencia.nome])

    return inf


@auth.requires_login()
def busca_aluno():

    # Variaveis
    campoNome = ''
    campo = ''
    lista = []
    pres = []
    o = ''
    dados = ''
    m = []
    data_atual = ''
    check = ''
    frequencia = ''
    f = ''
    nao_encontrado = ''
    d_nome = ''
    d_matric = ''
    d_mail = ''
    d_resp = ''
    d_sala = ''

    # Gerador codigo da frequencia
    data_atual = date.today()
    data_registro = data_atual.strftime('%d/%m/%Y')
    cod_presenca = data_atual.strftime('%Y%m%d')

    if request.vars.nome_kids:
        campoNome = request.vars.nome_kids
    if db(db.cadastro.nome_crianca == campoNome).select():
        campo = db(db.cadastro.nome_crianca == campoNome).select().first()
        lista.append(campo)

        for l in lista:
            d_nome = l.nome_crianca
            d_matric = l.id
            d_mail = l.email
            d_resp = l.nome_resp
            d_sala = l.sala_matriculado.nome_sala


            if db((db.frequencia.matric_aluno == l.id) & (db.frequencia.cod_presenca == cod_presenca)).select():
                nao_encontrado = "Registro ja efetuado"
    

            else:
                if l.id:

                    dados = {'nome': l.nome_crianca,
                            'data_entrada': data_atual,
                            'cartao': request.vars.c_cartao,
                            'matricula_sala': l.sala_matriculado.nome_sala,
                            'presenca': True,
                            'cod_presenca': cod_presenca,
                            'matric_aluno': l.id,
                            }
                    db.frequencia.insert(**dados)

                    response.flash = "Registro Salvo"

    # Exibe a lista de presença
    m = db(db.frequencia.cod_presenca == cod_presenca).select(
        db.frequencia.id,
        db.frequencia.nome,
        db.frequencia.cod_presenca,
        db.frequencia.matricula_sala,
        db.frequencia.cartao,
        db.frequencia.data_entrada,
        db.frequencia.matric_aluno)

    return locals()

