from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha: str, hash_senha: str) -> bool:
    '''
        funcao para verificar se a senha esta correta, comparando a senha com o hash
    '''
    return CRYPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    '''
        funcao que gerar e retorna o hash da senha
    '''
    return CRYPTO.hash(senha)
