# exemplo_uso_completo.py - Demonstração completa do sistema

import random
from datetime import datetime, timedelta
import json

# Importa todos os módulos do sistema
from main import SocialNetworkAnalyzer
from graph_utils import GraphAnalyzer, SuspiciousPatternDetector, NetworkVisualizer
from content_analyzer import ContentAnalyzer, ContentSimilarityAnalyzer
from report_generator import ReportGenerator

def gerar_dados_simulados():
    """Gera dados simulados para demonstração do sistema"""
    
    print("🔄 Gerando dados simulados...")
    
    # Cria instância do analisador
    analyzer = SocialNetworkAnalyzer()
    
    # Simula usuários (mistura de idades para detectar padrões suspeitos)
    usuarios = []
    for i in range(50):
        user_id = f"user_{i:03d}"
        # Distribui idades: alguns adultos, alguns menores, alguns suspeitos
        if i < 10:  # Usuários suspeitos
            age = random.randint(25, 65)
        elif i < 30:  # Adultos normais
            age = random.randint(18, 70)
        else:  # Menores de idade
            age = random.randint(8, 17)
        
        profile_data = {
            "name": f"Usuario_{i}",
            "registration_date": datetime.now() - timedelta(days=random.randint(1, 365))
        }
        
        analyzer.add_user(user_id, age, profile_data)
        usuarios.append((user_id, age))
    
    # Simula conexões (alguns padrões suspeitos)
    print("📊 Criando conexões na rede...")
    for i in range(80):  # 80 conexões
        user1, user2 = random.sample(usuarios, 2)
        connection_type = random.choice(['friend', 'follower', 'mutual'])
        analyzer.add_connection(user1[0], user2[0], connection_type, random.uniform(0.5, 1.0))
    
    # Simula conteúdo e interações
    print("🎯 Simulando consumo de conteúdo...")
    
    # Tipos de conteúdo
    content_types = {
        'kids_video': {'target_age_max': random.randint(5, 12), 'category': 'kids'},
        'children_game': {'target_age_max': random.randint(6, 14), 'category': 'games'},
        'educational_kids': {'target_age_max': random.randint(4, 10), 'category': 'education'},
        'adult_content': {'target_age_max': 100, 'category': 'entertainment'},
        'teen_content': {'target_age_max': random.randint(13, 17), 'category': 'teen'}
    }
    
    # Cria conteúdos
    for i in range(100):
        content_id = f"content_{i:03d}"
        content_type = random.choice(list(content_types.keys()))
        metadata = content_types[content_type].copy()
        metadata.update({
            'title': f'Conteúdo {i} - {content_type}',
            'description': f'Descrição do {content_type}',
            'duration_seconds': random.randint(30, 3600)
        })
        
        # Simula interações - usuários suspeitos consomem mais conteúdo infantil
        for user_id, age in usuarios:
            # Probabilidade de interação baseada na idade e tipo de conteúdo
            if age >= 18:  # Adultos
                if content_type in ['kids_video', 'children_game', 'educational_kids']:
                    # Usuários suspeitos (primeiros 10) têm alta probabilidade
                    if user_id.endswith(('000', '001', '002', '003', '004', '005', '006', '007', '008', '009')):
                        prob = 0.7  # 70% de chance
                    else:
                        prob = 0.1  # 10% de chance (normal)
                else:
                    prob = 0.3  # Conteúdo adulto normal
            else:  # Menores
                if content_type in ['kids_video', 'children_game', 'educational_kids', 'teen_content']:
                    prob = 0.6
                else:
                    prob = 0.05  # Baixa chance de conteúdo adulto
            
            if random.random() < prob:
                interaction_type = random.choice(['view', 'like', 'share', 'download'])
                analyzer.add_content_interaction(user_id, content_id, content_type, interaction_type, metadata)
    
    return analyzer

