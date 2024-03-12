from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Emprestimo, Chave, Servidor
from ..database import db
from .chave import atualizar_status_chave, status_chave
from datetime import datetime

emprestimo_bp = Blueprint('emprestimo', __name__, template_folder='templates')

@emprestimo_bp.route('/')
def index():
    emprestimos_ativos = Emprestimo.query.filter_by(status='Ativo').all()
    return render_template('emprestimo/index.html', emprestimos_ativos=emprestimos_ativos)


@emprestimo_bp.route('/emprestimo')
def create_get():
    chaves_disponiveis = Chave.query.filter_by(status='disponivel').all()
    servidores = Servidor.query.all()
    return render_template('emprestimo/createEmprestimo.html', chaves_disponiveis=chaves_disponiveis, servidores=servidores)


@emprestimo_bp.route('/devolucao')
def create_devolucao_get():
    chaves_indisponiveis = Chave.query.filter_by(status='indisponivel').all()
    servidores = Servidor.query.all()
    return render_template('emprestimo/devolucaoEmprestimo.html', chaves_indisponiveis=chaves_indisponiveis, servidores=servidores)


@emprestimo_bp.route('/delete')
def delete_get():
    emprestimos_inativos = Emprestimo.query.filter_by(status='Inativo').all()
    return render_template('emprestimo/deleteEmprestimo.html', emprestimos_inativos = emprestimos_inativos)


@emprestimo_bp.route('/createRequest', methods=['POST'])
def inserir_emprestimo():
    if request.method == 'POST':
        # Obter dados do formulário
        chave_id = request.form.get('chave_id')
        if status_chave(chave_id):
            try:
                servidor_retirou_id = request.form.get('servidor_retirou_id')
            
                if servidor_retirou_id:
                    servidor = Servidor.query.get(servidor_retirou_id)
                    if servidor:
                        servidor.status = "Com Pendencia"
            
                novo_emprestimo = Emprestimo(
                    datahora_emprestimo = datetime.now(),
                    status="Ativo",
                    chave_id=chave_id,
                    servidor_retirou_id=servidor_retirou_id,
                )
                
                atualizar_status_chave(chave_id)

                db.session.add(novo_emprestimo)
                db.session.commit()
                flash("Empréstimo feito com sucesso!")
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
                db.session.rollback()
        return redirect(url_for('emprestimo.index'))
        

@emprestimo_bp.route('/devolverRequest', methods=['POST'])
def devolver_emprestimo():
    if request.method == 'POST':
        # Obter dados do formulário
        chave_id = request.form.get('chave_id')
        if chave_id:
            try:
                emprestimo = Emprestimo.query.filter_by(chave_id=chave_id, status="Ativo").first()
                if emprestimo:
                    emprestimo.datahora_devolucao = datetime.now()
                    emprestimo.status = "Inativo"
                    
                servidor_devolveu_id = request.form.get('servidor_devolveu_id')
                emprestimo.servidor_devolveu_id = servidor_devolveu_id
                atualizar_status_chave(chave_id)
                db.session.commit()
                
                id_servidor = emprestimo.servidor_retirou_id
                if id_servidor:
                    servidor = Servidor.query.get(id_servidor)
                    if servidor and verificar_servidor(id_servidor):
                        servidor.status = "Sem Pendencia"
                db.session.commit()
            except Exception as e:
                print(f"Erro ao inserir no banco de dados: {e}")
                db.session.rollback()
        flash("Chave devolvida com sucesso!")
        return redirect(url_for('emprestimo.index'))
        
        
@emprestimo_bp.route('/deleteRequest', methods=['POST'])
def deletar_emprestimo():
    if request.method == 'POST':
        # Obter o ID do empréstimo a ser deletado
        emprestimo_id = request.form.get('id')
        # Obter o empréstimo pelo ID
        emprestimo = Emprestimo.query.get(emprestimo_id)
        
        if emprestimo:
            if emprestimo.status == "Inativo":
                # Deletar o empréstimo do banco de dados
                db.session.delete(emprestimo)
                db.session.commit()
    flash("Empréstimo deletado com sucesso!")
    return redirect(url_for('emprestimo.mostrar_emprestimos_inativos'))


@emprestimo_bp.route('/deleteAllRequest', methods=['POST'])
def deletar_todos_emprestimo():
    if request.method == 'POST':
        Emprestimo.query.filter_by(status="Inativo").delete()

        db.session.commit()
    flash("Empréstimos deletados com sucesso!")
    return redirect(url_for('emprestimo.mostrar_emprestimos_inativos'))


@emprestimo_bp.route('/readInativos')
def mostrar_emprestimos_inativos():
    emprestimos_inativos = Emprestimo.query.filter_by(status='Inativo').all()
    return render_template('emprestimo/mostrarEmprestimos_inativos.html', emprestimos_inativos=emprestimos_inativos)


def verificar_servidor(id_servidor):
    id_servidor  = int(id_servidor)
    emprestimos = Emprestimo.query.filter_by(servidor_retirou_id=id_servidor, status="Ativo").all()
    if len(emprestimos) == 0:
        return True
    return False
    