import random
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar
import os
import matplotlib.pyplot as plt

# Função para exibir a mensagem inicial
def mensagem_inicial():
    messagebox.showinfo("Bem-vindo", 
                        "Prezada Professora, os dados do estacionamento serão coletados por sensores ultrassônicos conectados a um dispositivo Arduino.\n"
                        "Esses dados serão enviados via Wi-Fi para um servidor, que armazenará e analisará as informações em tempo real. Os motoristas poderão visualizar as vagas disponíveis através de um aplicativo no celular, otimizando a mobilidade e eliminando a necessidade de procurar vagas.\n"
                        "Além disso, relatórios detalhados serão gerados, permitindo uma análise minuciosa. O sistema oferece gráficos para facilitar a interpretação dos dados, incluindo Análise por Período, Pico de Ocupação e Capacidade.\n"
                        "Se precisar de mais ajustes estamos a disposição.")

# Função para exibir o menu principal
def menu_principal():
    menu = simpledialog.askstring("Menu Principal", 
                                   "1. Gostaria de analisar algum mês específico?\n"
                                   "2. Ver o estacionamento em tempo real\n"
                                   "3. Gerar relatório do mês\n"
                                   "4. Sair\n"
                                   "Escolha uma opção (1, 2, 3 ou 4):")
    return menu

# Função para exibir o submenu de análise
def submenu_analise():
    opcao = simpledialog.askstring("Opções de Análise", 
                                   "1. Análise por Período (Manhã, Tarde, Noite)\n"
                                   "2. Análise de Picos de Ocupação\n"
                                   "3. Análise de Capacidade\n"
                                   "4. Retornar ao menu anterior\n"
                                   "5. Sair\n"
                                   "Escolha uma opção (1 a 5):")
    return opcao

# Função para analisar mês específico e gerar dados se necessário
def analisar_mes_especifico():
    while True:
        try:
            mes = int(simpledialog.askstring("Análise de Mês", "Qual mês gostaria de analisar (Digite um número de 1 a 12)?"))
            ano = int(simpledialog.askstring("Análise de Ano", 
                                              "Digite 1 para 2021, 2 para 2022, 3 para 2023 ou 4 para 2024:")) + 2020
            if 1 <= mes <= 12:  # Verifica se o mês está no intervalo válido
                # Verifica se existe um relatório salvo
                nome_arquivo = f"relatorio_ocupacao_vagas_{mes}_{ano}.xlsx"
                if os.path.exists(nome_arquivo):
                    messagebox.showinfo("Relatório encontrado", "Relatório existente encontrado e será utilizado para análise.")
                    df = pd.read_excel(nome_arquivo, index_col='Dia')
                    dados_vagas = df.to_dict(orient='index')
                else:
                    # Gera dados aleatórios para todo o mês se o arquivo não existir
                    messagebox.showinfo("Relatório não encontrado", "Nenhum relatório encontrado para este mês, gerando dados aleatórios.")
                    dados_vagas = gerar_dados_aleatorios_automaticamente(mes, ano)
                    salvar_em_excel(dados_vagas, mes, ano)
                return mes, ano, dados_vagas
            else:
                messagebox.showwarning("Mês Inválido", "Por favor, digite um mês válido entre 1 e 12.")
        except (ValueError, TypeError):
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um número válido.")

# Função para gerar dados aleatórios automaticamente para todo o mês
def gerar_dados_aleatorios_automaticamente(mes, ano):
    dados_vagas = {}
    for i in range(1, calendar.monthrange(ano, mes)[1] + 1):
        dados_vagas[i] = {
            'manha': random.randint(1, 50),
            'tarde': random.randint(1, 50),
            'noite': random.randint(1, 50)
        }
    return dados_vagas

# Função para salvar os dados em um arquivo Excel
def salvar_em_excel(dados_vagas, mes, ano):
    nome_arquivo = f"relatorio_ocupacao_vagas_{mes}_{ano}.xlsx"
    
    try:
        # Cria um novo DataFrame
        df = pd.DataFrame.from_dict(dados_vagas, orient='index')
        
        # Salva o DataFrame em um novo arquivo Excel
        df.to_excel(nome_arquivo, index_label='Dia')

        # Cria um DataFrame para informações e adiciona em uma nova planilha
        df_info = pd.DataFrame({'Informações': [f"Mês: {mes}", f"Ano: {ano}"]})
        
        # Adiciona as informações na nova planilha
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_info.to_excel(writer, sheet_name='Informações', index=False, header=False)
        
        messagebox.showinfo("Salvar Arquivo", f"Os dados foram salvos no arquivo: {nome_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar o arquivo: {e}")

