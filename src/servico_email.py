# src/servico_email.py

# A função de envio de email. No código de produção, ela se conectaria ao SMTP.
def enviar_confirmacao(fatura):
    """
    Envia o email de confirmação de compra.
    Nos testes, esta função será substituída (patched/stubbed) para não enviar nada.
    """
    # Lógica de envio real (Placeholder)
    # print(f"Enviando e-mail de confirmação para fatura: {fatura.id}")
    pass # Deixamos vazio para ser um alvo de patch claro.