from ..models import Emprestimo

chave_id = 1

emprestimo = Emprestimo.query.filter_by(chave_id=chave_id, status="Ativo")

print(emprestimo)