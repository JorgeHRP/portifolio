import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-super-secreta")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ============================================
# TRADUÇÕES COMPLETAS
# ============================================
TRADUCOES = {
    "pt-br": {
        "escolha_idioma": "Escolha seu idioma",
        "escolha_subtitulo": "Choose your language | Escolha o seu idioma",
        "portugues_brasil": "Português (Brasil)",
        "portugues_pt": "Português (Portugal)",
        "ingles": "English",
        "pode_mudar": "Você pode mudar o idioma a qualquer momento",
        "inicio": "Início",
        "projetos": "Projetos",
        "sobre": "Sobre",
        "contato": "Contato",
        "hero_ola": "Olá, sou",
        "hero_titulo": "Especialista em IA e Automações",
        "hero_descricao": "Desenvolvedor Full Stack especializado em Inteligência Artificial, automações N8N e soluções web escaláveis.",
        "ver_projetos": "Ver Projetos",
        "entre_contato": "Entre em Contato",
        "projetos_destaque": "Projetos em Destaque",
        "projetos_subtitulo": "Soluções em IA e automações inteligentes",
        "meus_projetos": "Portfólio de Projetos",
        "colecao_trabalhos": "Especializado em IA, automações N8N e desenvolvimento web",
        "filtro_todos": "Todos",
        "filtro_ia": "Inteligência Artificial",
        "filtro_automacao": "Automações N8N",
        "filtro_web": "Aplicações Web",
        "ver_detalhes": "Ver Detalhes",
        "tecnologias": "Tecnologias",
        "fechar": "Fechar",
        "sobre_projeto": "Sobre o Projeto",
        "problema_resolvido": "Problema Resolvido",
        "solucao_implementada": "Solução Implementada",
        "resultados": "Resultados Obtidos",
        "principais_funcionalidades": "Funcionalidades Principais",
        "como_funciona": "Como Funciona",
        "ver_codigo": "Ver Código",
        "ver_workflow": "Ver Workflow",
        "categorias": "Categorias",
        "voltar_projetos": "← Voltar",
        "sobre_mim": "Sobre Mim",
        "conheca_trajetoria": "Especialidades e experiência",
        "dev_apaixonado": "Especialista em IA e Automações",
        "sobre_texto1": "Especializado em criar soluções de Inteligência Artificial e automações com N8N. Transformo processos manuais em fluxos automatizados eficientes.",
        "sobre_texto2": "Experiência em desenvolvimento de agentes de IA, integração com APIs (OpenAI, Claude, Evolution API), processamento de dados e sistemas web robustos.",
        "sobre_texto3": "Cada projeto é desenvolvido com foco em escalabilidade, performance e resultados mensuráveis.",
        "projetos_ia": "Projetos IA",
        "automacoes_n8n": "Automações",
        "anos_experiencia": "Anos",
        "satisfacao_cliente": "Sucesso",
        "minhas_habilidades": "Especialidades",
        "entre_contato_titulo": "Contato",
        "trabalhar_juntos": "Vamos criar soluções inteligentes",
        "vamos_conversar": "Vamos Conversar",
        "vamos_conversar_texto": "Especializado em IA, N8N e desenvolvimento web. Vamos conversar sobre seu projeto.",
        "email": "Email",
        "telefone": "Telefone",
        "localizacao": "Localização",
        "disponibilidade": "Disponibilidade",
        "segunda_sexta": "Seg-Sex, 9h-18h",
        "envie_mensagem": "Envie uma Mensagem",
        "nome_completo": "Nome",
        "seu_nome": "Seu nome",
        "seu_email": "seu@email.com",
        "assunto": "Assunto",
        "como_posso_ajudar": "Como posso ajudar?",
        "mensagem": "Mensagem",
        "conte_projeto": "Conte sobre seu projeto...",
        "enviar_mensagem": "Enviar",
        "mensagem_enviada": "✅ Mensagem enviada!",
        "erro_enviar": "❌ Erro ao enviar",
        "pagina_nao_encontrada": "Página Não Encontrada",
        "ops_pagina": "Página não existe",
        "voltar_home": "Voltar",
        "todos_direitos": "Todos os direitos reservados",
        "desenvolvido_com": "Desenvolvido com ❤️"
    },
    "pt-pt": {
        "escolha_idioma": "Escolha o idioma",
        "escolha_subtitulo": "Choose your language",
        "portugues_brasil": "Português (Brasil)",
        "portugues_pt": "Português (Portugal)",
        "ingles": "English",
        "pode_mudar": "Pode mudar a qualquer momento",
        "inicio": "Início",
        "projetos": "Projectos",
        "sobre": "Sobre",
        "contato": "Contacto",
        "hero_ola": "Olá, sou",
        "hero_titulo": "Especialista em IA e Automações",
        "hero_descricao": "Programador Full Stack especializado em Inteligência Artificial, automações N8N e soluções web escaláveis.",
        "ver_projetos": "Ver Projectos",
        "entre_contato": "Contacto",
        "projetos_destaque": "Projectos Destacados",
        "projetos_subtitulo": "Soluções em IA e automações",
        "meus_projetos": "Portfólio",
        "colecao_trabalhos": "Especializado em IA, N8N e web",
        "filtro_todos": "Todos",
        "filtro_ia": "IA",
        "filtro_automacao": "Automações",
        "filtro_web": "Web",
        "ver_detalhes": "Detalhes",
        "tecnologias": "Tecnologias",
        "fechar": "Fechar",
        "sobre_projeto": "Sobre",
        "problema_resolvido": "Problema",
        "solucao_implementada": "Solução",
        "resultados": "Resultados",
        "principais_funcionalidades": "Funcionalidades",
        "como_funciona": "Como Funciona",
        "ver_codigo": "Código",
        "ver_workflow": "Workflow",
        "categorias": "Categorias",
        "voltar_projetos": "← Voltar",
        "sobre_mim": "Sobre",
        "conheca_trajetoria": "Especialidades",
        "dev_apaixonado": "Especialista IA",
        "sobre_texto1": "Especializado em IA e automações N8N.",
        "sobre_texto2": "Experiência em agentes IA e APIs.",
        "sobre_texto3": "Foco em resultados mensuráveis.",
        "projetos_ia": "IA",
        "automacoes_n8n": "Automações",
        "anos_experiencia": "Anos",
        "satisfacao_cliente": "Sucesso",
        "minhas_habilidades": "Especialidades",
        "entre_contato_titulo": "Contacto",
        "trabalhar_juntos": "Vamos criar soluções",
        "vamos_conversar": "Conversar",
        "vamos_conversar_texto": "IA, N8N e web.",
        "email": "Email",
        "telefone": "Telefone",
        "localizacao": "Local",
        "disponibilidade": "Disponibilidade",
        "segunda_sexta": "Seg-Sex, 9-18h",
        "envie_mensagem": "Mensagem",
        "nome_completo": "Nome",
        "seu_nome": "Nome",
        "seu_email": "email",
        "assunto": "Assunto",
        "como_posso_ajudar": "Como ajudo?",
        "mensagem": "Mensagem",
        "conte_projeto": "Projecto...",
        "enviar_mensagem": "Enviar",
        "mensagem_enviada": "✅ Enviado!",
        "erro_enviar": "❌ Erro",
        "pagina_nao_encontrada": "404",
        "ops_pagina": "Página inexistente",
        "voltar_home": "Voltar",
        "todos_direitos": "Direitos reservados",
        "desenvolvido_com": "Com ❤️"
    },
    "en": {
        "escolha_idioma": "Choose language",
        "escolha_subtitulo": "Select your language",
        "portugues_brasil": "Portuguese (BR)",
        "portugues_pt": "Portuguese (PT)",
        "ingles": "English",
        "pode_mudar": "Change anytime",
        "inicio": "Home",
        "projetos": "Projects",
        "sobre": "About",
        "contato": "Contact",
        "hero_ola": "Hi, I'm",
        "hero_titulo": "AI & Automation Expert",
        "hero_descricao": "Full Stack Developer specialized in AI, N8N automation and scalable web solutions.",
        "ver_projetos": "Projects",
        "entre_contato": "Contact",
        "projetos_destaque": "Featured",
        "projetos_subtitulo": "AI & automation solutions",
        "meus_projetos": "Portfolio",
        "colecao_trabalhos": "AI, N8N & web specialist",
        "filtro_todos": "All",
        "filtro_ia": "AI",
        "filtro_automacao": "Automation",
        "filtro_web": "Web",
        "ver_detalhes": "Details",
        "tecnologias": "Tech",
        "fechar": "Close",
        "sobre_projeto": "About",
        "problema_resolvido": "Problem",
        "solucao_implementada": "Solution",
        "resultados": "Results",
        "principais_funcionalidades": "Features",
        "como_funciona": "How it works",
        "ver_codigo": "Code",
        "ver_workflow": "Workflow",
        "categorias": "Categories",
        "voltar_projetos": "← Back",
        "sobre_mim": "About",
        "conheca_trajetoria": "Expertise",
        "dev_apaixonado": "AI Expert",
        "sobre_texto1": "AI & N8N specialist.",
        "sobre_texto2": "AI agents & APIs.",
        "sobre_texto3": "Results-focused.",
        "projetos_ia": "AI",
        "automacoes_n8n": "Automation",
        "anos_experiencia": "Years",
        "satisfacao_cliente": "Success",
        "minhas_habilidades": "Skills",
        "entre_contato_titulo": "Contact",
        "trabalhar_juntos": "Let's build",
        "vamos_conversar": "Talk",
        "vamos_conversar_texto": "AI, N8N & web.",
        "email": "Email",
        "telefone": "Phone",
        "localizacao": "Location",
        "disponibilidade": "Available",
        "segunda_sexta": "Mon-Fri 9-6",
        "envie_mensagem": "Message",
        "nome_completo": "Name",
        "seu_nome": "Name",
        "seu_email": "email",
        "assunto": "Subject",
        "como_posso_ajudar": "How help?",
        "mensagem": "Message",
        "conte_projeto": "Project...",
        "enviar_mensagem": "Send",
        "mensagem_enviada": "✅ Sent!",
        "erro_enviar": "❌ Error",
        "pagina_nao_encontrada": "404",
        "ops_pagina": "Page not found",
        "voltar_home": "Back",
        "todos_direitos": "All rights reserved",
        "desenvolvido_com": "With ❤️"
    }
}

