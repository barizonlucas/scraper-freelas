"""
Authentication Setup Script for Freelance Scraper.

This script initializes a SeleniumBase browser instance to allow manual user login.
It persists the session cookies and local storage into a dedicated Chrome profile directory,
bypassing the need for automated login in subsequent scraper runs.

Usage:
    Run this script once to generate the 'chrome_profile' with valid sessions.
"""

import sys
import time
from pathlib import Path
from seleniumbase import SB

# --- Constants (Configuration) ---
PROFILE_DIR_NAME = "chrome_profile"
WORKANA_LOGIN_URL = "https://www.workana.com/login"
FREELAS_LOGIN_URL = "https://www.99freelas.com.br/login"

# Selectors to verify successful login
WORKANA_SUCCESS_SELECTOR = ".user-menu, img.avatar"
FREELAS_SUCCESS_SELECTOR = ".user-area"

def setup_authentication():
    """
    Launches browser for manual login and saves the session state.
    """
    # Uses pathlib for modern cross-platform path handling
    base_dir = Path.cwd()
    user_data_dir = base_dir / PROFILE_DIR_NAME

    print(f"\n--- 🔐 CONFIGURAÇÃO DE ACESSO ---")
    print(f"📂 Perfil será salvo em: {user_data_dir}")
    print("🚀 Iniciando navegador... Por favor, aguarde.")

    try:
        # guest_mode=False is crucial to allow profile persistence
        with SB(uc=True, user_data_dir=str(user_data_dir), guest_mode=False) as sb:
            
            # --- 1. Workana Setup ---
            print(f"\n[1/2] Acessando Workana...")
            sb.open(WORKANA_LOGIN_URL)
            
            print(">>> 🛑 AÇÃO NECESSÁRIA: Faça o login manualmente no navegador.")
            print(">>> Resolva qualquer CAPTCHA se aparecer.")
            input(">>> Pressione ENTER aqui após logar e ver sua dashboard... ")

            if sb.is_element_visible(WORKANA_SUCCESS_SELECTOR):
                print("✅ Login Workana detectado com sucesso!")
            else:
                print("⚠️  Aviso: Login não detectado automaticamente (verifique se logou).")
            
            # Explicit save helps ensure persistence before navigation
            sb.save_cookies()
            time.sleep(2)

            # --- 2. 99Freelas Setup ---
            print(f"\n[2/2] Acessando 99Freelas...")
            sb.open(FREELAS_LOGIN_URL)
            
            print(">>> 🛑 AÇÃO NECESSÁRIA: Faça o login manualmente.")
            input(">>> Pressione ENTER aqui após logar... ")

            if sb.is_element_visible(FREELAS_SUCCESS_SELECTOR):
                print("✅ Login 99Freelas detectado com sucesso!")
            else:
                print("⚠️  Aviso: Login não detectado automaticamente.")

            sb.save_cookies()
            
            print("\n" + "="*50)
            print("🎉 SUCESSO! Perfil e cookies salvos.")
            print("Agora você pode rodar o 'scraper.py' sem precisar logar novamente.")
            print("="*50)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_authentication()