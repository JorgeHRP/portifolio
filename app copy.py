import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-super-secreta")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ============================================================
# TRADUCOES — PT-BR e EN
# ============================================================
TRADUCOES = {
    "pt-br": {
        "inicio":               "Início",
        "projetos":             "Projetos",
        "sobre":                "Sobre",
        "contato":              "Contato",
        "entre_contato":        "Falar sobre um projeto",
        "todos_direitos":       "Todos os direitos reservados",
        "privacidade":          "Privacidade",
        "ver_todos":            "Ver todos os projetos",
        "disponivel":           "Disponível para novos projetos",
        "fechar":               "Fechar",
        "hero_ola":             "Olá, sou",
        "hero_titulo":          "Especialista em IA e Automações",
        "hero_descricao":       "Construo produtos digitais orientados a resultado — automação, sistemas web, dashboards e integrações. Sempre com foco no problema real por trás do pedido.",
        "ver_projetos":         "Ver Projetos",
        "projetos_destaque":    "Projetos em Destaque",
        "projetos_subtitulo":   "Do conceito ao ar, sem enrolação",
        "colecao_trabalhos":    "Soluções reais entregues para negócios reais",
        "meus_projetos":        "Todos os Projetos",
        "mencao_honrosa":       "Outros Projetos",
        "mencao_subtitulo":     "Mais trabalhos entregues",
        "filtro_todos":         "Todos",
        "filtro_ia":            "Inteligência Artificial",
        "filtro_automacao":     "Automação",
        "filtro_web":           "Web & Sistemas",
        "ver_detalhes":         "Ver Detalhes",
        "tecnologias":          "Tecnologias",
        "voltar_projetos":      "Voltar aos projetos",
        "sobre_projeto":        "Sobre o Projeto",
        "problema_resolvido":   "O Problema",
        "solucao_implementada": "A Solução",
        "resultados":           "Resultado",
        "principais_funcionalidades": "Funcionalidades",
        "como_funciona":        "Como Funciona",
        "ver_codigo":           "Ver no GitHub",
        "sobre_mim":            "Sobre",
        "conheca_trajetoria":   "Especialidades e experiência",
        "dev_apaixonado":       "Especialista em IA e Automações",
        "sobre_texto1":         "Construo produtos digitais orientados a resultado. Não entrego código, entrego o que o cliente precisa que funcione.",
        "sobre_texto2":         "Experiência com automação via WhatsApp, bots com IA, dashboards em tempo real, APIs REST e sistemas web completos.",
        "sobre_texto3":         "Trabalho com negócios de diferentes setores — o que me deu visão prática de como tecnologia pode ser simples e eficaz ao mesmo tempo.",
        "projetos_ia":          "Projetos IA",
        "automacoes_n8n":       "Automações",
        "anos_experiencia":     "Anos",
        "satisfacao_cliente":   "Clientes",
        "minhas_habilidades":   "Especialidades",
        "entre_contato_titulo": "Vamos construir algo juntos",
        "trabalhar_juntos":     "Sem compromisso, sem pitch de vendas — só uma conversa direta sobre o que precisas resolver.",
        "vamos_conversar":      "Enviar Mensagem",
        "vamos_conversar_texto": "Especializado em IA, automações e sistemas web. Vamos conversar sobre o seu projeto.",
        "email":                "Email",
        "telefone":             "WhatsApp",
        "localizacao":          "Localização",
        "disponibilidade":      "Disponibilidade",
        "segunda_sexta":        "Seg–Sex, 9h–18h",
        "envie_mensagem":       "Envie uma Mensagem",
        "nome_completo":        "Nome",
        "seu_nome":             "Como posso te chamar?",
        "seu_email":            "seu@email.com",
        "assunto":              "Assunto",
        "como_posso_ajudar":    "Como posso ajudar?",
        "mensagem":             "Mensagem",
        "conte_projeto":        "Qual é o gargalo do seu negócio?",
        "enviar_mensagem":      "Enviar Mensagem",
        "mensagem_enviada":     "Mensagem enviada com sucesso!",
        "erro_enviar":          "Erro ao enviar. Tente novamente.",
        "pagina_nao_encontrada": "Página não encontrada",
        "ops_pagina":           "Esta página não existe.",
        "voltar_home":          "Voltar ao início",
        "cookie_texto":         "Utilizamos cookies para melhorar sua experiência.",
        "cookie_aceitar":       "Aceitar",
        "cookie_recusar":       "Recusar",
    },
    "en": {
        "inicio":               "Home",
        "projetos":             "Projects",
        "sobre":                "About",
        "contato":              "Contact",
        "entre_contato":        "Let's talk",
        "todos_direitos":       "All rights reserved",
        "privacidade":          "Privacy",
        "ver_todos":            "View all projects",
        "disponivel":           "Available for new projects",
        "fechar":               "Close",
        "hero_ola":             "Hi, I'm",
        "hero_titulo":          "AI & Automation Expert",
        "hero_descricao":       "I build result-driven digital products — automation, web systems, dashboards and integrations. Always focused on the real problem behind the request.",
        "ver_projetos":         "View Projects",
        "projetos_destaque":    "Featured Projects",
        "projetos_subtitulo":   "From concept to production, no fluff",
        "colecao_trabalhos":    "Real solutions delivered for real businesses",
        "meus_projetos":        "All Projects",
        "mencao_honrosa":       "More Projects",
        "mencao_subtitulo":     "More delivered work",
        "filtro_todos":         "All",
        "filtro_ia":            "Artificial Intelligence",
        "filtro_automacao":     "Automation",
        "filtro_web":           "Web & Systems",
        "ver_detalhes":         "View Details",
        "tecnologias":          "Technologies",
        "voltar_projetos":      "Back to projects",
        "sobre_projeto":        "About the Project",
        "problema_resolvido":   "The Problem",
        "solucao_implementada": "The Solution",
        "resultados":           "Result",
        "principais_funcionalidades": "Features",
        "como_funciona":        "How It Works",
        "ver_codigo":           "View on GitHub",
        "sobre_mim":            "About",
        "conheca_trajetoria":   "Skills & experience",
        "dev_apaixonado":       "AI & Automation Expert",
        "sobre_texto1":         "I build result-driven digital products. I don't deliver code, I deliver what the client needs to work.",
        "sobre_texto2":         "Experience with WhatsApp automation, AI bots, real-time dashboards, REST APIs and full web systems.",
        "sobre_texto3":         "I work with businesses across different sectors — which gave me practical insight into how technology can be simple and effective at the same time.",
        "projetos_ia":          "AI Projects",
        "automacoes_n8n":       "Automations",
        "anos_experiencia":     "Years",
        "satisfacao_cliente":   "Clients",
        "minhas_habilidades":   "Skills",
        "entre_contato_titulo": "Let's build something together",
        "trabalhar_juntos":     "No commitment, no sales pitch — just a direct conversation about what you need to solve.",
        "vamos_conversar":      "Send Message",
        "vamos_conversar_texto": "Specialized in AI, automation and web systems. Let's talk about your project.",
        "email":                "Email",
        "telefone":             "WhatsApp",
        "localizacao":          "Location",
        "disponibilidade":      "Availability",
        "segunda_sexta":        "Mon–Fri, 9am–6pm",
        "envie_mensagem":       "Send a Message",
        "nome_completo":        "Name",
        "seu_nome":             "Your name",
        "seu_email":            "your@email.com",
        "assunto":              "Subject",
        "como_posso_ajudar":    "How can I help?",
        "mensagem":             "Message",
        "conte_projeto":        "What's the bottleneck in your business?",
        "enviar_mensagem":      "Send Message",
        "mensagem_enviada":     "Message sent successfully!",
        "erro_enviar":          "Error sending. Please try again.",
        "pagina_nao_encontrada": "Page not found",
        "ops_pagina":           "This page does not exist.",
        "voltar_home":          "Back to home",
        "cookie_texto":         "We use cookies to improve your experience.",
        "cookie_aceitar":       "Accept",
        "cookie_recusar":       "Decline",
    }
}

