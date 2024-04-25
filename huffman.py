from collections import Counter
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as filedialog
import heapq

def ventanaPrincipal():
    global ventana
    ventana = tk.Tk()
    frm = ttk.Frame(ventana, padding=10)
    frm.grid()
    ventana.title("Actividad 07 - Mariana Ruiz Gonzalez")
    ventana.geometry("600x600")

    boton_examinar = ttk.Button(ventana, text="Examinar", command=examinar)
    boton_examinar.grid(column=1, row=0)
    boton_comprimir = ttk.Button(ventana, text="Comprimir", command=lambda: comprimir_archivo('Gullivers_Travels.txt', 'ArchivoComprimido.bin')).grid(column=1, row=1)
    boton_descomprimir = ttk.Button(ventana, text="Descomprimir", command=lambda: descomprimir_archivo('ArchivoComprimido.bin', 'ArchivoDescomprimido')).grid(column=1, row=2)

    ventana.mainloop()

def examinar():
    # Abrir el cuadro de diálogo de selección de archivos
    nombre_archivo = filedialog.askopenfilename(initialdir="/", title="Selecciona un archivo de texto",
                                                filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
    
    # Verificar si se seleccionó un archivo
    if nombre_archivo:
        # Leer el archivo seleccionado
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            mensaje = archivo.read()

        # Llamar a las funciones que deseas ejecutar con el archivo seleccionado
        contador = contador_de_Caracteres(mensaje)
        caracteres_ordenados = ordenar_Caracteres(mensaje)

        # Construir árbol de Huffman y asignar códigos
        arbol_huffman = construir_arbol_huffman(mensaje)
        codigos_huffman = asignar_codigos_huffman(arbol_huffman)

        # Llamar a resultado_Archivo con los argumentos requeridos
        resultado_Archivo(mensaje, contador, caracteres_ordenados, codigos_huffman)

# Contador de caracteres dentro del documento abierto
def contador_de_Caracteres(mensaje):
    contador = 0
    for linea in mensaje:
        for caracter in linea:
            contador += 1
    return contador

# Análisis para contar cuántas veces se repiten los caracteres en el doc
def ordenar_Caracteres(mensaje):
    repeticion = Counter(mensaje)
    caracteres_ordenados = sorted(repeticion.items(), key=lambda x: x[1], reverse=True)
    return caracteres_ordenados

# Crea un archivo de texto nuevo donde se imprimen los datos que se extrajeron anteriormente
# 'w' crea el archivo nuevo y si ya existe, se limpia y sobrescribe en modo abierto
def resultado_Archivo(mensaje, contador, caracteres_ordenados, codigos_huffman):
    with open('resultado.txt', 'w', encoding='utf-8') as archivoResultado:
        archivoResultado.write(f"Número total de caracteres en el texto: {contador}\n\n")
        archivoResultado.write("Caracteres y sus frecuencias:\n")
        for caracter, frecuencia in caracteres_ordenados:
            archivoResultado.write(f"Caracter: {caracter}, Frecuencia: {frecuencia}\n")
        archivoResultado.write("\nÁrbol de Huffman (codificación):\n")
        for caracter, codigo in codigos_huffman.items():
            archivoResultado.write(f"Caracter: {caracter}, Código Huffman: {codigo}\n")

def construir_arbol_huffman(mensaje):
    repeticion = Counter(mensaje)
    heap = [[frecuencia, [caracter, ""]] for caracter, frecuencia in repeticion.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        bajo = heapq.heappop(heap)
        alto = heapq.heappop(heap)
        for par in bajo[1:]:
            par[1] = '0' + par[1]
        for par in alto[1:]:
            par[1] = '1' + par[1]
        heapq.heappush(heap, [bajo[0] + alto[0]] + bajo[1:] + alto[1:])
    return heap[0][1:]

def asignar_codigos_huffman(arbol_huffman):
    codigos = {}
    for caracter, codigo in arbol_huffman:
        codigos[caracter] = codigo
    return codigos

def comprimir_archivo(archivo_entrada, archivo_salida):
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
        mensaje = archivo.read()

    # Calcular las frecuencias de los caracteres en el mensaje
    frecuencias = Counter(mensaje)

    # Construir el árbol de Huffman
    heap = [[frecuencia, [caracter, ""]] for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        bajo = heapq.heappop(heap)
        alto = heapq.heappop(heap)
        for par in bajo[1:]:
            par[1] = '0' + par[1]
        for par in alto[1:]:
            par[1] = '1' + par[1]
        heapq.heappush(heap, [bajo[0] + alto[0]] + bajo[1:] + alto[1:])
    
    # Obtener la codificación de Huffman para cada carácter
    codigos = {}
    for caracter, codigo in heap[0][1:]:
        codigos[caracter] = codigo

    # Reemplazar los caracteres del mensaje con sus códigos Huffman
    mensaje_codificado = ''.join(codigos[caracter] for caracter in mensaje)

    # Escribir las frecuencias de los caracteres y el mensaje codificado en el archivo de salida
    with open(archivo_salida, 'wb') as archivo:
        # Escribir las frecuencias de los caracteres para la descompresión
        for caracter, frecuencia in frecuencias.items():
            archivo.write(f"{caracter}:{frecuencia}\n".encode())
        archivo.write(b"\n")
        # Escribir el mensaje codificado
        archivo.write(mensaje_codificado.encode())

    print(f"Archivo comprimido creado: {archivo_salida}")

def descomprimir_archivo(ArchivoComprimido, ArchivoDescomprimido):
    # Leer el archivo comprimido
    with open(ArchivoComprimido, 'rb') as archivo:
        contenido = archivo.read().decode()

    # Extraer las frecuencias de los caracteres del encabezado
    frecuencias = {}
    caracteres, cuerpo = contenido.split('\n\n', 1)

    for linea in caracteres.split('\n'):
        if linea:
            caracter, frecuencia = linea.split(':')
            frecuencias[caracter] = int(frecuencia)

    # Reconstruir el árbol de Huffman
    heap = [[frecuencia, [caracter, ""]] for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        bajo = heapq.heappop(heap)
        alto = heapq.heappop(heap)
        for par in bajo[1:]:
            par[1] = '0' + par[1]
        for par in alto[1:]:
            par[1] = '1' + par[1]
        heapq.heappush(heap, [bajo[0] + alto[0]] + bajo[1:] + alto[1:])

    # Decodificar el cuerpo usando el árbol de Huffman
    # Decodificar el cuerpo usando el árbol de Huffman
    arbol_huffman = heap[0][1:]
    mensaje_descomprimido = ''
    nodo_raiz = arbol_huffman  # Mantener una referencia al nodo raíz
    nodo_actual = nodo_raiz
    for bit in cuerpo:
        if bit == '0':
            nodo_actual = nodo_actual[0]
        else:
            nodo_actual = nodo_actual[1]
        if isinstance(nodo_actual[0], str):
            mensaje_descomprimido += nodo_actual[0]
            nodo_actual = nodo_raiz  # Restablecer a la raíz para buscar el próximo caracter

    # Escribir el mensaje descomprimido en el archivo de salida
    with open(ArchivoDescomprimido, 'w', encoding='utf-8') as archivo:
        archivo.write(mensaje_descomprimido)

    print(f"Archivo descomprimido creado: {ArchivoDescomprimido}")



if __name__ == "__main__":
    ventanaPrincipal()
