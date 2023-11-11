import tkinter as tk
import cx_Oracle
from tkinter import Menu
from tkinter import PhotoImage
from tkinter import Entry
from tkinter import Button
from tkinter import Label

class Interface:
    def __init__(self, root):
        self.connection = cx_Oracle.connect('rm89162/280400@oracle.fiap.com.br:1521/orcl')
        self.cursor = self.connection.cursor()

        root.title("Gerenciador de Dados")
        root.geometry("800x800")

        self.registros_text = tk.Text(root, width=80, height=20)
        self.registros_text.pack()

        listar_button = tk.Button(root, text="Listar Registros", command=self.listar_registros)
        listar_button.pack()

        espaco_vertical = tk.Label(root, text="", height=2)
        espaco_vertical.pack()

        adicionar_label = Label(root, text="Adicionar Registro:")
        adicionar_label.pack()

        node_id_label = Label(root, text="Node_ID:")
        node_id_label.pack()
        self.node_id_entry = Entry(root)
        self.node_id_entry.pack()

        centroide_label = Label(root, text="Centroide:")
        centroide_label.pack()
        self.centroide_entry = Entry(root)
        self.centroide_entry.pack()

        uf_label = Label(root, text="UF:")
        uf_label.pack()
        self.uf_entry = Entry(root)
        self.uf_entry.pack()

        adicionar_button = Button(root, text="Adicionar", command=self.adicionar_registro)
        adicionar_button.pack()

        atualizar_label = Label(root, text="Atualizar Registro:")
        atualizar_label.pack()

        indice_label = Label(root, text="Índice:")
        indice_label.pack()
        self.indice_entry = Entry(root)
        self.indice_entry.pack()

        node_id_label = Label(root, text="Node_ID:")
        node_id_label.pack()
        self.node_id_entry_atualizar = Entry(root)
        self.node_id_entry_atualizar.pack()

        centroide_label = Label(root, text="Centroide:")
        centroide_label.pack()
        self.centroide_entry_atualizar = Entry(root)
        self.centroide_entry_atualizar.pack()

        uf_label = Label(root, text="UF:")
        uf_label.pack()
        self.uf_entry_atualizar = Entry(root)
        self.uf_entry_atualizar.pack()

        atualizar_button = Button(root, text="Atualizar", command=self.atualizar_registro)
        atualizar_button.pack()

        menu = Menu(root)
        root.config(menu=menu)

        imagem_menu = PhotoImage(file="./images/ResqLogo.png")

        submenu_arquivo = Menu(menu)
        menu.add_cascade(label="Arquivo", menu=submenu_arquivo)
        submenu_arquivo.add_command(label="Abrir Imagem", image=imagem_menu, compound=tk.LEFT)

    def listar_registros(self):
        self.registros_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT * FROM Matrizes")
        dados = self.cursor.fetchall()

        for i, registro in enumerate(dados):
            self.registros_text.insert(tk.END, f"Índice: {i}, Node_ID: {registro[0]}, Centroide: {registro[1]}, UF: {registro[2]}\n")

    def adicionar_registro(self):
        node_id = self.node_id_entry.get()
        centroide = self.centroide_entry.get()
        uf = self.uf_entry.get()

        try:
            self.cursor.execute("INSERT INTO Matrizes (Node_ID, Centroide, UF) VALUES (:node_id, :centroide, :uf)",
                               node_id=node_id, centroide=centroide, uf=uf)
            self.connection.commit()
            self.listar_registros()
        except Exception as e:
            print("Erro ao adicionar registro:", e)

    def atualizar_registro(self):
        indice = int(self.indice_entry.get())
        node_id = self.node_id_entry_atualizar.get()
        centroide = self.centroide_entry_atualizar.get()
        uf = self.uf_entry_atualizar.get()

        try:
            self.cursor.execute("UPDATE Matrizes SET Node_ID = :node_id, Centroide = :centroide, UF = :uf WHERE Node_ID = :node_id",
                               node_id=node_id, centroide=centroide, uf=uf)
            self.connection.commit()
            self.listar_registros()
        except Exception as e:
            print("Erro ao atualizar registro:", e)

def main():
    root = tk.Tk()
    interface = Interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