# ============================================================
# PROJETOS DESTAQUE — 6 com modal completo
# ============================================================
PROJETOS = [
    {
        "id": 1,
        "destaque": True,
        "titulo": "Automação de Atendimento via WhatsApp",
        "descricao": "Sistema de atendimento automático integrado com Evolution API. Backend em Python com sessão persistente, health check e deploy em nuvem.",
        "descricao_longa": "Sistema completo de atendimento via WhatsApp usando a principal API open-source do mercado. O bot mantém contexto da conversa, responde de forma humanizada e nunca cai — sessão persistente com reconexão automática e health check monitorado 24/7.",
        "problema": "O cliente perdia leads fora do horário comercial. Sem atendimento automático, mensagens ficavam sem resposta por horas.",
        "solucao": "Bot Python com Telethon + Evolution API rodando 24/7 em nuvem. Sessão persistente, reconexão automática, health check e deploy no Railway com zero downtime.",
        "resultado": "Zero leads perdidos fora do horário comercial. Atendimento instantâneo 24/7.",
        "funcionalidades": ["Atendimento 24/7", "Sessão persistente", "Health check", "Deploy Railway", "Logs estruturados", "Evolution API"],
        "como_funciona": "Mensagem chega → Bot processa → Responde → Loga → Monitora",
        "tecnologias": ["Python", "Telethon", "Flask", "Evolution API", "Railway"],
        "imagem": "proj-whatsapp.jpg",
        "categoria": ["automacao", "ia"],
        "github": "https://github.com/JorgeHRP"
    },
    {
        "id": 2,
        "destaque": True,
        "titulo": "Dashboard de Inteligência Artificial",
        "descricao": "Painel de resultados para projeto de IA universitário. Métricas em tempo real para público técnico e não técnico.",
        "descricao_longa": "Dashboard desenvolvido para apresentação de resultados de projeto de IA em ambiente universitário. Dados em tempo real, gráficos interativos e layout pensado para ser lido por qualquer audiência.",
        "problema": "Os resultados do projeto de IA existiam apenas em arquivos e logs. Era impossível apresentá-los de forma clara para diferentes públicos.",
        "solucao": "Dashboard Flask com visualizações em tempo real, filtragem por período e exportação de relatórios em dark theme.",
        "resultado": "Decisões tomadas com base em dados visuais em vez de planilhas.",
        "funcionalidades": ["Métricas em tempo real", "Gráficos interativos", "Filtros por período", "Exportação", "Responsivo", "Dark mode"],
        "como_funciona": "Dados brutos → API processa → Dashboard exibe → Usuário decide",
        "tecnologias": ["Python", "Flask", "JavaScript", "HTML/CSS", "APIs REST"],
        "imagem": "proj-dashboard.jpg",
        "categoria": ["ia", "web"],
        "github": "https://github.com/JorgeHRP"
    },
    {
        "id": 3,
        "destaque": True,
        "titulo": "Monitoramento de Máquinas em Campo",
        "descricao": "API e dashboard para dados de equipamentos agrícolas e de construção em operação. Tempo real, histórico e alertas automáticos.",
        "descricao_longa": "Sistema completo de monitoramento para frota de máquinas agrícolas e de construção. Coleta dados dos equipamentos em campo, exibe status em tempo real e dispara alertas automáticos quando algo sai do normal.",
        "problema": "Gestores não tinham visibilidade da frota em campo. Falhas eram descobertas tarde, causando paralisações e prejuízos.",
        "solucao": "API de coleta integrada a dashboard com mapa de status, histórico de operação e sistema de alertas por WhatsApp.",
        "resultado": "Visibilidade total da frota. Alertas preventivos antes de falhas críticas.",
        "funcionalidades": ["Coleta em tempo real", "Mapa de status", "Histórico", "Alertas automáticos", "API REST documentada", "Relatórios"],
        "como_funciona": "Máquina envia dados → API coleta → Dashboard exibe → Alerta dispara",
        "tecnologias": ["Python", "Flask", "APIs REST", "JavaScript", "HTML/CSS"],
        "imagem": "proj-monitoring.jpg",
        "categoria": ["web", "ia"],
        "github": "https://github.com/JorgeHRP/documentacao_api"
    },
    {
        "id": 4,
        "destaque": True,
        "titulo": "Sistema de Agendamento Online",
        "descricao": "Plataforma de agendamento para negócio de serviços. Cliente agenda em menos de 1 minuto. Eliminou gestão manual de horários.",
        "descricao_longa": "Sistema de agendamento completo para barbearia. O cliente escolhe serviço, profissional e horário diretamente pelo celular — sem ligar, sem mandar mensagem. O negócio recebe confirmação automática e tem agenda sempre organizada.",
        "problema": "Gestão manual de horários por WhatsApp causava conflitos, esquecimentos e perda de clientes que desistiam de esperar resposta.",
        "solucao": "Plataforma web com calendário em tempo real, confirmação automática e painel de gestão para o estabelecimento.",
        "resultado": "Gestão manual eliminada por completo. Clientes agendam em menos de 1 minuto.",
        "funcionalidades": ["Agendamento em tempo real", "Escolha de profissional", "Confirmação automática", "Painel de gestão", "Histórico", "Mobile-first"],
        "como_funciona": "Cliente escolhe → Sistema verifica → Confirma → Notifica → Registra",
        "tecnologias": ["Python", "Flask", "JavaScript", "HTML/CSS"],
        "imagem": "proj-agendamento.jpg",
        "categoria": ["web"],
        "github": "https://github.com/JorgeHRP/barbearia-agendamento"
    },
    {
        "id": 5,
        "destaque": True,
        "titulo": "Gerador de Orçamentos Profissionais",
        "descricao": "Ferramenta web com blocos reutilizáveis, cálculo automático e layout pronto para envio. De horas para minutos.",
        "descricao_longa": "Sistema de geração de orçamentos para prestadores de serviço. Blocos reutilizáveis, cálculo automático de totais, desconto e impostos — e o orçamento sai formatado e pronto para enviar ao cliente.",
        "problema": "Criar orçamentos tomava horas: copiar de planilhas, formatar, calcular manualmente, adaptar para cada cliente.",
        "solucao": "Ferramenta web com blocos salvos, cálculo automático e geração de orçamento formatado em segundos.",
        "resultado": "Tempo de orçamentação reduzido de horas para minutos.",
        "funcionalidades": ["Blocos reutilizáveis", "Cálculo automático", "Desconto e impostos", "Layout profissional", "Histórico", "Exportação"],
        "como_funciona": "Seleciona blocos → Sistema calcula → Formata → Exporta",
        "tecnologias": ["Python", "Flask", "JavaScript", "HTML/CSS"],
        "imagem": "proj-orcamento.jpg",
        "categoria": ["web"],
        "github": "https://github.com/JorgeHRP/neto"
    },
    {
        "id": 6,
        "destaque": True,
        "titulo": "Bot Telegram com IA 24/7",
        "descricao": "Bot assíncrono que monitora conversas, processa com IA e executa ações via webhooks em sistemas externos.",
        "descricao_longa": "Bot Telegram robusto com Telethon, análise de contexto por IA, detecção de eventos críticos e integração com sistemas externos via webhooks. Roda de forma assíncrona e nunca para.",
        "problema": "Monitoramento manual de grupos Telegram era inviável. Informações críticas se perdiam no volume de mensagens.",
        "solucao": "Bot assíncrono 24/7 com IA detectando mensagens relevantes e disparando ações automáticas nos sistemas certos.",
        "resultado": "100% das mensagens monitoradas. Ação instantânea sem intervenção manual.",
        "funcionalidades": ["Monitoramento 24/7", "Análise IA", "Detecção de eventos", "Webhooks externos", "Comandos custom", "Logs estruturados"],
        "como_funciona": "Monitora → IA analisa → Detecta evento → Executa → Notifica",
        "tecnologias": ["Python", "Telethon", "AsyncIO", "Flask", "Webhooks"],
        "imagem": "proj-telegram.jpg",
        "categoria": ["automacao", "ia"],
        "github": "https://github.com/JorgeHRP/wpp"
    },
]

