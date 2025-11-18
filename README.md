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