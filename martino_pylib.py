
def trova_in_lista(lista,targets):
    indici=([])
    valori=([])
    for elem in targets:
        
        if elem <= min(lista):
            indici.append(lista.index(min(lista)))
            valori.append(min(lista))
            continue

        if elem >= max(lista):
            indici.append(lista.index(max(lista)))
            valori.append(max(lista))
            continue
        
        if min(lista) < elem < max(lista):
            max_low=max([item for item in lista if item<=elem])
            indici.append(lista.index(max_low))
            valori.append(max_low)
    return indici,valori
    

if __name__=='__main__':
    elenco=[10009,-34, 6,-39,56,0,10000, -40]
    print(trova_in_lista(elenco,[-1000, -100, 10005, 0, 7]))