# ============================================================
# MENCOES HONROSAS — 14 projetos menores, sem modal
# ============================================================
MENCOES = [
    {
        "titulo": "Estratégia Digital — Tecidos América",
        "descricao": "Presença digital B2B para empresa têxtil. Posicionamento, conteúdo e página construídos para captação no mercado certo.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "Landing Pages — Produtos Digitais",
        "descricao": "Diversas páginas de venda para lançamentos de cursos e infoprodutos. Timer, depoimentos, âncoras de preço e checkout integrado.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "FastAçaí — Cardápio Digital",
        "descricao": "Cardápio digital interativo para açaíteria com montagem de pedido e integração com WhatsApp.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "Formulário de Captura de Leads",
        "descricao": "Formulário multi-etapa com validação em tempo real e envio automático para CRM via webhook.",
        "tecnologias": ["HTML", "CSS", "JavaScript", "Webhooks"],
        "categoria": ["web", "automacao"],
    },
    {
        "titulo": "Dashboard de Conteúdo",
        "descricao": "Painel de acompanhamento de métricas de conteúdo digital — alcance, engajamento e conversões.",
        "tecnologias": ["Python", "Flask", "JavaScript"],
        "categoria": ["web", "ia"],
    },
    {
        "titulo": "Estratégia Digital — Tecidos América",
        "descricao": "Presença digital B2B para empresa têxtil. Página institucional com catálogo e captação de clientes.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "Evolution API Railway",
        "descricao": "Deploy e configuração da Evolution API no Railway com variáveis de ambiente e reconexão automática.",
        "tecnologias": ["Evolution API", "Railway", "Node.js"],
        "categoria": ["automacao"],
    },
    {
        "titulo": "Criador de Posts Automático",
        "descricao": "Ferramenta que gera posts formatados para redes sociais a partir de texto simples, com templates editáveis.",
        "tecnologias": ["Python", "HTML/CSS", "JavaScript"],
        "categoria": ["automacao", "ia"],
    },
    {
        "titulo": "Calculadora de Serviços",
        "descricao": "Calculadora web para precificação de serviços profissionais com margens, impostos e custo hora.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "Portfólio de Conteúdo — Cora PUC",
        "descricao": "Site de apresentação de resultados do projeto CORA desenvolvido em parceria com a PUC Goiás.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "Landing Page — Produto Digital",
        "descricao": "Página de vendas para infoproduto com estrutura de lançamento, depoimentos e urgência real.",
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": "Integração Evolution API Avançada",
        "descricao": "Configuração avançada de instâncias WhatsApp com filas, fallback e logs em tempo real.",
        "tecnologias": ["Python", "Evolution API", "Flask"],
        "categoria": ["automacao"],
    },
    {
        "titulo": "Gestor de Rede de Contatos",
        "descricao": "Ferramenta para mapear e organizar rede de contactos profissionais com notas e lembretes de follow-up.",
        "tecnologias": ["Python", "Flask", "HTML/CSS"],
        "categoria": ["web"],
    },
    {
        "titulo": "Sistema de Disparo em Massa",
        "descricao": "Módulo de disparo de mensagens segmentadas via WhatsApp com controle de cadência e relatório de entrega.",
        "tecnologias": ["Python", "Evolution API", "Flask"],
        "categoria": ["automacao", "ia"],
    },
]