def executar_analise_completa():
    """Executa análise completa do sistema"""
    
    print("🚀 Iniciando Sistema de Análise de Redes Sociais")
    print("=" * 60)
    
    # Gera dados simulados
    analyzer = gerar_dados_simulados()
    
    print("✅ Dados simulados gerados com sucesso!")
    print(f"📊 Usuários: {len(analyzer.user_profiles)}")
    print(f"🔗 Conexões: {analyzer.graph.number_of_edges()}")
    print(f"📱 Conteúdos: {len(analyzer.content_data)}")
    
    # 1. ANÁLISE PRINCIPAL DE RISCO
    print("\n🔍 EXECUTANDO ANÁLISE DE RISCO...")
    report_principal = analyzer.generate_risk_report()
    
    print(f"⚠️  Usuários suspeitos detectados: {len(report_principal['suspicious_users'])}")
    print(f"🚨 Usuários de alto risco: {report_principal['summary']['high_risk_users']}")
    
    # 2. ANÁLISE AVANÇADA DE GRAFOS
    print("\n📈 EXECUTANDO ANÁLISE AVANÇADA DE GRAFOS...")
    graph_analyzer = GraphAnalyzer()
    
    # Detecta comunidades
    communities = graph_analyzer.detect_communities(analyzer.graph)
    print(f"🏘️  Comunidades detectadas: {len(set(communities.values()))}")
    
    # Calcula métricas avançadas
    centrality_metrics = graph_analyzer.calculate_advanced_centralities(analyzer.graph)
    
    # Encontra pontos críticos
    critical_points = graph_analyzer.find_bridges_and_articulation_points(analyzer.graph)
    print(f"🌉 Pontes na rede: {len(critical_points['bridges'])}")
    print(f"📍 Pontos de articulação: {len(critical_points['articulation_points'])}")
    
    # 3. DETECÇÃO DE PADRÕES SUSPEITOS
    print("\n🕵️ DETECTANDO PADRÕES SUSPEITOS...")
    pattern_detector = SuspiciousPatternDetector()
    
    # Anomalias baseadas em idade
    age_anomalies = pattern_detector.detect_age_based_anomalies(analyzer.graph, analyzer.user_profiles)
    print(f"👥 Conexões suspeitas por idade: {len(age_anomalies)}")
    
    # Clusters de consumo
    content_clusters = pattern_detector.detect_content_consumption_clusters(
        analyzer.user_profiles, analyzer.content_data
    )
    print(f"📺 Clusters de consumo suspeito: {len(content_clusters)}")
    
    # Padrões temporais
    timing_anomalies = pattern_detector.analyze_interaction_timing(analyzer.user_profiles)
    print(f"⏰ Anomalias temporais: {len(timing_anomalies)}")
    
    # 4. ANÁLISE DE CONTEÚDO
    print("\n📋 ANALISANDO PADRÕES DE CONTEÚDO...")
    content_analyzer = ContentAnalyzer()
    
    # Padrões de usuário
    user_patterns = content_analyzer.analyze_user_content_patterns(
        analyzer.user_profiles, analyzer.content_data
    )
    
    # Relatório de conteúdo
    content_report = content_analyzer.generate_content_risk_report(
        user_patterns, analyzer.content_data
    )
    
    print(f"📊 Usuários analisados para conteúdo: {len(user_patterns)}")
    print(f"🎯 Conteúdo problemático: {len(content_report.get('problematic_content', []))}")
    
    # 5. ANÁLISE DE SIMILARIDADE
    print("\n🔗 ANALISANDO SIMILARIDADE DE CONTEÚDO...")
    similarity_analyzer = ContentSimilarityAnalyzer()
    content_clusters = similarity_analyzer.find_content_clusters(analyzer.content_data)
    print(f"📦 Clusters de conteúdo similar: {len(content_clusters)}")
    
    # 6. GERAÇÃO DE RELATÓRIOS
    print("\n📄 GERANDO RELATÓRIOS...")
    report_generator = ReportGenerator()
    
    # Relatório Excel completo
    excel_file = report_generator.generate_comprehensive_excel_report(
        report_principal, content_report
    )
    print(f"📊 Relatório Excel gerado: {excel_file}")
    
    # CSV resumido
    csv_file = report_generator.generate_summary_csv(report_principal)
    print(f"📄 CSV resumido gerado: {csv_file}")
    
    # 7. VISUALIZAÇÕES
    print("\n🎨 GERANDO VISUALIZAÇÕES...")
    try:
        # Visualiza rede suspeita
        analyzer.visualize_suspicious_network('reports/rede_suspeitos.png')
        print("📈 Gráfico de rede suspeita gerado: rede_suspeitos.png")
        
        # Visualiza comunidades
        visualizer = NetworkVisualizer()
        visualizer.plot_community_structure(analyzer.graph, communities)
        print("🏘️  Gráfico de comunidades gerado")
        
    except Exception as e:
        print(f"⚠️  Erro na geração de gráficos: {e}")
    
    # 8. SUMÁRIO FINAL
    print("\n" + "=" * 60)
    print("📋 SUMÁRIO FINAL DA ANÁLISE")
    print("=" * 60)
    
    print(f"👥 Total de usuários analisados: {len(analyzer.user_profiles)}")
    print(f"🔗 Total de conexões: {analyzer.graph.number_of_edges()}")
    print(f"⚠️  Usuários suspeitos: {len(report_principal['suspicious_users'])}")
    print(f"🚨 Usuários de alto risco: {report_principal['summary']['high_risk_users']}")
    print(f"🕸️  Componentes de rede: {report_principal['network_analysis']['connected_components']}")
    print(f"📺 Conteúdos problemáticos: {len(content_report.get('problematic_content', []))}")
    
    print("\n🎯 PRINCIPAIS RECOMENDAÇÕES:")
    for i, rec in enumerate(report_principal['recommendations'][:3], 1):
        print(f"{i}. {rec}")
    
    print("\n📁 ARQUIVOS GERADOS:")
    print(f"• {excel_file}")
    print(f"• {csv_file}")
    print("• rede_suspeitos.png (se gerado)")
    
    return {
        'analyzer': analyzer,
        'report_principal': report_principal,
        'content_report': content_report,
        'communities': communities,
        'centrality_metrics': centrality_metrics,
        'excel_file': excel_file,
        'csv_file': csv_file
    }

