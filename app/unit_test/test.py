# from ..models import Emprestimo

# chave_id = 1

# emprestimo = Emprestimo.query.filter_by(chave_id=chave_id, status="Ativo")

# print(emprestimo)
from datetime import datetime


# timezone_sp = timezone('America/Sao_Paulo')

# print(timezone_sp)
# # pytz.timezone("America/Sao_Paulo").localize(now)
# loc_dt = timezone_sp.localize(datetime.now())

# print(loc_dt)

# format = "%Y-%m-%d %H:%M:%S %Z%z"
 
# # Current time in UTC
# now_utc = datetime.now(timezone('UTC'))
# print(now_utc.strftime(format))
 
# # Convert to Asia/Kolkata time zone
# now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
# print(now_asia.strftime(format))

# def data_local():
#     timezone_sp = timezone('America/Sao_Paulo')
#     loc_dt = timezone_sp.localize(datetime.now())
#     return loc_dt

# print(data_local())

print(datetime.now())
