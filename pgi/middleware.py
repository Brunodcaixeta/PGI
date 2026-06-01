import logging
from mpgo_keycloak.client import MPGOKeycloakClient, TokenData
from mpgo_keycloak.integrations.django import KeycloakUser
from pgi.utils import remover_duplicados_nome

# Monkey patch KeycloakUser.nome to clean up duplicated names from Keycloak/EPerfil IDP
original_nome_prop = KeycloakUser.nome

@property
def patched_nome(self):
    val = original_nome_prop.fget(self)
    
    # Se o nome vier vazio (ex: EPerfil não preenchido ou nulo), tenta o nome decodificado do token JWT
    if not val:
        val = self.name
        
    # Se ainda estiver vazio, tenta compor first_name (given_name) + last_name (family_name)
    if not val:
        decoded = getattr(self.token_data, 'decoded', {}) or {}
        given = decoded.get("given_name", "")
        family = decoded.get("family_name", "")
        if given or family:
            val = f"{given} {family}".strip()
            
    # Se tudo falhar, cai para o preferred_username do Keycloak
    if not val:
        val = self.preferred_username
        
    return remover_duplicados_nome(val)

KeycloakUser.nome = patched_nome

logger = logging.getLogger(__name__)

class HybridKeycloakMiddleware:
    """
    Middleware Django para autenticação híbrida com Keycloak.
    
    Popula request.keycloak_user a partir dos tokens JWT armazenados na sessão
    do Django (para requisições tradicionais de browser). 
    Caso o access_token esteja expirado, tenta renová-lo silenciosamente 
    utilizando o refresh_token guardado em sessão.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.client = MPGOKeycloakClient.from_env()

    def __call__(self, request):
        # 1. Ignorar se o SDK do Keycloak estiver desabilitado no .env
        if self.client.is_disabled():
            request.keycloak_user = None
            return self.get_response(request)

        # 2. Se já tiver keycloak_user (setado pelo middleware do SDK via header Bearer), prossegue
        if getattr(request, 'keycloak_user', None) is not None:
            return self.get_response(request)

        request.keycloak_user = None

        # 3. Se o usuário estiver autenticado via sessão do Django, tenta popular a partir da sessão
        if request.user.is_authenticated:
            access_token = request.session.get('access_token')
            refresh_token = request.session.get('refresh_token')

            if access_token:
                # Se o token estiver expirado, tenta dar refresh
                if self.client.is_token_expired(access_token):
                    if refresh_token:
                        try:
                            logger.info("[ZK-Hybrid] Access token expirado. Tentando refresh silencioso...")
                            token_data = self.client.refresh_token(refresh_token)
                            
                            access_token = token_data.access_token
                            refresh_token = token_data.refresh_token
                            
                            # Atualiza a sessão
                            request.session['access_token'] = access_token
                            request.session['refresh_token'] = refresh_token
                            logger.info("[ZK-Hybrid] Refresh token efetuado com sucesso!")
                        except Exception as e:
                            logger.warning(f"[ZK-Hybrid] Erro ao renovar token silenciosamente: {e}")
                            # Desconecta o usuário localmente caso o refresh expire/falhe
                            from django.contrib.auth import logout
                            logout(request)
                            access_token = None
                            refresh_token = None
                    else:
                        access_token = None

                # Se temos um access_token válido (ou renovado com sucesso)
                if access_token:
                    try:
                        decoded = self.client.decode_token(access_token, verify=False)
                        token_data = TokenData({
                            "access_token": access_token,
                            "refresh_token": refresh_token or "",
                            "id_token": "",
                        })
                        token_data.decoded = decoded

                        # Carrega dados do EPerfil armazenados em cache de sessão
                        e_perfil = None
                        perfil_criptografado = None
                        if 'e_perfil_data' in request.session:
                            try:
                                from mpgo_keycloak.models.eperfil import EPerfil
                                e_perfil = EPerfil(**request.session['e_perfil_data'])
                                perfil_criptografado = request.session.get('perfil_criptografado')
                            except Exception as ex:
                                logger.warning(f"[ZK-Hybrid] Erro ao instanciar EPerfil da sessão: {ex}")

                        # Constrói e injeta o objeto KeycloakUser no request
                        request.keycloak_user = KeycloakUser(
                            token_data=token_data,
                            e_perfil=e_perfil,
                            perfil_criptografado=perfil_criptografado
                        )
                    except Exception as e:
                        logger.error(f"[ZK-Hybrid] Falha ao decodificar token da sessão: {e}")

        return self.get_response(request)
