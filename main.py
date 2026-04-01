#Gabriel Vieira de Sousa 10410264
#Ian Merlini Kaltbeitzer - 10402831


import os

class Grafo:
    def __init__(self, tipo):
        self.tipo = tipo
        self.vertices = {}  # Estrutura: {id: [apelido, peso_vertice]} 
        self.adj = {}       # Lista de Adjacência: {u: {v: peso_aresta}} 

    def add_vertice(self, id_v, apelido, peso=0):
        self.vertices[id_v] = [apelido, peso]
        if id_v not in self.adj:
            self.adj[id_v] = {}

    def add_aresta(self, u, v, peso=1):
        if u in self.vertices and v in self.vertices:
            self.adj[u][v] = peso
            # Se o tipo for < 4, o grafo é não orientado 
            if self.tipo < 4:
                self.adj[v][u] = peso

    def remover_vertice(self, id_v):
        if id_v in self.vertices:
            del self.vertices[id_v]
            self.adj.pop(id_v, None)
            for u in self.adj:
                self.adj[u].pop(id_v, None) # Remove arestas incidentes 
            return True
        return False

    def remover_aresta(self, u, v):
        if u in self.adj and v in self.adj[u]:
            del self.adj[u][v]
            if self.tipo < 4:
                del self.adj[v][u]
            return True
        return False

    def mostrar_grafo(self):
        print("\n--- REPRESENTAÇÃO (LISTA DE ADJACÊNCIA) ---")
        for u in sorted(self.vertices.keys()):
            vizinhos = ", ".join([f"Destino:{v}(Peso:{p})" for v, p in self.adj[u].items()])
            print(f"Vértice {u} [{self.vertices[u][0]}]: {vizinhos}")

    def verificar_conexidade(self):
        if not self.vertices: return
        
        # Algoritmo de busca para verificar conectividade 
        visitados = set()
        inicio = list(self.vertices.keys())[0]
        
        pilha = [inicio]
        while pilha:
            v = pilha.pop()
            if v not in visitados:
                visitados.add(v)
                for vizinho in self.adj[v]:
                    pilha.append(vizinho)
        
        is_conexo = len(visitados) == len(self.vertices)
        status = "CONEXO" if is_conexo else "DESCONEXO"
        print(f"\nStatus de Conexidade: {status}")
        print(f"Vértices alcançáveis a partir do nó {inicio}: {len(visitados)}/{len(self.vertices)}")
        return is_conexo

def carregar_arquivo(nome_arq):
    if not os.path.exists(nome_arq):
        print(f"Erro: Arquivo '{nome_arq}' não encontrado!")
        return None
    
    try:
        with open(nome_arq, 'r', encoding='utf-8') as f:
            linhas = f.read().splitlines()
            tipo = int(linhas[0])
            n = int(linhas[1])
            
            g = Grafo(tipo)
            idx = 2
            # Lendo N vértices 
            for _ in range(n):
                partes = linhas[idx].split('"')
                id_v = int(partes[0].strip())
                apelido = partes[1]
                peso_v = int(partes[2].strip())
                g.add_vertice(id_v, apelido, peso_v)
                idx += 1
            
            # Lendo M arestas 
            m = int(linhas[idx])
            idx += 1
            arestas_contadas = 0
            for _ in range(m):
                if idx < len(linhas):
                    u, v, p = map(int, linhas[idx].split())
                    g.add_aresta(u, v, p)
                    arestas_contadas += 1
                    idx += 1
            
            print("\n" + "="*30)
            print("DADOS CARREGADOS COM SUCESSO")
            print(f"Vértices: {len(g.vertices)} (mínimo exigido: 70)")
            print(f"Arestas processadas: {arestas_contadas} (mínimo exigido: 180)")
            print("="*30)
            return g
    except Exception as e:
        print(f"Erro na leitura: {e}")
        return None

def salvar_arquivo(g, nome_arq):
    try:
        with open(nome_arq, 'w', encoding='utf-8') as f:
            f.write(f"{g.tipo}\n")
            f.write(f"{len(g.vertices)}\n")
            for v_id, info in g.vertices.items():
                f.write(f'{v_id} "{info[0]}" {info[1]}\n')
            
            # Coleta arestas únicas para salvar 
            lista_arestas = []
            for u in g.adj:
                for v, peso in g.adj[u].items():
                    if g.tipo >= 4 or u < v:
                        lista_arestas.append(f"{u} {v} {peso}")
            
            f.write(f"{len(lista_arestas)}\n")
            for linha in lista_arestas:
                f.write(f"{linha}\n")
        print("Arquivo salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def exibir_menu():
    print("\n" + "#"*45)
    print(" E-Mobility -  REDE DE TRANSPORTE URBANO  ") # Título coerente 
    print("#"*45)
    print("a) Ler dados do arquivo grafo.txt")
    print("b) Gravar dados no arquivo grafo.txt")
    print("c) Inserir vértice")
    print("d) Inserir aresta")
    print("e) Remover vértice")
    print("f) Remover aresta")
    print("g) Mostrar conteúdo do arquivo")
    print("h) Mostrar grafo (Lista de Adjacência)")
    print("i) Apresentar conexidade")
    print("j) Encerrar a aplicação")
    return input("\nEscolha uma opção: ").lower()

def main():
    grafo_atual = None
    
    while True:
        opcao = exibir_menu()
        
        if opcao == 'a':
            grafo_atual = carregar_arquivo("grafo.txt")
        elif opcao == 'j':
            print("Encerrando aplicação...") 
            break
        elif grafo_atual is None:
            print("Aviso: Você precisa carregar o arquivo (opção 'a') primeiro!")
        else:
            if opcao == 'b':
                salvar_arquivo(grafo_atual, "grafo.txt")
            elif opcao == 'c':
                id_v = int(input("ID do novo vértice: "))
                nome = input("Nome/Localidade: ")
                grafo_atual.add_vertice(id_v, nome)
            elif opcao == 'd':
                try:
                    entrada = input("Digite 'Origem Destino Peso' (ex: 0 1 10): ").split()
                    if len(entrada) == 3:
                        u, v, p = map(int, entrada)
                        grafo_atual.add_aresta(u, v, p)
                        print(f"Aresta {u}->{v} inserida com sucesso!")
                    else:
                        print("Erro: Você deve digitar 3 números separados por espaço.")
                except ValueError:
                    print("Erro: Digite apenas números inteiros.")
            elif opcao == 'e':
                id_v = int(input("ID do vértice a remover: "))
                if grafo_atual.remover_vertice(id_v): print("Vértice removido.")
            elif opcao == 'f':
                try:
                    entrada = input("Digite 'Origem Destino' da aresta: ").split()
                    if len(entrada) == 2:
                        u, v = map(int, entrada)
                        if grafo_atual.remover_aresta(u, v):
                            print(f"Aresta {u}-{v} removida com sucesso!")
                        else:
                            print("Erro: Aresta não encontrada.")
                    else:
                        print("Erro: Digite 2 números (Origem e Destino) separados por espaço.")
                except ValueError:
                    print("Erro: Digite apenas números inteiros.")
            elif opcao == 'g':
                if os.path.exists("grafo.txt"):
                    with open("grafo.txt", 'r') as f: print(f.read())
            elif opcao == 'h':
                grafo_atual.mostrar_grafo()
            elif opcao == 'i':
                grafo_atual.verificar_conexidade()

if __name__ == "__main__":
    main()
