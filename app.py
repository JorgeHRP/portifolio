import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from translations import get_translation

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-super-secreta")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ============================================================
# PROJETOS DESTAQUE — 6 com modal completo
# Campos textuais são dicts {"pt-br": ..., "en": ...} e são
# resolvidos para o idioma da sessão por localizar_projetos().
# ============================================================
PROJETOS = [
    {
        "id": 1,
        "destaque": True,
        "titulo": {
            "pt-br": "Automação de Atendimento via WhatsApp",
            "en": "WhatsApp Customer Service Automation",
        },
        "descricao": {
            "pt-br": "Sistema de atendimento automático integrado com API Oficial. Backend em Python com sessão persistente, health check e deploy em nuvem.",
            "en": "Automated customer service system integrated with the Official API. Python backend with persistent session, health check and cloud deployment.",
        },
        "descricao_longa": {
            "pt-br": "Sistema completo de atendimento via WhatsApp usando a principal API open-source do mercado. O bot mantém contexto da conversa, responde de forma humanizada e nunca cai — sessão persistente com reconexão automática e health check monitorado 24/7.",
            "en": "Complete WhatsApp customer service system built on the market's leading open-source API. The bot keeps conversation context, replies in a human-like way and never goes down — persistent session with automatic reconnection and health check monitored 24/7.",
        },
        "problema": {
            "pt-br": "O cliente perdia leads fora do horário comercial. Sem atendimento automático, mensagens ficavam sem resposta por horas.",
            "en": "The client was losing leads outside business hours. Without automated service, messages went unanswered for hours.",
        },
        "solucao": {
            "pt-br": "Bot Python com Telethon + API Oficial rodando 24/7 em nuvem. Sessão persistente, reconexão automática, health check e deploy no Railway com zero downtime.",
            "en": "Python bot with Telethon + Official API running 24/7 in the cloud. Persistent session, automatic reconnection, health check and zero-downtime deployment on Railway.",
        },
        "resultado": {
            "pt-br": "Zero leads perdidos fora do horário comercial. Atendimento instantâneo 24/7.",
            "en": "Zero leads lost outside business hours. Instant 24/7 service.",
        },
        "funcionalidades": {
            "pt-br": ["Atendimento 24/7", "Sessão persistente", "Health check", "Deploy Railway", "Logs estruturados", "API Oficial"],
            "en": ["24/7 Service", "Persistent Session", "Health Check", "Railway Deploy", "Structured Logs", "Official API"],
        },
        "como_funciona": {
            "pt-br": "Mensagem chega → Bot processa → Responde → Loga → Monitora",
            "en": "Message arrives → Bot processes → Replies → Logs → Monitors",
        },
        "tecnologias": ["Python", "Telethon", "Flask", "API Oficial", "Railway"],
        "imagem": "proj-whatsapp.jpg",
        "categoria": ["automacao", "ia"],
        "github": "https://github.com/JorgeHRP"
    },
    {
        "id": 2,
        "destaque": True,
        "titulo": {
            "pt-br": "Dashboard de Inteligência Artificial",
            "en": "Artificial Intelligence Dashboard",
        },
        "descricao": {
            "pt-br": "Painel de resultados para projeto de IA universitário. Métricas em tempo real para público técnico e não técnico.",
            "en": "Results panel for a university AI project. Real-time metrics for both technical and non-technical audiences.",
        },
        "descricao_longa": {
            "pt-br": "Dashboard desenvolvido para apresentação de resultados de projeto de IA em ambiente universitário. Dados em tempo real, gráficos interativos e layout pensado para ser lido por qualquer audiência.",
            "en": "Dashboard built to present AI project results in a university setting. Real-time data, interactive charts and a layout designed to be read by any audience.",
        },
        "problema": {
            "pt-br": "Os resultados do projeto de IA existiam apenas em arquivos e logs. Era impossível apresentá-los de forma clara para diferentes públicos.",
            "en": "The AI project's results existed only in files and logs. It was impossible to present them clearly to different audiences.",
        },
        "solucao": {
            "pt-br": "Dashboard Flask com visualizações em tempo real, filtragem por período e exportação de relatórios em dark theme.",
            "en": "Flask dashboard with real-time visualizations, filtering by period and report export in dark theme.",
        },
        "resultado": {
            "pt-br": "Decisões tomadas com base em dados visuais em vez de planilhas.",
            "en": "Decisions made based on visual data instead of spreadsheets.",
        },
        "funcionalidades": {
            "pt-br": ["Métricas em tempo real", "Gráficos interativos", "Filtros por período", "Exportação", "Responsivo", "Dark mode"],
            "en": ["Real-time Metrics", "Interactive Charts", "Period Filters", "Export", "Responsive", "Dark Mode"],
        },
        "como_funciona": {
            "pt-br": "Dados brutos → API processa → Dashboard exibe → Usuário decide",
            "en": "Raw data → API processes → Dashboard displays → User decides",
        },
        "tecnologias": ["Python", "Flask", "JavaScript", "HTML/CSS", "APIs REST"],
        "imagem": "proj-dashboard.jpg",
        "categoria": ["ia", "web"],
        "github": "https://github.com/JorgeHRP"
    },
    {
        "id": 3,
        "destaque": True,
        "titulo": {
            "pt-br": "Monitoramento de Máquinas em Campo",
            "en": "Field Equipment Monitoring",
        },
        "descricao": {
            "pt-br": "API e dashboard para dados de equipamentos agrícolas e de construção em operação. Tempo real, histórico e alertas automáticos.",
            "en": "API and dashboard for agricultural and construction equipment data in the field. Real-time, history and automatic alerts.",
        },
        "descricao_longa": {
            "pt-br": "Sistema completo de monitoramento para frota de máquinas agrícolas e de construção. Coleta dados dos equipamentos em campo, exibe status em tempo real e dispara alertas automáticos quando algo sai do normal.",
            "en": "Complete monitoring system for a fleet of agricultural and construction machines. Collects data from equipment in the field, shows real-time status and triggers automatic alerts when something is off.",
        },
        "problema": {
            "pt-br": "Gestores não tinham visibilidade da frota em campo. Falhas eram descobertas tarde, causando paralisações e prejuízos.",
            "en": "Managers had no visibility into the field fleet. Failures were discovered late, causing downtime and losses.",
        },
        "solucao": {
            "pt-br": "API de coleta integrada a dashboard com mapa de status, histórico de operação e sistema de alertas por WhatsApp.",
            "en": "Data collection API integrated with a dashboard featuring a status map, operation history and WhatsApp alert system.",
        },
        "resultado": {
            "pt-br": "Visibilidade total da frota. Alertas preventivos antes de falhas críticas.",
            "en": "Full fleet visibility. Preventive alerts before critical failures.",
        },
        "funcionalidades": {
            "pt-br": ["Coleta em tempo real", "Mapa de status", "Histórico", "Alertas automáticos", "API REST documentada", "Relatórios"],
            "en": ["Real-time Collection", "Status Map", "History", "Automatic Alerts", "Documented REST API", "Reports"],
        },
        "como_funciona": {
            "pt-br": "Máquina envia dados → API coleta → Dashboard exibe → Alerta dispara",
            "en": "Machine sends data → API collects → Dashboard displays → Alert triggers",
        },
        "tecnologias": ["Python", "Flask", "APIs REST", "JavaScript", "HTML/CSS"],
        "imagem": "proj-monitoring.jpg",
        "categoria": ["web", "ia"],
        "github": "https://github.com/JorgeHRP/documentacao_api"
    },
    {
        "id": 4,
        "destaque": True,
        "titulo": {
            "pt-br": "Sistema de Agendamento Online",
            "en": "Online Booking System",
        },
        "descricao": {
            "pt-br": "Plataforma de agendamento para negócio de serviços. Cliente agenda em menos de 1 minuto. Eliminou gestão manual de horários.",
            "en": "Booking platform for a service business. Customers book in under 1 minute. Eliminated manual schedule management.",
        },
        "descricao_longa": {
            "pt-br": "Sistema de agendamento completo para barbearia. O cliente escolhe serviço, profissional e horário diretamente pelo celular — sem ligar, sem mandar mensagem. O negócio recebe confirmação automática e tem agenda sempre organizada.",
            "en": "Complete booking system for a barbershop. The customer chooses service, professional and time directly from their phone — no calls, no messages. The business gets automatic confirmation and always has an organized schedule.",
        },
        "problema": {
            "pt-br": "Gestão manual de horários por WhatsApp causava conflitos, esquecimentos e perda de clientes que desistiam de esperar resposta.",
            "en": "Manual schedule management via WhatsApp caused conflicts, missed appointments and lost customers who gave up waiting for a reply.",
        },
        "solucao": {
            "pt-br": "Plataforma web com calendário em tempo real, confirmação automática e painel de gestão para o estabelecimento.",
            "en": "Web platform with a real-time calendar, automatic confirmation and a management panel for the business.",
        },
        "resultado": {
            "pt-br": "Gestão manual eliminada por completo. Clientes agendam em menos de 1 minuto.",
            "en": "Manual management completely eliminated. Customers book in under 1 minute.",
        },
        "funcionalidades": {
            "pt-br": ["Agendamento em tempo real", "Escolha de profissional", "Confirmação automática", "Painel de gestão", "Histórico", "Mobile-first"],
            "en": ["Real-time Booking", "Professional Selection", "Automatic Confirmation", "Management Panel", "History", "Mobile-first"],
        },
        "como_funciona": {
            "pt-br": "Cliente escolhe → Sistema verifica → Confirma → Notifica → Registra",
            "en": "Customer chooses → System checks → Confirms → Notifies → Records",
        },
        "tecnologias": ["Python", "Flask", "JavaScript", "HTML/CSS"],
        "imagem": "proj-agendamento.jpg",
        "categoria": ["web"],
        "github": "https://github.com/JorgeHRP/barbearia-agendamento"
    },
    {
        "id": 5,
        "destaque": True,
        "titulo": {
            "pt-br": "Gerador de Orçamentos Profissionais",
            "en": "Professional Quote Generator",
        },
        "descricao": {
            "pt-br": "Ferramenta web com blocos reutilizáveis, cálculo automático e layout pronto para envio. De horas para minutos.",
            "en": "Web tool with reusable blocks, automatic calculation and a layout ready to send. From hours to minutes.",
        },
        "descricao_longa": {
            "pt-br": "Sistema de geração de orçamentos para prestadores de serviço. Blocos reutilizáveis, cálculo automático de totais, desconto e impostos — e o orçamento sai formatado e pronto para enviar ao cliente.",
            "en": "Quote generation system for service providers. Reusable blocks, automatic calculation of totals, discounts and taxes — and the quote comes out formatted and ready to send to the client.",
        },
        "problema": {
            "pt-br": "Criar orçamentos tomava horas: copiar de planilhas, formatar, calcular manualmente, adaptar para cada cliente.",
            "en": "Creating quotes took hours: copying from spreadsheets, formatting, calculating manually, adapting for each client.",
        },
        "solucao": {
            "pt-br": "Ferramenta web com blocos salvos, cálculo automático e geração de orçamento formatado em segundos.",
            "en": "Web tool with saved blocks, automatic calculation and formatted quote generation in seconds.",
        },
        "resultado": {
            "pt-br": "Tempo de orçamentação reduzido de horas para minutos.",
            "en": "Quoting time reduced from hours to minutes.",
        },
        "funcionalidades": {
            "pt-br": ["Blocos reutilizáveis", "Cálculo automático", "Desconto e impostos", "Layout profissional", "Histórico", "Exportação"],
            "en": ["Reusable Blocks", "Automatic Calculation", "Discounts & Taxes", "Professional Layout", "History", "Export"],
        },
        "como_funciona": {
            "pt-br": "Seleciona blocos → Sistema calcula → Formata → Exporta",
            "en": "Selects blocks → System calculates → Formats → Exports",
        },
        "tecnologias": ["Python", "Flask", "JavaScript", "HTML/CSS"],
        "imagem": "proj-orcamento.jpg",
        "categoria": ["web"],
        "github": "https://github.com/JorgeHRP/neto"
    },
    {
        "id": 6,
        "destaque": True,
        "titulo": {
            "pt-br": "Bot Telegram com IA 24/7",
            "en": "24/7 AI-Powered Telegram Bot",
        },
        "descricao": {
            "pt-br": "Bot assíncrono que monitora conversas, processa com IA e executa ações via webhooks em sistemas externos.",
            "en": "Asynchronous bot that monitors conversations, processes them with AI and triggers actions via webhooks in external systems.",
        },
        "descricao_longa": {
            "pt-br": "Bot Telegram robusto com Telethon, análise de contexto por IA, detecção de eventos críticos e integração com sistemas externos via webhooks. Roda de forma assíncrona e nunca para.",
            "en": "Robust Telegram bot with Telethon, AI-powered context analysis, critical event detection and integration with external systems via webhooks. Runs asynchronously and never stops.",
        },
        "problema": {
            "pt-br": "Monitoramento manual de grupos Telegram era inviável. Informações críticas se perdiam no volume de mensagens.",
            "en": "Manually monitoring Telegram groups was unfeasible. Critical information got lost in the volume of messages.",
        },
        "solucao": {
            "pt-br": "Bot assíncrono 24/7 com IA detectando mensagens relevantes e disparando ações automáticas nos sistemas certos.",
            "en": "24/7 asynchronous bot with AI detecting relevant messages and triggering automatic actions in the right systems.",
        },
        "resultado": {
            "pt-br": "100% das mensagens monitoradas. Ação instantânea sem intervenção manual.",
            "en": "100% of messages monitored. Instant action with no manual intervention.",
        },
        "funcionalidades": {
            "pt-br": ["Monitoramento 24/7", "Análise IA", "Detecção de eventos", "Webhooks externos", "Comandos custom", "Logs estruturados"],
            "en": ["24/7 Monitoring", "AI Analysis", "Event Detection", "External Webhooks", "Custom Commands", "Structured Logs"],
        },
        "como_funciona": {
            "pt-br": "Monitora → IA analisa → Detecta evento → Executa → Notifica",
            "en": "Monitors → AI analyzes → Detects event → Executes → Notifies",
        },
        "tecnologias": ["Python", "Telethon", "AsyncIO", "Flask", "Webhooks"],
        "imagem": "proj-telegram.jpg",
        "categoria": ["automacao", "ia"],
        "github": "https://github.com/JorgeHRP/wpp"
    },
]