def exemplo_uso_real():
    """Exemplo de como usar o sistema com dados reais"""
    
    print("\n" + "=" * 60)
    print("💡 EXEMPLO DE USO COM DADOS REAIS")
    print("=" * 60)
    
    # Exemplo de como carregar dados reais
    exemplo_codigo = '''
# Para usar com dados reais, substitua os dados simulados por:

# 1. Carregue dados de usuários (ex: do banco de dados)
for user_data in load_users_from_database():
    analyzer.add_user(
        user_data['id'], 
        user_data['age'], 
        user_data['profile']
    )

# 2. Carregue conexões entre usuários
for connection in load_connections_from_database():
    analyzer.add_connection(
        connection['user1_id'],
        connection['user2_id'],
        connection['type'],
        connection['weight']
    )

# 3. Carregue interações com conteúdo
for interaction in load_content_interactions():
    analyzer.add_content_interaction(
        interaction['user_id'],
        interaction['content_id'],
        interaction['content_type'],
        interaction['interaction_type'],
        interaction['metadata']
    )

# 4. Execute a análise
report = analyzer.generate_risk_report()

# 5. Gere relatórios
report_generator = ReportGenerator()
excel_file = report_generator.generate_comprehensive_excel_report(report)
'''
    
    print(exemplo_codigo)

if __name__ == "__main__":
    try:
        # Executa análise completa
        resultados = executar_analise_completa()
        
        # Mostra exemplo de uso real
        exemplo_uso_real()
        
        print("\n✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("🔒 Lembre-se: Este sistema é para fins de segurança e proteção.")
        print("📞 Em casos suspeitos, sempre acione as autoridades competentes.")
        
    except Exception as e:
        print(f"\n❌ ERRO na execução: {e}")
        import traceback
        traceback.print_exc()