# PROJETOS COM FOCO EM IA E N8N
PROJETOS = [
    {
        "id": 1,
        "titulo": "Agente IA Multi-Modelo N8N",
        "descricao": "Sistema inteligente que processa imagens e textos usando múltiplos modelos de IA com decisões automatizadas.",
        "descricao_longa": "Workflow N8N avançado implementando agente de IA com processamento multi-modal (GPT-4, Claude), loops de iteração e decisões inteligentes.",
        "problema": "Processar volumes massivos de dados não estruturados manualmente era inviável e propenso a erros.",
        "solucao": "Sistema multi-agente N8N integrando OpenAI e Claude, com loops de processamento em lote, extração de arquivos e envio automático via WhatsApp.",
        "resultados": "80% redução no tempo de processamento | 1000+ itens/hora | 95% precisão",
        "funcionalidades": [
            "Processamento em lote com loops inteligentes",
            "Integração GPT-4 + Claude AI",
            "Extração automática de dados de arquivos",
            "Envio via WhatsApp/Email",
            "Sistema de decisão com IA",
            "Logs e monitoramento real-time"
        ],
        "como_funciona": "Webhook → Loop processa itens → IA analisa → Extrai dados → Envia resultado",
        "tecnologias": ["N8N", "GPT-4", "Claude", "HTTP", "Loops", "Extract File"],
        "icone": "🤖",
        "categoria": ["ia", "automacao"],
        "tipo": "n8n"
    },
    {
        "id": 2,
        "titulo": "Bot Instagram com IA",
        "descricao": "Automação que monitora Instagram, filtra menções e responde automaticamente usando IA contextual.",
        "descricao_longa": "Sistema N8N completo com trigger Instagram, filtros inteligentes e respostas personalizadas via IA.",
        "problema": "Gerenciar menções do Instagram consumia horas diárias de trabalho manual repetitivo.",
        "solucao": "Workflow com trigger Instagram, filtros condicionais e IA gerando respostas contextuais automáticas.",
        "resultados": "Resposta instantânea | 100% menções monitoradas | 45% aumento engajamento",
        "funcionalidades": [
            "Monitor real-time de menções",
            "Filtros por palavra-chave",
            "Respostas IA personalizadas",
            "Contexto via ChatGPT",
            "Dashboard métricas",
            "Alertas críticos"
        ],
        "como_funciona": "Trigger Instagram → Filtra relevância → IA gera resposta → Envia automaticamente",
        "tecnologias": ["N8N", "Instagram API", "OpenAI", "Filters", "HTTP"],
        "icone": "📸",
        "categoria": ["ia", "automacao"],
        "tipo": "n8n"
    },
    {
        "id": 3,
        "titulo": "Pipeline ETL com IA",
        "descricao": "Sistema completo de extração, transformação e análise de dados usando IA para insights automáticos.",
        "descricao_longa": "Pipeline ETL robusto em N8N com 15+ nós, análise preditiva via IA e processamento de 50GB+ diários.",
        "problema": "Dados de múltiplas fontes precisavam ser consolidados e transformados em insights acionáveis.",
        "solucao": "Pipeline automatizado com ingestão multi-fonte, análise de IA, validação de qualidade e armazenamento.",
        "resultados": "50GB+ processados/dia | Insights real-time | 120h/mês economizadas",
        "funcionalidades": [
            "Ingestão multi-fonte",
            "Limpeza e validação auto",
            "Análise preditiva IA",
            "Detecção anomalias",
            "Relatórios automáticos",
            "Alertas WhatsApp"
        ],
        "como_funciona": "Coleta APIs → Valida → IA analisa → Gera insights → Armazena e notifica",
        "tecnologias": ["N8N", "Python", "OpenAI", "HTTP", "Transform", "DB"],
        "icone": "📊",
        "categoria": ["ia", "automacao"],
        "tipo": "n8n"
    },
    {
        "id": 4,
        "titulo": "Sistema Telegram + IA + PDF",
        "descricao": "Captura conversas Telegram, analisa com IA e exporta PDFs profissionais para documentação legal.",
        "descricao_longa": "Plataforma Flask + Telethon que captura mensagens real-time, analisa sentimentos via IA e gera PDFs jurídicos.",
        "problema": "Documentar conversas Telegram profissionalmente para fins legais era trabalhoso e inconsistente.",
        "solucao": "Sistema com Telethon capturando mensagens, análise de IA e geração de PDFs com hash de integridade.",
        "resultados": "1000+ conversas documentadas | PDFs aceitos legalmente | 40h/mês economizadas",
        "funcionalidades": [
            "Captura real-time",
            "Análise sentimento IA",
            "PDF formatação legal",
            "Hash integridade",
            "Interface web",
            "Filtros avançados"
        ],
        "como_funciona": "Telethon captura → Armazena → IA analisa → Gera PDF → Download",
        "tecnologias": ["Flask", "Telethon", "OpenAI", "ReportLab", "Supabase"],
        "icone": "💬",
        "categoria": ["ia", "web"],
        "tipo": "github",
        "github": "https://github.com"
    },
    {
        "id": 5,
        "titulo": "Dashboard WhatsApp + IA",
        "descricao": "Gestão de instâncias WhatsApp com chatbot IA e analytics em tempo real via Evolution API.",
        "descricao_longa": "Plataforma gerenciando múltiplas instâncias WhatsApp, chatbots com IA contextual e métricas detalhadas.",
        "problema": "Gerenciar múltiplos WhatsApp com respostas automáticas inteligentes era desafiador.",
        "solucao": "Dashboard Flask com Evolution API, chatbots OpenAI, sistema de filas e analytics completos.",
        "resultados": "50+ instâncias gerenciadas | 85% resposta auto | 60% satisfação aumentada",
        "funcionalidades": [
            "Multi-instância WhatsApp",
            "Chatbot IA contextual",
            "Fila inteligente",
            "Analytics real-time",
            "Disparo massa",
            "Integração CRM"
        ],
        "como_funciona": "Evolution API → IA processa → Fila distribui → Analytics monitora",
        "tecnologias": ["Flask", "Evolution API", "OpenAI", "Supabase", "JS"],
        "icone": "📱",
        "categoria": ["ia", "web", "automacao"],
        "tipo": "github",
        "github": "https://github.com"
    },
    {
        "id": 6,
        "titulo": "Estoque Inteligente + IA",
        "descricao": "Sistema com IA preditiva que monitora estoque e dispara pedidos automáticos via WhatsApp.",
        "descricao_longa": "App web com ML prevendo demanda, monitorando estoque real-time e automatizando reabastecimento.",
        "problema": "Controle manual causava rupturas frequentes e excesso de inventário.",
        "solucao": "Sistema Flask com ML para previsão, monitoramento auto e pedidos via WhatsApp Evolution API.",
        "resultados": "Zero rupturas 6 meses | 35% redução excesso | ROI 300% em 3 meses",
        "funcionalidades": [
            "Previsão ML demanda",
            "Monitor real-time",
            "Pedidos auto WhatsApp",
            "Gestão fornecedores",
            "Relatórios preditivos",
            "Alertas inteligentes"
        ],
        "como_funciona": "ML prevê → Monitora níveis → Gera pedidos → Envia WhatsApp → Rastreia",
        "tecnologias": ["Flask", "Scikit-learn", "Pandas", "Supabase", "Evolution"],
        "icone": "📦",
        "categoria": ["ia", "web", "automacao"],
        "tipo": "github",
        "github": "https://github.com"
    },
    {
        "id": 7,
        "titulo": "API Processamento Imagens IA",
        "descricao": "FastAPI que analisa e transforma imagens usando Computer Vision e IA automaticamente.",
        "descricao_longa": "API REST performática com modelos de IA para análise, recorte inteligente e otimização de imagens.",
        "problema": "Processar milhares de imagens manualmente consumia dias com resultados inconsistentes.",
        "solucao": "API FastAPI com OpenAI Vision para análise, recorte inteligente e otimização automática.",
        "resultados": "10.000+ imagens/dia | 95% redução tempo | 99% qualidade consistente",
        "funcionalidades": [
            "Análise conteúdo IA",
            "Recorte inteligente",
            "Aplicação logos auto",
            "Otimização qualidade",
            "Geração variações",
            "API RESTful"
        ],
        "como_funciona": "Recebe imagem → IA analisa → Transforma → Otimiza → Retorna",
        "tecnologias": ["FastAPI", "OpenAI Vision", "Pillow", "Python", "CV"],
        "icone": "🖼️",
        "categoria": ["ia", "web"],
        "tipo": "github",
        "github": "https://github.com"
    },
    {
        "id": 8,
        "titulo": "Bot Telegram IA 24/7",
        "descricao": "Bot assíncrono que monitora conversas, processa com IA e executa ações via webhooks.",
        "descricao_longa": "Bot Telegram robusto usando Telethon com IA, análise contextual e integração com sistemas externos.",
        "problema": "Monitoramento manual de grupos Telegram era inviável e informações críticas eram perdidas.",
        "solucao": "Bot assíncrono 24/7 com IA detectando mensagens importantes e notificando sistemas externos.",
        "resultados": "100% mensagens monitoradas | Resposta instantânea | 5+ integrações",
        "funcionalidades": [
            "Monitor 24/7 async",
            "Análise contexto IA",
            "Detecção eventos",
            "Webhooks externos",
            "Comandos custom",
            "Logs estruturados"
        ],
        "como_funciona": "Monitora → IA analisa → Detecta eventos → Executa → Notifica webhooks",
        "tecnologias": ["Telethon", "AsyncIO", "OpenAI", "Flask", "Webhooks"],
        "icone": "🤖",
        "categoria": ["ia", "automacao"],
        "tipo": "github",
        "github": "https://github.com"
    }
]

