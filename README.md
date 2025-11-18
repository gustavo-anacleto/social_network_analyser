# 🔍 Sistema de Análise de Redes Sociais

Sistema completo para análise de redes sociais com foco na detecção de padrões suspeitos de consumo de conteúdo, especialmente adultos consumindo conteúdo direcionado a menores de idade.

## ⚠️ Aviso Importante

Este sistema foi desenvolvido para auxiliar autoridades e plataformas na identificação de comportamentos suspeitos que possam indicar riscos para menores de idade. Deve ser utilizado apenas por profissionais autorizados e sempre em conformidade com as leis locais de privacidade e proteção de dados.

## 📋 Funcionalidades Principais

- **Análise de Grafos**: Detecção de comunidades, influenciadores e padrões de conexão
- **Detecção de Padrões Suspeitos**: Identificação de usuários com comportamentos anômalos
- **Análise de Conteúdo**: Avaliação de padrões de consumo de conteúdo
- **Métricas de Centralidade**: Identificação de usuários influentes na rede
- **Relatórios Detalhados**: Geração de planilhas Excel com análises completas
- **Visualizações**: Gráficos de rede para melhor compreensão dos dados

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Dependências

```bash
pip install networkx pandas numpy matplotlib seaborn openpyxl jinja2
```

### Dependências Opcionais

```bash
# Para detecção de comunidades mais avançada
pip install python-louvain

# Para análises estatísticas adicionais
pip install scipy scikit-learn
```

## 📁 Estrutura do Projeto

```
social-network-analyzer/
│
├── main.py                    # Módulo principal
├── graph_utils.py             # Utilitários de análise de grafos
├── content_analyzer.py        # Análise de padrões de conteúdo
├── report_generator.py        # Geração de relatórios
├── exemplo_uso_completo.py    # Exemplo de uso
├── README.md                  # Este arquivo
│
└── reports/                   # Diretório de saída dos relatórios
    ├── relatorio_*.xlsx       # Relatórios Excel
    ├── usuarios_suspeitos_*.csv
    └── *.png                  # Gráficos gerados
```

## 🚀 Uso Rápido

### Exemplo Básico

```python
from main import SocialNetworkAnalyzer

# Cria instância do analisador
analyzer = SocialNetworkAnalyzer()

# Adiciona usuários
analyzer.add_user("user_001", 45, {"name": "João"})
analyzer.add_user("user_002", 12, {"name": "Ana"})

# Adiciona conexões
analyzer.add_connection("user_001", "user_002", "friend")

# Adiciona consumo de conteúdo
analyzer.add_content_interaction(
    "user_001", 
    "content_001", 
    "kids_video", 
    "view", 
    {"target_age_max": 8}
)

# Gera relatório
report = analyzer.generate_risk_report()
print(f"Usuários suspeitos: {len(report['suspicious_users'])}")
```

### Execução Completa com Dados Simulados

```bash
python exemplo_uso_completo.py
```

## 📊 Módulos do Sistema

### 1. main.py - Módulo Principal
- `SocialNetworkAnalyzer`: Classe principal para análise de redes
- Detecção de usuários suspeitos
- Análise de redes de conexões
- Geração de relatórios de risco

### 2. graph_utils.py - Análise de Grafos
- `GraphAnalyzer`: Análises avançadas de grafos
- `SuspiciousPatternDetector`: Detecção de padrões específicos
- `NetworkVisualizer`: Visualizações de rede

### 3. content_analyzer.py - Análise de Conteúdo
- `ContentAnalyzer`: Análise de padrões de consumo
- `ContentSimilarityAnalyzer`: Análise de similaridade entre conteúdos
- Classificação de risco de conteúdos

### 4. report_generator.py - Relatórios
- `ReportGenerator`: Geração de relatórios Excel e CSV
- Múltiplas abas com diferentes análises
- Formatação profissional para investigação

## 📈 Métricas Analisadas

