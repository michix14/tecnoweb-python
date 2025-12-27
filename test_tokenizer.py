#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test del tokenizador
"""
import sys
sys.path.insert(0, '.')

from lexer.lexer import tokenize

print("="*70)
print("TEST DE TOKENIZACION")
print("="*70)
print()

tests = [
    ("usuario mostrar", 3, "Comando simple"),
    ("USUARIO MOSTRAR", 3, "Case insensitive"),
    ("usuario ver [5]", 6, "Con parametro numerico"),
    ("cliente mostrar", 3, "Subtipo cliente"),
    ("usuario agregar [Juan; juan@mail.com; pass123]", None, "Con multiples parametros"),
]

for cmd, expected_count, description in tests:
    print(f"TEST: {description}")
    print(f"Comando: '{cmd}'")
    
    tokens = tokenize(cmd)
    
    if expected_count:  
        status = "OK" if len(tokens) == expected_count else "FAIL"
        print(f"[{status}] Tokens: {len(tokens)} (esperados: {expected_count})")
    else:
        print(f"[INFO] Tokens: {len(tokens)}")
    
    print("Desglose:")
    for i, token in enumerate(tokens):
        tipo = token. type. value
        valor = token.value
        pos = token.position
        # Formato sin espacio después de los dos puntos
        print(f"  {i}.  {tipo:12} | '{valor}' | pos={pos}")
    print()

print("="*70)
print("FIN DE TESTS")
print("="*70)