HABILIDADES = {
    "Inteligência Artificial": ["OpenAI GPT-4", "Claude AI", "Machine Learning", "Computer Vision", "NLP"],
    "Automação Expert": ["N8N Workflows", "API Integration", "Webhooks", "Process Automation"],
    "Backend": ["Python", "Flask", "FastAPI", "Telethon", "Supabase"],
    "Frontend": ["HTML5", "CSS3", "JavaScript", "Responsive Design"],
    "Ferramentas": ["Git", "Docker", "Evolution API", "Pandas"]
}

def get_translation():
    lang = session.get("lang", "pt-br")
    return TRADUCOES.get(lang, TRADUCOES["pt-br"])

@app.route("/")
def language_selector():
    return render_template("language.html", traducoes=TRADUCOES)

@app.route("/set-language/<lang>")
def set_language(lang):
    if lang in TRADUCOES:
        session["lang"] = lang
        return redirect(url_for("home"))
    return redirect(url_for("language_selector"))

@app.route("/home")
def home():
    if not session.get("lang"):
        return redirect(url_for("language_selector"))
    return render_template("index.html", projetos=PROJETOS[:3], t=get_translation())

@app.route("/projetos")
def projetos():
    if not session.get("lang"):
        return redirect(url_for("language_selector"))
    return render_template("projetos.html", projetos=PROJETOS, t=get_translation())

