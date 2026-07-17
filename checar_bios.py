"""
Nome do Projeto: Monitor de BIOS Genérico Dinâmico
Versão: 2.0.0
Desenvolvedor: Eduardo Motta
Descrição: Detecta a placa-mãe local e abre a página de suporte dinamicamente no navegador.
"""

import sys
import subprocess
import webbrowser
import msvcrt
import urllib.parse
import time

# Força a saída do terminal a usar UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def obter_dados_sistema():
    try:
        # Comando do PowerShell para pegar o Fabricante e o Modelo da Placa-Mãe
        cmd_placa = "Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product | Format-Table -HideTableHeaders"
        proc_placa = subprocess.check_output(["powershell", "-Command", cmd_placa], text=True)
        linhas_placa = [l.strip() for l in proc_placa.split('\n') if l.strip()]
        
        # Comando do PowerShell para pegar a Versão da BIOS Atual
        cmd_bios = "Get-CimInstance Win32_Bios | Select-Object SMBIOSBIOSVersion | Format-Table -HideTableHeaders"
        proc_bios = subprocess.check_output(["powershell", "-Command", cmd_bios], text=True)
        linhas_bios = [l.strip() for l in proc_bios.split('\n') if l.strip()]

        if linhas_placa and linhas_bios:
            dados_placa = linhas_placa[0].split()
            fabricante = dados_placa[0].upper()
            
            # Limpa strings sujas como "COMPUTER INC." se existirem
            modelo_bruto = " ".join(dados_placa[1:])
            modelo = modelo_bruto.replace("COMPUTER INC.", "").strip()
            
            bios_atual = linhas_bios[0].strip()
            return fabricante, modelo, bios_atual
    except Exception:
        pass
    return None, None, None

def abrir_suporte_dinamico(fabricante, modelo):
    termo_busca = f"{fabricante} {modelo} BIOS support"
    termo_codificado = urllib.parse.quote(termo_busca)
    url_google = f"https://www.google.com/search?q={termo_codificado}"
    
    print(f"\n🌐 Redirecionando para a busca oficial de suporte...")
    webbrowser.open(url_google)

def exibir_interface():
    print("==========================================")
    print("     MONITOR DE BIOS GENÉRICO DINÂMICO    ")
    print("==========================================")
    print("  DESENVOLVEDOR: EDUARDO MOTTA")
    print("  VERSÃO V2.0.0")
    print("==========================================")
    print("")
    
    print("🔍 Identificando seu hardware...")
    fabricante, modelo, bios_atual = obter_dados_sistema()
    
    # Limpa a linha do "Identificando..."
    print("\033[F\033[K", end="") 
    
    if not fabricante or not modelo:
        print("❌ Não foi possível identificar o hardware desta máquina.")
    else:
        print(f" -> FABRICANTE: {fabricante}")
        print(f" -> PLACA-MÃE:  {modelo}")
        print(f" -> BIOS ATUAL: {bios_atual}")
        print("==========================================")
        print("")
        
        print(f"Deseja abrir a página de verificação e download para a {modelo}? (S/N)")
        print("(Isso abrirá uma pesquisa no Google para localizar o suporte oficial do seu hardware)")
        
        # Captura apenas uma tecla sem precisar dar Enter
        resposta = msvcrt.getch().decode('utf-8').upper()
        if resposta == 'S':
            abrir_suporte_dinamico(fabricante, modelo)
        else:
            print("\nOperação cancelada pelo usuário.")
    
    print("\nO programa fechará automaticamente em 10 segundos ou pressione qualquer tecla para sair...")
    
    # Loop de 10 segundos
    for i in range(10, 0, -1):
        print(f"\rFechando em {i}...", end="", flush=True)
        for _ in range(10): # Checa a cada 0.1s para não travar
            time.sleep(0.1)
            if msvcrt.kbhit():
                msvcrt.getch() # Limpa o buffer
                print("\nEncerrado pelo usuário.")
                return
    
    print("\nTempo esgotado. Fechando...")

if __name__ == "__main__":
    exibir_interface()