HABILIDADES = {
    "Inteligência Artificial": ["OpenAI GPT-4", "Claude AI", "Machine Learning", "Computer Vision", "NLP"],
    "Automação":               ["Evolution API", "Webhooks", "Bots WhatsApp", "Bots Telegram", "Telethon"],
    "Backend":                 ["Python", "Flask", "FastAPI", "AsyncIO", "Supabase"],
    "Frontend":                ["HTML5", "CSS3", "JavaScript", "Responsive Design"],
    "Ferramentas":             ["Git", "Docker", "Railway", "Pandas", "REST APIs"]
}

# ============================================================
# HELPERS
# ============================================================
def get_translation():
    lang = session.get("lang", "pt-br")
    return TRADUCOES.get(lang, TRADUCOES["pt-br"])

def lang_check():
    session.setdefault("lang", "pt-br")

# ============================================================
# ROTAS
# ============================================================
@app.route("/")
def index():
    session.setdefault("lang", "pt-br")
    return redirect(url_for("home"))

@app.route("/set-language/<lang>")
def set_language(lang):
    if lang in TRADUCOES:
        session["lang"] = lang
    return redirect(request.referrer or url_for("home"))

@app.route("/home")
def home():
    lang_check()
    return render_template("index.html", projetos=PROJETOS[:3], t=get_translation())