@app.route("/projeto/<int:projeto_id>")
def projeto_detalhe(projeto_id):
    if not session.get("lang"):
        return redirect(url_for("language_selector"))
    projeto = next((p for p in PROJETOS if p["id"] == projeto_id), None)
    if not projeto:
        return redirect(url_for("projetos"))
    return render_template("projeto_detalhe.html", projeto=projeto, t=get_translation())

@app.route("/sobre")
def sobre():
    if not session.get("lang"):
        return redirect(url_for("language_selector"))
    return render_template("sobre.html", habilidades=HABILIDADES, t=get_translation())

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if not session.get("lang"):
        return redirect(url_for("language_selector"))
    
    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome"),
            "email": request.form.get("email"),
            "assunto": request.form.get("assunto"),
            "mensagem": request.form.get("mensagem"),
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        t = get_translation()
        if WEBHOOK_URL:
            try:
                response = requests.post(WEBHOOK_URL, json=dados, timeout=10)
                response.raise_for_status()
                flash(t["mensagem_enviada"], "success")
            except:
                flash(t["erro_enviar"], "danger")
        else:
            flash(t["mensagem_enviada"], "success")
        return redirect(url_for("contato"))
    
    return render_template("contato.html", t=get_translation())

@app.errorhandler(404)
def page_not_found(e):
    lang = session.get("lang", "pt-br")
    return render_template("404.html", t=TRADUCOES[lang]), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)