from datetime import datetime
import tkinter as tk
import cx_Oracle
import json
from tkinter import messagebox

class Interface:
    def __init__(self, root):
        self.connection = cx_Oracle.connect('rm550711/221004@oracle.fiap.com.br:1521/orcl')
        self.cursor = self.connection.cursor()

        root.title("Gerenciador de Medicamentos")
        root.geometry("800x1440")

        self.registros_text = tk.Text(root, width=80, height=20)
        self.registros_text.pack()

        listar_button = tk.Button(root, text="Listar Medicamentos", command=self.listar_medicamentos)
        listar_button.pack()

        espaco_vertical = tk.Label(root, text="", height=2)
        espaco_vertical.pack()

        adicionar_label = tk.Label(root, text="Adicionar Medicamento:")
        adicionar_label.pack()

        nm_medicamento_label = tk.Label(root, text="Nome do Medicamento:")
        nm_medicamento_label.pack()
        self.nm_medicamento_entry = tk.Entry(root)
        self.nm_medicamento_entry.pack()

        ds_medicamento_label = tk.Label(root, text="Descrição Detalhada:")
        ds_medicamento_label.pack()
        self.ds_medicamento_entry = tk.Entry(root)
        self.ds_medicamento_entry.pack()

        codigo_barras_label = tk.Label(root, text="Código de Barras:")
        codigo_barras_label.pack()
        self.codigo_barras_entry = tk.Entry(root)
        self.codigo_barras_entry.pack()

        nm_usuario_label = tk.Label(root, text="Nome do Usuário:")
        nm_usuario_label.pack()
        self.nm_usuario_entry = tk.Entry(root)
        self.nm_usuario_entry.pack()

        adicionar_button = tk.Button(root, text="Adicionar", command=self.adicionar_medicamento)
        adicionar_button.pack()

        atualizar_label = tk.Label(root, text="Atualizar Medicamento:")
        atualizar_label.pack()

        id_label = tk.Label(root, text="ID do Medicamento:")
        id_label.pack()
        self.id_entry = tk.Entry(root)
        self.id_entry.pack()

        atualizar_nm_medicamento_label = tk.Label(root, text="Novo Nome do Medicamento:")
        atualizar_nm_medicamento_label.pack()
        self.atualizar_nm_medicamento_entry = tk.Entry(root)
        self.atualizar_nm_medicamento_entry.pack()

        atualizar_button = tk.Button(root, text="Atualizar", command=self.atualizar_medicamento)
        atualizar_button.pack(pady=10)

        excluir_label = tk.Label(root, text="Excluir Medicamento:")
        excluir_label.pack()

        id_excluir_label = tk.Label(root, text="ID do Medicamento a Excluir:")
        id_excluir_label.pack()
        self.id_excluir_entry = tk.Entry(root)
        self.id_excluir_entry.pack()

        excluir_button = tk.Button(root, text="Excluir", command=self.excluir_medicamento)
        excluir_button.pack(pady=5)

        consulta1_button = tk.Button(root, text="Exportar tudo", command=lambda: self.consulta_e_exporta(1))
        consulta1_button.pack(pady=10)

        consulta2_button = tk.Button(root, text="Exportar nomes", command=lambda: self.consulta_e_exporta(2))
        consulta2_button.pack(pady=10)

        consulta3_button = tk.Button(root, text="Exportar descrições", command=lambda: self.consulta_e_exporta(3))
        consulta3_button.pack(pady=10)

        menu = tk.Menu(root)
        root.config(menu=menu)

        submenu_arquivo = tk.Menu(menu)
        menu.add_cascade(label="Arquivo", menu=submenu_arquivo)
        submenu_arquivo.add_command(label="Abrir Imagem")

    def listar_medicamentos(self):
        self.registros_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT * FROM T_PLPL_MEDICAMENTO")
        dados = self.cursor.fetchall()

        for registro in dados:
            texto = f"ID: {registro[0]}, Nome: {registro[1]}, Descrição: {registro[2]}, "
            texto += f"Código de Barras: {registro[3]}, Data Cadastro: {registro[4]}, Usuário: {registro[5]}\n"
            self.registros_text.insert(tk.END, texto)

    def validar_entrada(self, entrada):
        return entrada.strip() != ""

    def adicionar_medicamento(self):
        nm_medicamento = self.nm_medicamento_entry.get()
        ds_medicamento = self.ds_medicamento_entry.get()
        codigo_barras = self.codigo_barras_entry.get()
        nm_usuario = self.nm_usuario_entry.get()

        if not self.validar_entrada(nm_medicamento) or not self.validar_entrada(ds_medicamento) \
           or not self.validar_entrada(codigo_barras) or not self.validar_entrada(nm_usuario):
            messagebox.showerror("Erro", "Dados de entrada inválidos")
            return

        try:
            self.cursor.execute("INSERT INTO T_PLPL_MEDICAMENTO (NM_MEDICAMENTO, DS_DETALHADA_MEDICAMENTO, NR_CODIGO_BARRAS, NM_USUARIO) "
                                "VALUES (:nm_medicamento, :ds_medicamento, :codigo_barras, :nm_usuario)",
                                nm_medicamento=nm_medicamento, ds_medicamento=ds_medicamento, 
                                codigo_barras=codigo_barras, nm_usuario=nm_usuario)
            self.connection.commit()
            self.listar_medicamentos()
        except Exception as e:
            messagebox.showerror("Erro ao adicionar medicamento", str(e))


    def excluir_medicamento(self):
        id_medicamento = self.id_excluir_entry.get()

        if not self.validar_entrada(id_medicamento):
            messagebox.showerror("Erro", "Por favor, insira um ID válido")
            return

        try:
            self.cursor.execute("DELETE FROM T_PLPL_MEDICAMENTO WHERE ID_MEDICAMENTO = :ID_MEDICAMENTO",
                                id_medicamento=id_medicamento)
            self.connection.commit()
            messagebox.showinfo("Sucesso", "Medicamento excluído com sucesso")
            self.listar_medicamentos()
        except Exception as e:
            messagebox.showerror("Erro ao excluir medicamento", str(e))

    def atualizar_medicamento(self):
        id_medicamento = self.id_entry.get()
        novo_nm_medicamento = self.atualizar_nm_medicamento_entry.get()

        if not self.validar_entrada(id_medicamento) or not self.validar_entrada(novo_nm_medicamento):
            messagebox.showerror("Erro", "Dados de entrada inválidos")
            return

        try:
            self.cursor.execute("UPDATE T_PLPL_MEDICAMENTO SET NM_MEDICAMENTO = :novo_nm_medicamento WHERE ID_MEDICAMENTO = :id_medicamento",
                                novo_nm_medicamento=novo_nm_medicamento, id_medicamento=id_medicamento)
            self.connection.commit()
            self.listar_medicamentos()
        except Exception as e:
            messagebox.showerror("Erro ao atualizar medicamento", str(e))

    def consulta_e_exporta(self, numero_consulta):
        consulta = {
            1: "SELECT * FROM T_PLPL_MEDICAMENTO",
            2: "SELECT NM_MEDICAMENTO FROM T_PLPL_MEDICAMENTO",
            3: "SELECT DS_DETALHADA_MEDICAMENTO FROM T_PLPL_MEDICAMENTO",
        }[numero_consulta]

        self.cursor.execute(consulta)
        dados = self.cursor.fetchall()
        self.exportar_para_json(dados, f'consulta{numero_consulta}.json')

    def exportar_para_json(self, dados, nome_arquivo):
        try:
            dados_formatados = []
            for row in dados:
                row_formatado = list(row)
                for i, valor in enumerate(row_formatado):
                    if isinstance(valor, datetime):
                        row_formatado[i] = valor.strftime("%Y-%m-%d %H:%M:%S")
                dados_formatados.append(dict(zip(["ID_MEDICAMENTO", "NM_MEDICAMENTO", "DS_DETALHADA_MEDICAMENTO", 
                                                  "NR_CODIGO_BARRAS", "DT_CADASTRO", "NM_USUARIO"], row_formatado)))

            with open(nome_arquivo, 'w') as arquivo:
                json.dump(dados_formatados, arquivo, indent=4)

            messagebox.showinfo("Sucesso", f"Dados exportados para {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível exportar os dados: {e}")

def main():
    root = tk.Tk()
    interface = Interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
