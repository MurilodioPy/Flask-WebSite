# from ..models import Emprestimo

# chave_id = 1

# emprestimo = Emprestimo.query.filter_by(chave_id=chave_id, status="Ativo")

# print(emprestimo)
from datetime import datetime
from pytz import timezone

timezone_sp = timezone('America/Sao_Paulo')

print(timezone_sp)

loc_dt = timezone_sp.localize(datetime.utcnow())

print(loc_dt)