### Usuários
- **Score de Risco**: Baseado em padrões de consumo anômalos
- **Centralidade**: Grau, intermediação, proximidade, PageRank
- **Padrões Temporais**: Horários de atividade suspeitos
- **Conexões**: Redes de usuários com comportamentos similares

### Conteúdo
- **Classificação de Risco**: Baseada em idade alvo e metadados
- **Padrões de Consumo**: Adultos consumindo conteúdo infantil
- **Similaridade**: Agrupamento de conteúdos similares
- **Interações**: Tipos de interação (view, download, share)

## 📋 Relatórios Gerados

### Relatório Excel Completo
- **Resumo Executivo**: Métricas principais e alertas
- **Usuários Suspeitos**: Lista detalhada com scores de risco
- **Análise de Redes**: Componentes conectados e comunidades
- **Influenciadores**: Usuários com alta centralidade e risco
- **Conteúdo Problemático**: Conteúdos com alta interação suspeita
- **Recomendações**: Ações específicas por prioridade
- **Dados para Investigação**: Informações detalhadas para autoridades

### CSV Resumido
- Lista simplificada de usuários suspeitos
- Formato compatível com outras ferramentas
- Fácil importação em sistemas externos

## 🎯 Indicadores de Risco

### Alto Risco (Score > 0.7)
- Adultos com >60% de consumo de conteúdo infantil
- Múltiplas ações de download/compartilhamento suspeitas
- Padrões temporais anômalos (horário escolar)

### Médio Risco (Score 0.4-0.7)
- Adultos com 30-60% de consumo de conteúdo infantil
- Conexões suspeitas por diferença de idade
- Comportamento focado em poucos tipos de conteúdo

### Baixo Risco (Score 0.2-0.4)
- Padrões levemente anômalos
- Consumo ocasional de conteúdo infantil
- Requer monitoramento

## 🔧 Configuração Avançada

### Ajuste de Thresholds

```python
# Personalizar detecção de padrões suspeitos
analyzer.detect_suspicious_content_patterns(min_age_gap=15)

# Configurar detector de padrões
pattern_detector = SuspiciousPatternDetector(age_gap_threshold=20)

# Ajustar similaridade de conteúdo
similarity_analyzer = ContentSimilarityAnalyzer()
similarity_analyzer.similarity_threshold = 0.8
```

### Integração com Banco de Dados

```python
def load_data_from_database():
    # Conecta ao banco de dados
    conn = create_database_connection()
    
    # Carrega usuários
    users = conn.execute("SELECT id, age, profile_data FROM users").fetchall()
    for user in users:
        analyzer.add_user(user.id, user.age, user.profile_data)
    
    # Carrega conexões
    connections = conn.execute("SELECT user1_id, user2_id, type FROM connections").fetchall()
    for conn_data in connections:
        analyzer.add_connection(conn_data.user1_id, conn_data.user2_id, conn_data.type)
```

## 📊 Interpretação dos Resultados

### Scores de Risco
- **0.8-1.0**: Risco crítico - Investigação imediata
- **0.6-0.8**: Risco alto - Monitoramento intensivo
- **0.4-0.6**: Risco médio - Acompanhamento regular
- **0.2-0.4**: Risco baixo - Monitoramento passivo
- **0.0-0.2**: Risco mínimo - Comportamento normal

### Métricas de Rede
- **Densidade**: Quão conectados estão os usuários suspeitos
- **Componentes**: Grupos isolados de usuários conectados
- **Centralidade**: Influência de cada usuário na rede

## ⚖️ Considerações Legais e Éticas

1. **Privacidade**: Sempre anonimize dados pessoais
2. **Consentimento**: Garanta base legal para processamento
3. **Proporcionalidade**: Use apenas para fins legítimos de segurança
4. **Transparência**: Mantenha logs de todas as análises
5. **Retenção**: Defina políticas de retenção de dados

