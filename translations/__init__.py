from .global_t    import GLOBAL
from .home        import HOME
from .projetos    import PROJETOS_T
from .sobre       import SOBRE
from .contato     import CONTATO
from .legal       import LEGAL

def get_translation(lang: str = "pt-br") -> dict:
    """Mescla todas as traduções numa dict plana, priorizando o idioma pedido."""
    base = {}
    for module in (GLOBAL, HOME, PROJETOS_T, SOBRE, CONTATO, LEGAL):
        section = module.get(lang) or module.get("pt-br", {})
        base.update(section)
    return base
