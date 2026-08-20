from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pathlib import Path
from pypdf import PdfReader
import os
import shutil
import time
import traceback

from config import PATH_FILE, LINK_SIAFI, DOWNLOAD_ROOT, PDF_TEMP
from interface import Interface
from manipulate_excel import Excel
from message_alert import show_message_alert

# Chamando a interface
interface = Interface()
interface.mainloop()

time.sleep(3)

if interface.user is not None:  # Opção Download dos arquivos
    # Configura e inicia o navegador com o Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Inicia maximizado
    prefs = {
        # Isso força o Chrome a baixar o PDF em vez de abri-lo
        "plugins.always_open_pdf_externally": True, 

        # pasta de download 
        "download.default_directory": PDF_TEMP,

        # Desabilita a pergunta "Onde salvar..."
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)  # Define um tempo máximo de espera de 20 segundos
    actions = ActionChains(driver)

    if not os.path.exists(PDF_TEMP):
                os.makedirs(PDF_TEMP)

    if not os.path.exists(DOWNLOAD_ROOT):
                os.makedirs(DOWNLOAD_ROOT)

    try:
        driver.get(LINK_SIAFI)

        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Login')]")
        ))  # Aguardar o texto 'Login' na pag. HTML

        ################################## Logar
        wait.until(EC.visibility_of_element_located(
            (By.ID, "usuario")
        )).send_keys(interface.user)

        wait.until(EC.visibility_of_element_located(
            (By.ID, "senha")
        )).send_keys(interface.password)

        wait.until(EC.visibility_of_element_located(
            (By.ID, "unidexec")
        )).send_keys(interface.unid_exec)

        time.sleep(2)
        ano_siafi = wait.until(EC.visibility_of_element_located(
            (By.ID, "ano")
        ))
        ano_siafi.clear()
        time.sleep(1)
        ano_siafi.send_keys(interface.exercise_year)
        time.sleep(2)

        driver.find_element(By.XPATH, "//*[@value='Prosseguir']").click()
        ##################################
        
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Menu de opções')]")
        ))  # Aguardar o texto 'Menu de opções' na pag. HTML

        driver.find_element(
            By.LINK_TEXT, "Consulta / Impressão Documento Específico"
        ).click()

        excel = Excel(PATH_FILE)
        excel.open()
        first_free_row = excel.first_free_row("A")

        for i in range(interface.begin_line, first_free_row):
            files_before = set(os.listdir(PDF_TEMP))
            numOrdemPagamento = excel.get_cell_value("A", i)

            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'INFORME OS PARÂMETROS')]")
            ))  # Aguardar o texto INFORME OS PARAMETROS na pag. HTML

            print(6)
            driver.find_element(
                By.XPATH, "//td[contains(text(), 'Ordem de Pagamento Bancária')]/input"
            ).click() # Clicar na opção 'Ordem de Pagamento Bancária' no Input Radio

            print(7)
            wait.until(EC.visibility_of_element_located(
                (By.ID, "numOrdemPagamento")
            )).send_keys(numOrdemPagamento)  # Preenche Nº Ordem Pagamento

            print(8)
            driver.find_element(By.ID, "confirmar").click() # Clicar em 'confirmar'

            time.sleep(1.5)

            files_after = set(os.listdir(PDF_TEMP))

            downloaded_file = files_after - files_before

            if not downloaded_file:
                print("AVISO: Nenhum novo arquivo foi detectado após o download.")
                continue

            file_name_temp = downloaded_file.pop()

            download_path_temp = os.path.join(PDF_TEMP, file_name_temp)
            final_download_path = os.path.join(DOWNLOAD_ROOT, f"OP_{numOrdemPagamento}_{str(interface.exercise_year)[-2:]}.pdf")

            shutil.move(download_path_temp, final_download_path)
            
            time.sleep(0.5)

        message = "Download dos arquivos concluído com sucesso!",
        title = "Automação Concluída"

    except TimeoutException:
        message = "[ERRO] O tempo de espera por um elemento foi excedido.\nVerifique sua conexão ou os seletores no código.",
        title = "ERRO"
    except NoSuchElementException as e:
        message = f"[ERRO] Não foi possível encontrar um elemento: {e}.\nO seletor (ID, XPATH, etc.) pode estar incorreto.",
        title = "ERRO"
    except Exception as e:
        message = f"[ERRO] Ocorreu um erro inesperado: {e}",
        title = "ERRO"
    finally:
        excel.close()

        if 'driver' in locals():
            driver.quit()

        show_message_alert(message, title)

elif interface.analyze_selected:  # Analisar e renomear arquivos
    message = "Análise e renomeação de arquivos concluídos!"
    title = "Automação Concluída"

    pdf_list = list(
         Path(DOWNLOAD_ROOT).glob('*.pdf')
    )

    if pdf_list:
        for pdf in pdf_list:
            try:
                reader = PdfReader(pdf)
                pdf_content = ""
                txt_page = ""

                for page in reader.pages:
                    txt_page += page.extract_text()

                    if txt_page:
                        pdf_content += txt_page

                if pdf_content:
                    if not "ACATADA PELO BANCO" in pdf_content:
                        new_pdf = str(pdf).replace(".pdf", "_Não Acatada.pdf")
                        shutil.move(pdf, new_pdf)
                        print(f"arquivo {pdf} renomeado!")

            except Exception as e:
                message = f"Erro ao processar o arquivo {pdf}: {e}\n",
                title = "ERRO"

    show_message_alert(message, title)