## 🛡️ Segurança

- Mantenha relatórios em local seguro
- Use criptografia para dados sensíveis
- Implemente controle de acesso rigoroso
- Monitore uso do sistema

## 🤝 Integração com Autoridades

### Formato de Exportação
Os relatórios são gerados em formato compatível com sistemas de investigação:
- Excel com múltiplas abas organizadas
- CSV para importação em outras ferramentas
- Metadados completos para rastreabilidade

### Informações Incluídas
- Identificadores de usuário (hasheados se necessário)
- Scores de risco calculados
- Evidências de comportamento suspeito
- Recomendações de ação
- Timestamps de todas as atividades

## 📞 Suporte e Desenvolvimento

Para dúvidas técnicas ou melhorias:
1. Verifique a documentação dos módulos
2. Execute os exemplos fornecidos
3. Teste com dados simulados antes de usar dados reais

## 🔄 Atualizações Futuras

Funcionalidades planejadas:
- Integração com APIs de redes sociais
- Machine Learning para detecção mais precisa
- Dashboard web para visualização em tempo real
- Alertas automáticos por email/SMS
- Análise de sentimento em mensagens

---

**⚠️ IMPORTANTE**: Este sistema é uma ferramenta de apoio à investigação. A interpretação dos resultados e tomada de decisões devem sempre envolver profissionais qualificados e seguir os procedimentos legais apropriados.


1. Detecção de comunidades (detect_communities)

Louvain (community_louvain.best_partition)

Tipo: algoritmo de detecção de comunidades baseado em maximização de modularidade.
Ideia: tenta agrupar nós em comunidades de forma que:
haja muitas arestas dentro de cada comunidade;
e relativamente poucas arestas entre comunidades diferentes.
Funciona em duas fases repetidas:
Fase local: move nós entre comunidades vizinhas se isso aumentar a modularidade.
Fase de agregação: comprime cada comunidade em um “super-nó” e repete o processo.
Resultado: um dicionário nó -> id_da_comunidade.
Greedy modularity (nx.community.greedy_modularity_communities)

Tipo: algoritmo guloso de comunidades, também baseado em modularidade.
Começa com cada nó em sua própria comunidade e, passo a passo, junta comunidades que mais aumentam a modularidade, até não ser mais possível melhorar.
Resultado original do NetworkX: lista de conjuntos de nós (cada conjunto é uma comunidade); o código converte isso para nó -> id.
Propagação de rótulos (nx.community.label_propagation_communities)

Tipo: algoritmo rótulo que se espalha (label propagation).
Ideia:
Cada nó começa com um rótulo único.
Em iterações, cada nó assume o rótulo mais frequente entre seus vizinhos.
Com o tempo, rótulos “dominantes” se espalham e formam comunidades.
Vantagem: muito rápido e escalável, não precisa de parâmetros.
Resultado: também convertido para nó -> id_da_comunidade.

2. Centralidades avançadas (calculate_advanced_centralities)

Aqui ele calcula várias medidas de importância dos nós na rede:

Degree Centrality (nx.degree_centrality)

Base: grau do nó (quantidade de conexões) normalizado.
Interpretação: quanto mais conexões diretas o usuário tem, mais “exposto” ou “popular” ele é.
Betweenness Centrality (nx.betweenness_centrality)

Conta quantos caminhos mais curtos entre pares de nós passam por um determinado nó.
Interpretação: nó com alta betweenness funciona como “ponte” entre grupos; ele controla o fluxo de informação.
Closeness Centrality (nx.closeness_centrality)

Base: inverso da soma das distâncias mínimas do nó para todos os outros nós.
Interpretação: quão “perto” o nó está do restante da rede em termos de caminhos curtos; bom para medir rapidez de alcance.
Eigenvector Centrality (nx.eigenvector_centrality)

