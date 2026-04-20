import re
import matplotlib.pyplot as plt
import networkx as nx

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

def obtener_prioridad(operador):
    prioridades = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    return prioridades.get(operador, 0)

def infija_a_postfija(expresion):
    salida = []
    pila = []
    
    tokens = re.findall(r'\d+|[+\-*/()^]', expresion)
    
    for token in tokens:
        if token.isdigit():
            salida.append(token)
        elif token == '(':
            pila.append(token)
        elif token == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            if pila: 
                pila.pop()
        else:
            while pila and obtener_prioridad(pila[-1]) >= obtener_prioridad(token):
                salida.append(pila.pop())
            pila.append(token)
            
    while pila:
        salida.append(pila.pop())
    return salida

def construir_arbol(lista_postfija):
    if not lista_postfija: 
        return None
    
    pila_nodos = []
    
    for token in lista_postfija:
        if token.isdigit():
            pila_nodos.append(Nodo(token))
        else:
            nuevo_nodo = Nodo(token)
            if len(pila_nodos) >= 2:
                nuevo_nodo.derecho = pila_nodos.pop()
                nuevo_nodo.izquierdo = pila_nodos.pop()
            pila_nodos.append(nuevo_nodo)
            
    return pila_nodos[0] if pila_nodos else None

def dibujar_arbol(raiz, operacion_usuario):
    grafo = nx.DiGraph()
    posiciones = {}
    etiquetas = {}

    def agregar_aristas(nodo, x=0, y=0, nivel=1):
        if nodo is not None:
            id_nodo = id(nodo)
            grafo.add_node(id_nodo)
            etiquetas[id_nodo] = nodo.valor
            posiciones[id_nodo] = (x, y)
            
            if nodo.izquierdo:
                grafo.add_edge(id_nodo, id(nodo.izquierdo))
                agregar_aristas(nodo.izquierdo, x - 1 / nivel, y - 1, nivel * 2)
            
            if nodo.derecho:
                grafo.add_edge(id_nodo, id(nodo.derecho))
                agregar_aristas(nodo.derecho, x + 1 / nivel, y - 1, nivel * 2)

    plt.clf() 
    agregar_aristas(raiz)
    
    nx.draw(grafo, posiciones, labels=etiquetas, with_labels=True, 
            node_size=2000, node_color="lightgreen", 
            font_size=12, font_weight="bold", arrows=False)
    
    plt.title(f"Árbol de la expresión: {operacion_usuario}")
    plt.show()

print("--- GENERADOR DE ÁRBOLES DE EXPRESIONES ---")
print("Escribe 'salir' para cerrar.")

while True:
    print("\n" + "="*40)
    entrada_usuario = input("Ingresa la operación matemática: ")
    
    if entrada_usuario.lower() == 'salir':
        print("Saliendo...")
        break
    
    if not entrada_usuario.strip():
        print("Error: No escribiste nada.")
        continue

    try:
        resultado_postfijo = infija_a_postfija(entrada_usuario)
        arbol_final = construir_arbol(resultado_postfijo)
        
        if arbol_final:
            print("Dibujando... (cierra la ventana para continuar)")
            dibujar_arbol(arbol_final, entrada_usuario)
        else:
            print("Error: No se pudo crear el árbol.")
            
    except Exception as error:
        print(f"Hubo un error: {error}")
        