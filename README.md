# 🕵️ Freelance Market Scraper

Um scraper automatizado e resiliente para coletar oportunidades de projetos em plataformas de freelancers (Workana e 99Freelas). Desenvolvido com **SeleniumBase** (modo UC) e **BeautifulSoup**.

## 🚀 Funcionalidades

- **Bypass de Proteções**: Utiliza Undetected ChromeDriver para contornar verificações de bot (Cloudflare).
- **Persistência de Sessão**: Sistema inteligente que exige login manual apenas uma vez, salvando cookies para execuções futuras.
- **Extração Robusta**: Coleta Título, Descrição, Link, Orçamento e Data.
- **Logs Detalhados**: Feedback em tempo real no terminal.
- **Saída Estruturada**: Salva os dados em formato JSONL (JSON Lines) para fácil processamento.

## 🛠️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/NOME_REPO.git
cd scraper-freelas
```

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Como Usar

### 1. Configuração Inicial (Primeiro Acesso)

Execute o script de configuração para realizar o login manual e salvar sua sessão:

```bash
python setup_login.py
```

> Siga as instruções no terminal para fazer login nas plataformas.

### 2. Coleta de Dados

Com a sessão salva, execute o scraper principal:

```bash
python scraper.py
```

Os dados serão salvos em `projetos_coletados.jsonl`.

## ⚠️ Aviso Legal

Este projeto foi desenvolvido para fins de estudo e análise de dados pessoais. O uso de scrapers deve respeitar os Termos de Serviço das plataformas. Não utilize este software para sobrecarregar os servidores dos sites alvo.

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.