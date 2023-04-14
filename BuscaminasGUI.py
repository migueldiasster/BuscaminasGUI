import tkinter as tk
import random

# Tamaño del tablero de juego
NUM_FILAS = 10
NUM_COLUMNAS = 10
NUM_MINAS = 10

class JuegoDeMina:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Minas")
        self.crear_tablero()
        self.generar_minas()
        self.crear_interfaz_grafica()

    def crear_tablero(self):
        self.tablero = [[0 for _ in range(NUM_COLUMNAS)] for _ in range(NUM_FILAS)]

    def generar_minas(self):
        minas_generadas = 0
        while minas_generadas < NUM_MINAS:
            fila = random.randint(0, NUM_FILAS - 1)
            columna = random.randint(0, NUM_COLUMNAS - 1)
            if self.tablero[fila][columna] != -1:
                self.tablero[fila][columna] = -1
                minas_generadas += 1

    def crear_interfaz_grafica(self):
        self.botones = []
        for fila in range(NUM_FILAS):
            fila_botones = []
            for columna in range(NUM_COLUMNAS):
                boton = tk.Button(self.root, width=3, height=1, font=('Helvetica', 16))
                boton.grid(row=fila, column=columna)
                boton.bind('<Button-1>', lambda event, fila=fila, columna=columna: self.revelar_casilla(event, fila, columna))
                fila_botones.append(boton)
            self.botones.append(fila_botones)

    def revelar_casilla(self, event, fila, columna):
        if self.tablero[fila][columna] == -1:
            self.botones[fila][columna].config(text='*', state='disabled')
            self.mostrar_mensaje("Perdiste")
            self.desactivar_botones()
        else:
            minas_cercanas = self.contar_minas_cercanas(fila, columna)
            self.botones[fila][columna].config(text=minas_cercanas, state='disabled')
            if minas_cercanas == 0:
                self.revelar_casillas_cercanas(fila, columna)
            if self.verificar_victoria():
                self.mostrar_mensaje("¡Ganaste!")
                self.desactivar_botones()

    def contar_minas_cercanas(self, fila, columna):
        minas_cercanas = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                fila_vecina = fila + i
                columna_vecina = columna + j
                if 0 <= fila_vecina < NUM_FILAS and 0 <= columna_vecina < NUM_COLUMNAS and self.tablero[fila_vecina][columna_vecina] == -1:
                    minas_cercanas += 1
        return minas_cercanas

    def revelar_casillas_cercanas(self, fila, columna):
        for i in range(-1, 2):
            for j in range(-1, 2):
                fila_vecina = fila + i
                columna_vecina = columna + j
                if 0 <= fila_vecina < NUM_FILAS and 0 <= columna_vecina < NUM_COLUMNAS and self.botones[fila_vecina][columna_vecina]['state'] == 'normal':
                    self.revelar_casilla(None, fila_vecina, columna_vecina)

    def verificar_victoria(self):
        for fila in range(NUM_FILAS):
            for columna in range(NUM_COLUMNAS):
                if self.tablero[fila][columna] != -1 and self.botones[fila][columna]['state'] == 'normal':
                    return False
        return True

    def mostrar_mensaje(self, mensaje):
        popup = tk.Toplevel()
        popup.title("Mensaje")
        label = tk.Label(popup, text=mensaje, font=('Helvetica', 16), padx=20, pady=20)
        label.pack()
        ok_button = tk.Button(popup, text="OK", font=('Helvetica', 16), command=popup.destroy)
        ok_button.pack()

    def desactivar_botones(self):
        for fila in range(NUM_FILAS):
            for columna in range(NUM_COLUMNAS):
                self.botones[fila][columna]['state'] = 'disabled'

if __name__ == '__main__':
    root = tk.Tk()
    juego = JuegoDeMina(root)
    root.mainloop()