# Função para gerar gráfico
def gerar_grafico(dados_vagas, mes, ano, tipo_analise):
    dias = list(dados_vagas.keys())
    ocupacao_manha = [dados_vagas[dia]['manha'] for dia in dias]
    ocupacao_tarde = [dados_vagas[dia]['tarde'] for dia in dias]
    ocupacao_noite = [dados_vagas[dia]['noite'] for dia in dias]
    
    plt.figure(figsize=(10, 6))
    
    if tipo_analise == '1':  # Análise por período
        plt.plot(dias, ocupacao_manha, label='Manhã', color='blue', marker='o')
        plt.plot(dias, ocupacao_tarde, label='Tarde', color='green', marker='o')
        plt.plot(dias, ocupacao_noite, label='Noite', color='red', marker='o')
        plt.title(f'Ocupação de Vagas por Período em {mes}/{ano}')
    elif tipo_analise == '2':  # Análise de Picos de Ocupação
        plt.plot(dias, [max(ocupacao_manha[i], ocupacao_tarde[i], ocupacao_noite[i]) for i in range(len(dias))],
                 label='Picos de Ocupação', color='purple', marker='o')
        plt.title(f'Picos de Ocupação em {mes}/{ano}')
    elif tipo_analise == '3':  # Análise de Capacidade
        plt.fill_between(dias, ocupacao_manha, color='blue', alpha=0.3, label='Manhã')
        plt.fill_between(dias, ocupacao_tarde, color='green', alpha=0.3, label='Tarde')
        plt.fill_between(dias, ocupacao_noite, color='red', alpha=0.3, label='Noite')
        plt.title(f'Análise de Capacidade em {mes}/{ano}')
    
    plt.xlabel('Dias do Mês')
    plt.ylabel('Vagas Ocupadas')
    plt.legend()
    plt.grid(True)
    plt.xticks(dias)
    plt.show()

# Simular o estacionamento em tempo real com 50 vagas
def simular_estacionamento_tempo_real():
    vagas_totais = 50
    vagas_ocupadas = random.randint(0, vagas_totais)
    simulacao_ativa = True  # Variável para controlar a execução da simulação

    # Criar janela para a simulação em tempo real
    janela_simulacao = tk.Toplevel()
    janela_simulacao.title("Simulação do Estacionamento em Tempo Real")

    label_vagas = tk.Label(janela_simulacao, text=f"Vagas Ocupadas: {vagas_ocupadas} | Vagas Disponíveis: {vagas_totais - vagas_ocupadas}")
    label_vagas.pack(pady=20)

    # Função de atualização da simulação
    def atualizar_simulacao():
        nonlocal vagas_ocupadas
        if simulacao_ativa:
            alterar_ocupacao = random.choice([-1, 1])  # Escolhe aleatoriamente aumentar ou diminuir
            vagas_ocupadas = max(0, min(vagas_totais, vagas_ocupadas + alterar_ocupacao))
            label_vagas.config(text=f"Vagas Ocupadas: {vagas_ocupadas} | Vagas Disponíveis: {vagas_totais - vagas_ocupadas}")
            janela_simulacao.after(1000, atualizar_simulacao)  # Atualiza a cada 1 segundo (mais responsivo)

    atualizar_simulacao()

# Função para gerar relatório do mês completo
def gerar_relatorio_mes():
    mes = int(simpledialog.askstring("Gerar Relatório", "Qual mês deseja gerar o relatório? (Digite um número de 1 a 12)"))
    ano = int(simpledialog.askstring("Gerar Relatório", "Digite o ano do relatório: (Ex.: 2023)"))

    dados_vagas = gerar_dados_aleatorios_automaticamente(mes, ano)
    salvar_em_excel(dados_vagas, mes, ano)

# Função principal
def main():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    mensagem_inicial()  # Exibe mensagem inicial

    while True:
        opcao_menu = menu_principal()
        if opcao_menu == '1':  # Análise de mês específico
            mes, ano, dados_vagas = analisar_mes_especifico()
            while True:
                tipo_analise = submenu_analise()
                if tipo_analise in ['1', '2', '3']:
                    gerar_grafico(dados_vagas, mes, ano, tipo_analise)
                elif tipo_analise == '4':
                    break
                elif tipo_analise == '5':
                    root.quit()
                    return

        elif opcao_menu == '2':  # Simulação em tempo real do estacionamento
            simular_estacionamento_tempo_real()

        elif opcao_menu == '3':  # Gerar relatório do mês
            gerar_relatorio_mes()

        elif opcao_menu == '4':  # Verificar saída
            root.quit()  # Fecha a aplicação Tkinter
            break
        else:
            messagebox.showwarning("Opção Inválida", "Por favor, escolha uma opção válida.")

    root.destroy()

if __name__ == "__main__":
    main()