# ============================================================
# MAIS PROJETOS — projetos menores, sem modal
# ============================================================
MAIS_PROJETOS = [
    {
        "titulo": {"pt-br": "Estratégia Digital — Tecidos América", "en": "Digital Strategy — Tecidos América"},
        "descricao": {
            "pt-br": "Presença digital B2B para empresa têxtil. Posicionamento, conteúdo e página construídos para captação no mercado certo.",
            "en": "B2B digital presence for a textile company. Positioning, content and page built to attract the right market.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "Landing Pages — Produtos Digitais", "en": "Landing Pages — Digital Products"},
        "descricao": {
            "pt-br": "Diversas páginas de venda para lançamentos de cursos e infoprodutos. Timer, depoimentos, âncoras de preço e checkout integrado.",
            "en": "Several sales pages for course and digital product launches. Countdown timer, testimonials, price anchoring and integrated checkout.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "FastAçaí — Cardápio Digital", "en": "FastAçaí — Digital Menu"},
        "descricao": {
            "pt-br": "Cardápio digital interativo para açaíteria com montagem de pedido e integração com WhatsApp.",
            "en": "Interactive digital menu for an açaí shop with order builder and WhatsApp integration.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "Formulário de Captura de Leads", "en": "Lead Capture Form"},
        "descricao": {
            "pt-br": "Formulário multi-etapa com validação em tempo real e envio automático para CRM via webhook.",
            "en": "Multi-step form with real-time validation and automatic submission to CRM via webhook.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript", "Webhooks"],
        "categoria": ["web", "automacao"],
    },
    {
        "titulo": {"pt-br": "Dashboard de Conteúdo", "en": "Content Dashboard"},
        "descricao": {
            "pt-br": "Painel de acompanhamento de métricas de conteúdo digital — alcance, engajamento e conversões.",
            "en": "Tracking panel for digital content metrics — reach, engagement and conversions.",
        },
        "tecnologias": ["Python", "Flask", "JavaScript"],
        "categoria": ["web", "ia"],
    },
    {
        "titulo": {"pt-br": "Evolution API Railway", "en": "Evolution API on Railway"},
        "descricao": {
            "pt-br": "Deploy e configuração da Evolution API no Railway com variáveis de ambiente e reconexão automática.",
            "en": "Deployment and configuration of the Evolution API on Railway with environment variables and automatic reconnection.",
        },
        "tecnologias": ["Evolution API", "Railway", "Node.js"],
        "categoria": ["automacao"],
    },
    {
        "titulo": {"pt-br": "Criador de Posts Automático", "en": "Automatic Post Creator"},
        "descricao": {
            "pt-br": "Ferramenta que gera posts formatados para redes sociais a partir de texto simples, com templates editáveis.",
            "en": "Tool that generates formatted social media posts from plain text, with editable templates.",
        },
        "tecnologias": ["Python", "HTML/CSS", "JavaScript"],
        "categoria": ["automacao", "ia"],
    },
    {
        "titulo": {"pt-br": "Calculadora de Serviços", "en": "Service Pricing Calculator"},
        "descricao": {
            "pt-br": "Calculadora web para precificação de serviços profissionais com margens, impostos e custo hora.",
            "en": "Web calculator for pricing professional services with margins, taxes and hourly cost.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "Portfólio de Conteúdo — Cora PUC", "en": "Content Portfolio — Cora PUC"},
        "descricao": {
            "pt-br": "Site de apresentação de resultados do projeto CORA desenvolvido em parceria com a PUC Goiás.",
            "en": "Results showcase site for the CORA project, developed in partnership with PUC Goiás.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "Landing Page — Produto Digital", "en": "Landing Page — Digital Product"},
        "descricao": {
            "pt-br": "Página de vendas para infoproduto com estrutura de lançamento, depoimentos e urgência real.",
            "en": "Sales page for a digital product with launch structure, testimonials and real urgency.",
        },
        "tecnologias": ["HTML", "CSS", "JavaScript"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "Integração Evolution API Avançada", "en": "Advanced Evolution API Integration"},
        "descricao": {
            "pt-br": "Configuração avançada de instâncias WhatsApp com filas, fallback e logs em tempo real.",
            "en": "Advanced configuration of WhatsApp instances with queues, fallback and real-time logs.",
        },
        "tecnologias": ["Python", "Evolution API", "Flask"],
        "categoria": ["automacao"],
    },
    {
        "titulo": {"pt-br": "Gestor de Rede de Contatos", "en": "Contact Network Manager"},
        "descricao": {
            "pt-br": "Ferramenta para mapear e organizar rede de contactos profissionais com notas e lembretes de follow-up.",
            "en": "Tool to map and organize a professional contact network with notes and follow-up reminders.",
        },
        "tecnologias": ["Python", "Flask", "HTML/CSS"],
        "categoria": ["web"],
    },
    {
        "titulo": {"pt-br": "Sistema de Disparo em Massa", "en": "Mass Messaging System"},
        "descricao": {
            "pt-br": "Módulo de disparo de mensagens segmentadas via WhatsApp com controle de cadência e relatório de entrega.",
            "en": "Module for sending segmented WhatsApp messages with cadence control and delivery reporting.",
        },
        "tecnologias": ["Python", "API Oficial", "Flask"],
        "categoria": ["automacao", "ia"],
    },
]

HABILIDADES = {
    "pt-br": {
        "Inteligência Artificial": ["OpenAI GPT-4", "Claude AI", "Machine Learning", "Computer Vision", "NLP"],
        "Automação":               ["API Oficial WhatsApp", "Webhooks", "Bots WhatsApp", "Bots Telegram", "Telethon"],
        "Backend":                 ["Python", "Flask", "FastAPI", "AsyncIO", "Supabase"],
        "Frontend":                ["HTML5", "CSS3", "JavaScript", "Responsive Design"],
        "Ferramentas":             ["Git", "Docker", "Railway", "Pandas", "REST APIs"],
    },
    "en": {
        "Artificial Intelligence": ["OpenAI GPT-4", "Claude AI", "Machine Learning", "Computer Vision", "NLP"],
        "Automation":              ["Official WhatsApp API", "Webhooks", "WhatsApp Bots", "Telegram Bots", "Telethon"],
        "Backend":                 ["Python", "Flask", "FastAPI", "AsyncIO", "Supabase"],
        "Frontend":                ["HTML5", "CSS3", "JavaScript", "Responsive Design"],
        "Tools":                   ["Git", "Docker", "Railway", "Pandas", "REST APIs"],
    },
}

# ============================================================
# HELPERS
# ============================================================
def _loc(campo, lang):
    if isinstance(campo, dict):
        return campo.get(lang, campo.get("pt-br"))
    return campo

def localizar_projetos(lista, lang):
    campos = ("titulo", "descricao", "descricao_longa", "problema", "solucao", "resultado", "funcionalidades", "como_funciona")
    localizados = []
    for item in lista:
        novo = dict(item)
        for campo in campos:
            if campo in novo:
                novo[campo] = _loc(novo[campo], lang)
        localizados.append(novo)
    return localizados

def lang_check():
    session.setdefault("lang", "en")

# ============================================================
# ROTAS
# ============================================================
@app.route("/")
def index():
    session.setdefault("lang", "en")
    return redirect(url_for("home"))

@app.route("/set-language/<lang>")
def set_language(lang):
    from translations import get_translation as _gt
    if lang in ("pt-br", "en"):
        session["lang"] = lang
    return redirect(request.referrer or url_for("home"))

@app.route("/home")
def home():
    lang_check()
    lang = session["lang"]
    return render_template("index.html", projetos=localizar_projetos(PROJETOS, lang)[:3], t=get_translation(lang))

@app.route("/projetos")
def projetos():
    lang_check()
    lang = session["lang"]
    return render_template(
        "projetos.html",
        projetos=localizar_projetos(PROJETOS, lang),
        mais_projetos=localizar_projetos(MAIS_PROJETOS, lang),
        t=get_translation(lang)
    )

@app.route("/projeto/<int:projeto_id>")
def projeto_detalhe(projeto_id):
    lang_check()
    lang = session["lang"]
    projeto = next((p for p in PROJETOS if p["id"] == projeto_id), None)
    if not projeto:
        return redirect(url_for("projetos"))
    projeto = localizar_projetos([projeto], lang)[0]
    return render_template("projeto_detalhe.html", projeto=projeto, t=get_translation(lang))

@app.route("/sobre")
def sobre():
    lang_check()
    lang = session["lang"]
    habilidades = HABILIDADES.get(lang, HABILIDADES["pt-br"])
    return render_template("sobre.html", habilidades=habilidades, t=get_translation(lang))

@app.route("/contato", methods=["GET", "POST"])
def contato():
    lang_check()
    t = get_translation(session["lang"])
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
    return render_template("cookies.html", t=get_translation(session["lang"]))

@app.route("/privacidade")
def privacidade():
    lang_check()
    return render_template("privacidade.html", t=get_translation(session["lang"]))

@app.errorhandler(404)
def page_not_found(e):
    lang_check()
    return render_template("404.html", t=get_translation(session["lang"])), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)