@app.route("/projetos")
def projetos():
    lang_check()
    return render_template(
        "projetos.html",
        projetos=PROJETOS,
        mencoes=MENCOES,
        t=get_translation()
    )

@app.route("/projeto/<int:projeto_id>")
def projeto_detalhe(projeto_id):
    lang_check()
    projeto = next((p for p in PROJETOS if p["id"] == projeto_id), None)
    if not projeto:
        return redirect(url_for("projetos"))
    return render_template("projeto_detalhe.html", projeto=projeto, t=get_translation())

@app.route("/sobre")
def sobre():
    lang_check()
    return render_template("sobre.html", habilidades=HABILIDADES, t=get_translation())

@app.route("/contato", methods=["GET", "POST"])
def contato():
    lang_check()
    t = get_translation()
    if request.method == "POST":
        dados = {
            "nome":     request.form.get("nome"),
            "email":    request.form.get("email"),
            "assunto":  request.form.get("assunto"),
            "mensagem": request.form.get("mensagem"),
            "data":     datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        if WEBHOOK_URL:
            try:
                r = requests.post(WEBHOOK_URL, json=dados, timeout=10)
                r.raise_for_status()
                flash(t["mensagem_enviada"], "success")
            except Exception:
                flash(t["erro_enviar"], "danger")
        else:
            flash(t["mensagem_enviada"], "success")
        return redirect(url_for("contato"))
    return render_template("contato.html", t=t)

@app.route("/cookies")
def cookies():
    lang_check()
    return render_template("cookies.html", t=get_translation())

@app.route("/privacidade")
def privacidade():
    lang_check()
    return render_template("privacidade.html", t=get_translation())

@app.errorhandler(404)
def page_not_found(e):
    lang_check()
    return render_template("404.html", t=get_translation()), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
