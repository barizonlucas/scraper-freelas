"""
Freelance Project Scraper
-------------------------
Script responsável por coletar oportunidades de projetos nas plataformas
Workana e 99Freelas utilizando SeleniumBase e BeautifulSoup.

Autor: Lucas Bariza
Data: Janeiro/2026
"""

import json
import random
import time
import logging
from pathlib import Path
from typing import Dict, Any, List

from bs4 import BeautifulSoup
from seleniumbase import SB

# --- Configurações Globais ---
# Diretórios e Arquivos
BASE_DIR = Path.cwd()
PROFILE_DIR = BASE_DIR / "chrome_profile"
OUTPUT_FILE = BASE_DIR / "projetos_coletados.jsonl"

# Configurações de Scraping
MAX_PAGES = 5
MIN_SLEEP = 4.0
MAX_SLEEP = 7.0

# URLs Base
WORKANA_BASE_URL = "https://www.workana.com/jobs?language=pt&publication=1w"
FREELAS_BASE_URL = "https://www.99freelas.com.br/projects"

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class FreelanceScraper:
    """Classe principal para gerenciar o scraping de múltiplos sites."""

    def __init__(self, driver):
        """
        Inicializa o scraper com uma instância do SeleniumBase.
        
        Args:
            driver: Instância ativa do SeleniumBase (SB).
        """
        self.sb = driver

    def _random_sleep(self):
        """Pausa a execução por um tempo aleatório para simular comportamento humano."""
        sleep_time = random.uniform(MIN_SLEEP, MAX_SLEEP)
        time.sleep(sleep_time)

    def _save_data(self, data: Dict[str, Any]):
        """
        Salva um dicionário de dados no arquivo JSONL.
        
        Args:
            data (dict): Dicionário contendo os dados do projeto.
        """
        try:
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        except IOError as e:
            logger.error(f"Erro ao salvar dados no arquivo: {e}")

    def scrape_workana(self):
        """Executa a coleta de dados na plataforma Workana."""
        logger.info(f"--- 🚀 Iniciando Workana (Max Páginas: {MAX_PAGES}) ---")

        for page in range(1, MAX_PAGES + 1):
            # Construção da URL
            url = WORKANA_BASE_URL if page == 1 else f"{WORKANA_BASE_URL}&page={page}"
            
            logger.info(f"📄 Navegando para Página {page}: {url}")
            self.sb.open(url)
            self._random_sleep()

            soup = BeautifulSoup(self.sb.get_page_source(), 'html.parser')
            
            # Estratégia de fallback para seletores
            projetos = soup.find_all("div", class_="project-item")
            if not projetos:
                projetos = soup.find_all("div", id=lambda x: x and x.startswith('project-'))

            logger.info(f"   -> Encontrados {len(projetos)} projetos.")

            if not projetos and page == 1:
                logger.warning("❌ Erro crítico: Nenhum projeto na pág 1. Verifique Login/Seletores.")
                return

            self._extract_workana_projects(projetos)

        logger.info("✅ Workana finalizado.")

    def _extract_workana_projects(self, projetos: List[BeautifulSoup]):
        """Extrai e salva dados de uma lista de elementos do Workana."""
        for proj in projetos:
            try:
                titulo_elem = proj.find("h2") or proj.find("h3")
                if not titulo_elem: continue

                titulo = titulo_elem.get_text(strip=True)
                link_tag = titulo_elem.find("a")
                link = "https://www.workana.com" + link_tag['href'] if link_tag else "N/A"
                
                desc_elem = proj.find(class_="expander") or proj.find(class_="project-body")
                desc = desc_elem.get_text(strip=True) if desc_elem else "Sem descrição"
                
                orcamento_elem = proj.find(class_="values")
                orcamento = orcamento_elem.get_text(strip=True) if orcamento_elem else "A combinar"

                self._save_data({
                    "plataforma": "Workana",
                    "titulo": titulo,
                    "link": link,
                    "descricao": desc,
                    "orcamento": orcamento,
                    "data_coleta": time.strftime("%Y-%m-%d")
                })
            except Exception as e:
                logger.error(f"Erro ao extrair projeto Workana: {e}")
                continue

    def scrape_99freelas(self):
        """Executa a coleta de dados na plataforma 99Freelas."""
        logger.info(f"\n--- 🚀 Iniciando 99Freelas (Max Páginas: {MAX_PAGES}) ---")

        for page in range(1, MAX_PAGES + 1):
            url = FREELAS_BASE_URL if page == 1 else f"{FREELAS_BASE_URL}?page={page}"
            
            logger.info(f"📄 Navegando para Página {page}...")
            self.sb.open(url)
            self._random_sleep()

            soup = BeautifulSoup(self.sb.get_page_source(), 'html.parser')

            # Seletores principais e fallback
            projetos = soup.find_all("li", class_="result-item")
            if not projetos:
                containers = soup.find_all("div", class_="projects-result-list")
                if containers:
                    projetos = containers[0].find_all("li")
            
            logger.info(f"   -> Encontrados {len(projetos)} projetos.")
            
            self._extract_99freelas_projects(projetos)

        logger.info("✅ 99Freelas finalizado.")

    def _extract_99freelas_projects(self, projetos: List[BeautifulSoup]):
        """Extrai e salva dados de uma lista de elementos do 99Freelas."""
        for proj in projetos:
            try:
                title_elem = proj.find("h1", class_="title") or proj.find("h2", class_="title")
                if not title_elem: continue
                
                titulo = title_elem.get_text(strip=True)
                link_tag = title_elem.find("a")
                link = "https://www.99freelas.com.br" + link_tag['href'] if link_tag else "N/A"
                
                desc_elem = proj.find("div", class_="description")
                desc = desc_elem.get_text(strip=True) if desc_elem else ""
                
                self._save_data({
                    "plataforma": "99Freelas",
                    "titulo": titulo,
                    "link": link,
                    "descricao": desc,
                    "data_coleta": time.strftime("%Y-%m-%d")
                })
            except Exception as e:
                logger.error(f"Erro ao extrair projeto 99Freelas: {e}")
                continue


def main():
    """Função principal de execução."""
    # Cria diretório de perfil se não existir
    if not PROFILE_DIR.exists():
        PROFILE_DIR.mkdir()

    logger.info(f"Iniciando Browser. Perfil: {PROFILE_DIR}")

    # Inicializa o SeleniumBase com as configurações
    with SB(uc=True, user_data_dir=str(PROFILE_DIR)) as sb:
        scraper = FreelanceScraper(sb)
        
        # Executa os scrapers
        scraper.scrape_workana()
        scraper.scrape_99freelas()

if __name__ == "__main__":
    main()