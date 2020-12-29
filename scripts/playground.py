from pyeda.boolalg import expr
import re
from pyeda.parsing.boolexpr import Error as ParseError


stri1 = '(-(bitcoin * litecoin)) + ((-monero + litecoin) * (cardano+ethereum))'
stri1 = stri1.replace('*', '&')
stri1 = stri1.replace('+', '|')
stri1 = stri1.replace('-', '~')
print(stri1)

try:
    result1 = str(expr.expr(stri1).to_dnf())
    print(result1)

except ParseError as e:
    error_msg = str(e)
    error_msg = error_msg.replace('&', '*')
    error_msg = error_msg.replace('|', '+')
    error_msg = error_msg.replace('~', '-')
    print(error_msg)

stri2 = '(-(bitcoin * * litecoin)) + ((-monero + litecoin) * cardano)'
stri2 = stri2.replace('*', '&')
stri2 = stri2.replace('+', '|')
stri2 = stri2.replace('-', '~')

print('################################')

print(stri2)

try:
    result2 = str(expr.expr(stri2).to_dnf())
    print(result2)

except ParseError as e:
    error_msg = str(e)
    error_msg = error_msg.replace('&', '*')
    error_msg = error_msg.replace('|', '+')
    error_msg = error_msg.replace('~', '-')
    print(error_msg)





