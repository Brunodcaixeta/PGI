def remover_duplicados_nome(nome: str) -> str:
    """
    Remove subsequências repetidas consecutivas de palavras em um nome.
    Exemplo: "THAISE REGINA GOUVEIA DE REGINA GOUVEIA DE MIRANDA" -> "THAISE REGINA GOUVEIA DE MIRANDA"
    """
    if not nome:
        return ""
    
    words = nome.strip().split()
    i = 0
    while i < len(words):
        found_dup = False
        # Testar tamanhos de subsequência de 1 até metade das palavras restantes
        for s in range(1, (len(words) - i) // 2 + 1):
            sub1 = words[i : i + s]
            sub2 = words[i + s : i + 2 * s]
            # Comparação case-insensitive
            if [w.lower() for w in sub1] == [w.lower() for w in sub2]:
                # Deleta a repetição consecutiva
                del words[i + s : i + 2 * s]
                found_dup = True
                break
        if not found_dup:
            i += 1
            
    return " ".join(words)
