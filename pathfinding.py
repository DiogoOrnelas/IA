# Menções diretas ao tabuleiro serão evitadas; pretende-se que seja geral o suficiente para qualquer tabuleiro

# Esta classe representa um nodo
class Node:
    # Inicialização de dito nodo
    def __init__(self, position, parent):
        self.position = position    # Contém a coordenada que representa
        self.parent = parent        # Contém a coordenada do nodo que o gerou
        self.g = 0                  # Heurística (estimada)
        self.h = 0                  # Heurística (idém)
        self.f = 0                  # Custo total

    # Estes métodos são usados pelo Python para executar operações da linguagem
    # Igualdade (==)
    def __eq__(self, other):
        return self.position == other.position
    # Comparação (<,>)
    def __lt__(self, other):
         return self.f < other.f
    # Converte para string
    def __repr__(self):
        return str(self.position)

# Variáveis que limitam o movimento
limit = [5,5]          # Casa do canto diagonalmente oposto a [0,0] ( assume-se que o tabuleiro tenha esta casa num canto )
illegal_moves = []     # Movimentos não permitidos
illegal_tiles = []     # Casas inacessíveis

# Função que, por ordem, recebe a casa oposta a [0,0], os movimentos não permitidos e as casas inacessíveis
def setRestrictions(_l,_im,_it):
    global limit, illegal_moves, illegal_tiles  # Necessário para alterar variáveis globais
    limit = _l
    illegal_moves = _im
    illegal_tiles = _it

# Função heurística, distância de Manhattan
def getManhattan(tile_a,tile_b):
    return abs(tile_a[0] - tile_b[0]) + abs(tile_a[1] - tile_b[1]) # Soma dos valores absolutos das diferenças dos xx e dos yy

# Esta função pega na casa atual e num dos seus possíveis vizinhos e verifica se o movimente entre ambas é impossível
def isIllegal(start,target):
    if (target in illegal_tiles):                                                           # Esta casa não é permitida?
        return True
    elif ([start,target] in illegal_moves) or ([target,start] in illegal_moves):            # O movimento entre as casas é impossível?
        return True
    elif (target[0] < 0 or target[1] < 0 or target[0] > limit[0] or target[1] > limit[1]):  # Esta casa não devia existir?
        return True
    else:                                                                                   # Se nenhuma das condições se verifica, então...    
        return False

# Devolve uma lista com todos os vizinhos acessíveis de uma casa
def getNeighbors(tile):
    (x,y) = tile
    neighbors = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]   # Para cada casa, define uma lista com os vizinhos
    illegals = []
    for neighbor in neighbors:
        if ( isIllegal(tile,neighbor) ):           # Percorrendo essa lista, remove os inacessíveis
            illegals.append(neighbor)
    for illegal in illegals:
        if illegal in neighbors:
            neighbors.remove(illegal)
    return neighbors

# Algoritmo A*
def getPath(start, end):
    
    frontier = []   # Lista de nodos em aberto (fronteira)
    visited = [] # Lista de nodos fechados
    
    start_node = Node(start, None)  # Inicializar o nodo inicial
    goal_node = Node(end, None)     # Inicializar o nodo final
    
    frontier.append(start_node)         # Começar pelo nodo inicial
    
    # Enquanto houver nodos a explorar
    while len(frontier) > 0: 
        frontier.sort() # Ordenar os nodos por custo    
        current_node = frontier.pop(0) # Escolher o nodo com custo menor
        visited.append(current_node) # Fechar o nodo atual

        # Verifica se foi alcançado o objetivo
        if current_node == goal_node:
            
            path = [] # Cria a lista que conterá o caminho

            # Como o nodo atual é o final, retroceder nodo a nodo ( através do atributo parent ),
            # adicionando-os ao path
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            # path.append(start) # Adicionar nodo inicial ao path
            return path[::-1] # Devolve caminho

        # Se o nodo atual não é o objetivo, então:
        neighbors = getNeighbors(current_node.position) # Determina as coordenadas para as quais o movimento é possível

        for next in neighbors:                  # Para cada um das casas vizinhas
            neighbor = Node(next, current_node) # Cria um nodo (coordenada, nodo que o gera)
            if(neighbor in visited):            # Verifica se já foi visitado
                continue
            # Gera as estimativas de forma a calcular custo
            neighbor.g = getManhattan(neighbor.position,start_node.position)
            neighbor.h = getManhattan(neighbor.position,goal_node.position)
            neighbor.f = neighbor.g + neighbor.h
            # Verfifica se o vizinho deve ser adicionado à lista de possíveis caminhos a tomar
            if(canAddToFrontier(frontier, neighbor)):
                frontier.append(neighbor)
    return [] # Caso sejam percorridos todos os nodos possíveis e não tenha sido encontrado o caminho, devolve None
    

# Função auxiliar para avaliar se o nodo é válido para ser visitado
def canAddToFrontier(frontier, neighbor):
    for node in frontier:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True
