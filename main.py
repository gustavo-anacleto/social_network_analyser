# main.py - Módulo Principal do Analisador de Redes Sociais

import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class SocialNetworkAnalyzer:
    """
    Classe principal para análise de redes sociais focada em detecção
    de padrões suspeitos de consumo de conteúdo.
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        self.user_profiles = {}
        self.content_data = {}
        self.suspicious_patterns = []
        
    def add_user(self, user_id: str, age: int, profile_data: dict = None):
        """Adiciona um usuário ao grafo com seus dados de perfil"""
        self.graph.add_node(user_id)
        
        profile = {
            'user_id': user_id,
            'age': age,
            'registration_date': datetime.now(),
            'suspicious_score': 0.0,
            'content_consumed': [],
            'connections': []
        }
        
        if profile_data:
            profile.update(profile_data)
            
        self.user_profiles[user_id] = profile
    
    def add_connection(self, user1: str, user2: str, connection_type: str = 'friend', weight: float = 1.0):
        """Adiciona uma conexão entre dois usuários"""
        if user1 in self.user_profiles and user2 in self.user_profiles:
            self.graph.add_edge(user1, user2, 
                              connection_type=connection_type, 
                              weight=weight,
                              timestamp=datetime.now())
            
            # Atualiza listas de conexões
            self.user_profiles[user1]['connections'].append(user2)
            self.user_profiles[user2]['connections'].append(user1)
    
    def add_content_interaction(self, user_id: str, content_id: str, 
                              content_type: str, interaction_type: str = 'view',
                              content_metadata: dict = None):
        """Registra interação de usuário com conteúdo"""
        if user_id not in self.user_profiles:
            return False
            
        interaction = {
            'content_id': content_id,
            'content_type': content_type,
            'interaction_type': interaction_type,
            'timestamp': datetime.now(),
            'metadata': content_metadata or {}
        }
        
        self.user_profiles[user_id]['content_consumed'].append(interaction)
        
        # Armazena dados do conteúdo se não existir
        if content_id not in self.content_data:
            self.content_data[content_id] = {
                'content_id': content_id,
                'content_type': content_type,
                'interactions': [],
                'flags': [],
                'metadata': content_metadata or {}
            }
        
        self.content_data[content_id]['interactions'].append({
            'user_id': user_id,
            'interaction_type': interaction_type,
            'timestamp': datetime.now()
        })
        
        return True
    
    def calculate_user_centrality_metrics(self) -> Dict[str, Dict[str, float]]:
        """Calcula métricas de centralidade para todos os usuários"""
        centrality_metrics = {}
        
        # Centralidade de grau
        degree_centrality = nx.degree_centrality(self.graph)
        
        # Centralidade de intermediação
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        
        # Centralidade de proximidade
        closeness_centrality = nx.closeness_centrality(self.graph)
        
        # Centralidade de autovetor
        eigenvector_centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)
        
        for user_id in self.graph.nodes():
            centrality_metrics[user_id] = {
                'degree': degree_centrality.get(user_id, 0),
                'betweenness': betweenness_centrality.get(user_id, 0),
                'closeness': closeness_centrality.get(user_id, 0),
                'eigenvector': eigenvector_centrality.get(user_id, 0)
            }
        
        return centrality_metrics
    
    def detect_suspicious_content_patterns(self, min_age_gap: int = 10) -> List[Dict]:
        """
        Detecta padrões suspeitos baseados em:
        - Adultos consumindo muito conteúdo direcionado a crianças
        - Usuários com comportamentos anômalos de consumo
        """
        suspicious_users = []
        
        for user_id, profile in self.user_profiles.items():
            if profile['age'] < 18:  # Ignora menores de idade
                continue
                
            child_content_count = 0
            total_content_count = len(profile['content_consumed'])
            
            if total_content_count == 0:
                continue
            
            # Analisa conteúdo consumido
            for interaction in profile['content_consumed']:
                content_type = interaction['content_type']
                metadata = interaction.get('metadata', {})
                
                # Verifica se é conteúdo infantil
                if (content_type in ['kids_video', 'children_game', 'educational_kids'] or
                    metadata.get('target_age_max', 100) < 13):
                    child_content_count += 1
            
            # Calcula proporção de conteúdo infantil
            child_content_ratio = child_content_count / total_content_count
            
            # Define threshold suspeito baseado na idade e proporção
            age = profile['age']
            suspicion_threshold = max(0.1, 0.5 - (age - 25) * 0.02)  # Ajusta por idade
            
            if child_content_ratio > suspicion_threshold and child_content_count > 5:
                suspicion_score = min(1.0, child_content_ratio * 2)
                
                suspicious_users.append({
                    'user_id': user_id,
                    'age': age,
                    'child_content_ratio': child_content_ratio,
                    'child_content_count': child_content_count,
                    'total_content_count': total_content_count,
                    'suspicion_score': suspicion_score,
                    'connections_count': len(profile['connections'])
                })
                
                # Atualiza score no perfil
                self.user_profiles[user_id]['suspicious_score'] = suspicion_score
        
        return sorted(suspicious_users, key=lambda x: x['suspicion_score'], reverse=True)
    
    def analyze_suspicious_networks(self, suspicious_users: List[Dict]) -> Dict:
        """Analisa redes de conexões entre usuários suspeitos"""
        suspicious_user_ids = {user['user_id'] for user in suspicious_users}
        
        # Subgrafo com usuários suspeitos e suas conexões diretas
        extended_suspicious = set()
        for user_id in suspicious_user_ids:
            extended_suspicious.add(user_id)
            extended_suspicious.update(self.graph.neighbors(user_id))
        
        subgraph = self.graph.subgraph(extended_suspicious)
        
        # Encontra componentes conectados
        connected_components = list(nx.connected_components(subgraph))
        
        # Analisa cada componente
        network_analysis = {
            'total_suspicious_users': len(suspicious_user_ids),
            'connected_components': len(connected_components),
            'largest_component_size': max(len(comp) for comp in connected_components) if connected_components else 0,
            'components_analysis': []
        }
        
        for i, component in enumerate(connected_components):
            suspicious_in_component = component.intersection(suspicious_user_ids)
            
            if len(suspicious_in_component) > 1:  # Pelo menos 2 usuários suspeitos conectados
                component_subgraph = subgraph.subgraph(component)
                
                network_analysis['components_analysis'].append({
                    'component_id': i,
                    'total_users': len(component),
                    'suspicious_users': len(suspicious_in_component),
                    'suspicious_user_ids': list(suspicious_in_component),
                    'density': nx.density(component_subgraph),
                    'avg_clustering': nx.average_clustering(component_subgraph),
                    'diameter': nx.diameter(component_subgraph) if nx.is_connected(component_subgraph) else 'N/A'
                })
        
        return network_analysis
    
    def generate_risk_report(self) -> Dict:
        """Gera relatório completo de análise de risco"""
        # Detecta usuários suspeitos
        suspicious_users = self.detect_suspicious_content_patterns()
        
        # Analisa redes suspeitas
        network_analysis = self.analyze_suspicious_networks(suspicious_users)
        
        # Calcula métricas de centralidade
        centrality_metrics = self.calculate_user_centrality_metrics()
        
        # Identifica influenciadores suspeitos
        influential_suspicious = []
        for user in suspicious_users[:10]:  # Top 10 suspeitos
            user_id = user['user_id']
            if user_id in centrality_metrics:
                metrics = centrality_metrics[user_id]
                user_with_metrics = user.copy()
                user_with_metrics.update(metrics)
                influential_suspicious.append(user_with_metrics)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_users': len(self.user_profiles),
                'total_connections': self.graph.number_of_edges(),
                'suspicious_users_count': len(suspicious_users),
                'high_risk_users': len([u for u in suspicious_users if u['suspicion_score'] > 0.7])
            },
            'suspicious_users': suspicious_users[:20],  # Top 20
            'network_analysis': network_analysis,
            'influential_suspicious': influential_suspicious,
            'recommendations': self._generate_recommendations(suspicious_users, network_analysis)
        }
        
        return report
    
    def _generate_recommendations(self, suspicious_users: List[Dict], network_analysis: Dict) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        if len(suspicious_users) > 10:
            recommendations.append(
                f"ALERTA: {len(suspicious_users)} usuários com padrões suspeitos detectados. "
                "Recomenda-se investigação manual dos casos de maior risco."
            )
        
        high_risk_count = len([u for u in suspicious_users if u['suspicion_score'] > 0.7])
        if high_risk_count > 0:
            recommendations.append(
                f"PRIORIDADE ALTA: {high_risk_count} usuários com score de risco > 0.7. "
                "Estes casos requerem atenção imediata."
            )
        
        if network_analysis['connected_components'] > 0:
            recommendations.append(
                f"REDES IDENTIFICADAS: {network_analysis['connected_components']} grupos "
                "de usuários suspeitos conectados foram identificados. "
                "Investigar possíveis coordenação entre usuários."
            )
        
        large_components = [c for c in network_analysis['components_analysis'] 
                          if c['suspicious_users'] >= 3]
        if large_components:
            recommendations.append(
                f"REDES COMPLEXAS: {len(large_components)} grupos com 3+ usuários suspeitos "
                "conectados. Estas redes podem indicar atividade coordenada."
            )
        
        return recommendations
    
    def visualize_suspicious_network(self, output_file: str = 'suspicious_network.png'):
        """Visualiza a rede de usuários suspeitos"""
        suspicious_users = self.detect_suspicious_content_patterns()
        suspicious_user_ids = {user['user_id'] for user in suspicious_users}
        
        # Cria subgrafo com usuários suspeitos e vizinhos
        extended_suspicious = set()
        for user_id in suspicious_user_ids:
            extended_suspicious.add(user_id)
            extended_suspicious.update(list(self.graph.neighbors(user_id))[:5])  # Máximo 5 vizinhos
        
        subgraph = self.graph.subgraph(extended_suspicious)
        
        # Configurações de visualização
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(subgraph, k=3, iterations=50)
        
        # Cores dos nós baseadas no tipo
        node_colors = []
        node_sizes = []
        for node in subgraph.nodes():
            if node in suspicious_user_ids:
                score = next(u['suspicion_score'] for u in suspicious_users if u['user_id'] == node)
                node_colors.append('red' if score > 0.7 else 'orange')
                node_sizes.append(300 + score * 200)
            else:
                node_colors.append('lightblue')
                node_sizes.append(100)
        
        # Desenha o grafo
        nx.draw(subgraph, pos, 
                node_color=node_colors,
                node_size=node_sizes,
                with_labels=True,
                font_size=8,
                font_weight='bold',
                edge_color='gray',
                alpha=0.7)
        
        plt.title('Rede de Usuários Suspeitos\n(Vermelho: Alto Risco | Laranja: Médio Risco | Azul: Conexões)', 
                  fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()

# Exemplo de uso
if __name__ == "__main__":
    # Cria instância do analisador
    analyzer = SocialNetworkAnalyzer()
    
    # Exemplo de dados de teste
    # Adiciona usuários
    users_data = [
        ("user_001", 45, {"name": "João Silva"}),
        ("user_002", 23, {"name": "Maria Santos"}),
        ("user_003", 52, {"name": "Pedro Costa"}),
        ("user_004", 16, {"name": "Ana Oliveira"}),
        ("user_005", 38, {"name": "Carlos Mendes"}),
    ]
    
    for user_id, age, profile in users_data:
        analyzer.add_user(user_id, age, profile)
    
    # Adiciona conexões
    connections = [
        ("user_001", "user_002", "friend"),
        ("user_001", "user_003", "friend"),
        ("user_002", "user_004", "follower"),
        ("user_003", "user_005", "friend"),
    ]
    
    for user1, user2, conn_type in connections:
        analyzer.add_connection(user1, user2, conn_type)
    
    # Simula consumo de conteúdo suspeito
    suspicious_content = [
        ("user_001", "content_001", "kids_video", {"target_age_max": 8}),
        ("user_001", "content_002", "children_game", {"target_age_max": 10}),
        ("user_001", "content_003", "kids_video", {"target_age_max": 12}),
        ("user_003", "content_001", "kids_video", {"target_age_max": 8}),
        ("user_003", "content_004", "educational_kids", {"target_age_max": 6}),
    ]
    
    for user_id, content_id, content_type, metadata in suspicious_content:
        analyzer.add_content_interaction(user_id, content_id, content_type, "view", metadata)
    
    # Gera relatório
    report = analyzer.generate_risk_report()
    
    print("=== RELATÓRIO DE ANÁLISE DE RISCO ===")
    print(f"Usuários analisados: {report['summary']['total_users']}")
    print(f"Usuários suspeitos: {report['summary']['suspicious_users_count']}")
    print(f"Usuários de alto risco: {report['summary']['high_risk_users']}")
    
    print("\n=== RECOMENDAÇÕES ===")
    for rec in report['recommendations']:
        print(f"• {rec}")
    
    # Salva relatório em JSON
    with open('risk_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)