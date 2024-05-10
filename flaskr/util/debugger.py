# debugger: função que printa as variaveis colocadas no parametro da função no terminal, usando um try except para evitar erros
# parametros: *args: variaveis a serem printadas
# retorno: None
def debugger(*args):
    try:
        for arg in args:
            print(arg)
    except:
        print("Erro ao printar variáveis")
    return None
