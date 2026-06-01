from django.test import TestCase
from pgi.utils import remover_duplicados_nome

class NameDeduplicationTests(TestCase):
    def test_deduplicate_subphrase(self):
        # Caso clássico trazido pelo usuário
        nome = "THAISE REGINA GOUVEIA DE REGINA GOUVEIA DE MIRANDA"
        esperado = "THAISE REGINA GOUVEIA DE MIRANDA"
        self.assertEqual(remover_duplicados_nome(nome), esperado)

    def test_deduplicate_single_word(self):
        # Repetição simples de uma palavra
        self.assertEqual(remover_duplicados_nome("JOÃO SILVA SILVA"), "JOÃO SILVA")
        self.assertEqual(remover_duplicados_nome("PEDRO PEDRO PEDRO"), "PEDRO")

    def test_no_duplicates(self):
        # Nome comum sem repetições consecutivas
        self.assertEqual(remover_duplicados_nome("MARIA DE SOUZA"), "MARIA DE SOUZA")

    def test_empty_input(self):
        # Inputs vazios ou nulos
        self.assertEqual(remover_duplicados_nome(""), "")
        self.assertEqual(remover_duplicados_nome("   "), "")