Ideia: um nó é importante se ele se conecta a outros nós também importantes.
Usa o autovetor principal da matriz de adjacência.
Interpretação: parecido com popularidade “de prestígio” – conexões com hubs valem mais que conexões com nós periféricos.
Katz Centrality (nx.katz_centrality)

Expande a ideia de eigenvector:
considera não só vizinhos diretos, mas também caminhos mais longos, com um fator de decaimento (alpha) para caminhos maiores.
Interpretação: captura influência que se propaga pela rede (não só contatos diretos).
PageRank (nx.pagerank)

Modelo de um “surfer aleatório” que caminha pelos links do grafo, com probabilidade de “pular” para qualquer nó a cada passo (alpha controla isso).
Interpretação: importância global levando em conta estrutura de links, muito usado para rankear páginas (e aqui, usuários).
O método junta tudo em um dicionário: nó -> {degree, betweenness, closeness, eigenvector, katz, pagerank}.

3. Pontes e pontos de articulação (find_bridges_and_articulation_points)

Pontes (nx.bridges)

Arestas cuja remoção aumenta o número de componentes conectados.
Na prática: conexões críticas; se você cortar essa amizade/conexão, a rede se fragmenta.
Pontos de articulação (nx.articulation_points)

Nós cuja remoção (junto com suas arestas) também quebra o grafo em mais componentes.
Na prática: usuários “chave” que conectam grupos; se saírem, a rede se desconecta.
4. Análise estrutural do grafo (analyze_graph_structure)

Este método usa várias funções do NetworkX para estatísticas globais:

nx.density(graph): densidade (proporção de arestas existentes em relação ao máximo possível).

Conectividade:

nx.is_connected(graph): se todos os nós estão, direta ou indiretamente, conectados.
nx.number_connected_components(graph): quantos componentes (subgrafos desconectados) existem.
nx.connected_components(graph): conjuntos de nós em cada componente.
Clustering / coesão local:

nx.average_clustering(graph): coeficiente médio de clustering, indica quantos triângulos ou “amigos em comum” existem.
nx.transitivity(graph): razão entre triângulos e tríades possíveis; outra medida de “triangulação” social.
Distâncias (se o grafo é conectado):

nx.diameter(graph): maior distância mínima entre qualquer par de nós (tamanho da “rede” em termos de hops).
nx.radius(graph): menor distância máxima de um nó para todos os outros (centralidade estrutural da rede).
nx.average_shortest_path_length(graph): comprimento médio dos caminhos mais curtos (quão “pequeno” é o mundo).
Distribuição de grau (graph.degree())

Calcula mínimo, máximo, média e desvio padrão do grau dos nós – útil para ver se há hubs ou se é uma rede mais homogênea.
5. Parte não-estritamente-grafo (padrões suspeitos e visualização)

Embora ainda use o grafo social, a lógica aqui é mais de análise de atributos e tempo do que algoritmos de teoria de grafos:

SuspiciousPatternDetector:

detect_age_based_anomalies: percorre arestas (conexões) e marca adultos conectados a menores com grande diferença de idade.
detect_content_consumption_clusters: agrupa por conteúdo e detecta clusters de adultos consumindo conteúdo infantil.
analyze_interaction_timing: analisa horários de interações com conteúdo infantil (especialmente horário escolar).
NetworkVisualizer:

Usa layouts de grafo do NetworkX (nx.spring_layout, nx.circular_layout, etc.) para desenhar a rede e as comunidades.
Usa seaborn/matplotlib para histogramas, box plots e heatmaps (não são algoritmos de grafo, são de visualização/estatística).
Se você quiser, posso pegar um exemplo pequeno de grafo (tipo 6–8 nós) e te mostrar, passo a passo, como cada uma dessas métricas se comporta nesse exemplo, ou explicar matematicamente algum algoritmo específico (por exemplo, aprofundar em PageRank ou Louvain).

https://www.canva.com/design/DAG5ARA-fNk/rEr4Mo_hgfrfiscPHNuKtg/edit
