# graph_utils.py - Utilitários para manipulação de grafos

import networkx as nx
import numpy as np
from typing import Dict, List, Set, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

class GraphAnalyzer:
    """Classe para análises avançadas de grafos"""
    
    @staticmethod
    def detect_communities(graph: nx.Graph, method: str = 'louvain') -> Dict[str, int]:
        """
        Detecta comunidades no grafo usando diferentes algoritmos
        
        Args:
            graph: Grafo NetworkX
            method: Método de detecção ('louvain', 'greedy', 'label_propagation')
        
        Returns:
            Dicionário mapeando nós para IDs de comunidade
        """
        if method == 'louvain':
            try:
                import community as community_louvain # type: ignore
                partition = community_louvain.best_partition(graph)
                return partition
            except ImportError:
                print("Biblioteca python-louvain não instalada. Usando método greedy.")
                method = 'greedy'
        
        if method == 'greedy':
            communities = nx.community.greedy_modularity_communities(graph)
        elif method == 'label_propagation':
            communities = nx.community.label_propagation_communities(graph)
        else:
            raise ValueError(f"Método {method} não suportado")
        
        # Converte para formato de dicionário
        partition = {}
        for i, community in enumerate(communities):
            for node in community:
                partition[node] = i
        
        return partition
    
    @staticmethod
    def calculate_advanced_centralities(graph: nx.Graph) -> Dict[str, Dict[str, float]]:
        """Calcula métricas avançadas de centralidade"""
        metrics = {}
        
        # Métricas básicas
        degree_cent = nx.degree_centrality(graph)
        betweenness_cent = nx.betweenness_centrality(graph)
        closeness_cent = nx.closeness_centrality(graph)
        
        # Métricas avançadas
        try:
            eigenvector_cent = nx.eigenvector_centrality(graph, max_iter=1000)
        except:
            eigenvector_cent = {node: 0.0 for node in graph.nodes()}
        
        try:
            katz_cent = nx.katz_centrality(graph, alpha=0.1)
        except:
            katz_cent = {node: 0.0 for node in graph.nodes()}
        
        # Page Rank
        pagerank = nx.pagerank(graph, alpha=0.85)
        
        # Combina todas as métricas
        for node in graph.nodes():
            metrics[node] = {
                'degree': degree_cent.get(node, 0),
                'betweenness': betweenness_cent.get(node, 0),
                'closeness': closeness_cent.get(node, 0),
                'eigenvector': eigenvector_cent.get(node, 0),
                'katz': katz_cent.get(node, 0),
                'pagerank': pagerank.get(node, 0)
            }
        
        return metrics
    
    @staticmethod
    def find_bridges_and_articulation_points(graph: nx.Graph) -> Dict[str, List]:
        """Encontra pontes e pontos de articulação no grafo"""
        bridges = list(nx.bridges(graph))
        articulation_points = list(nx.articulation_points(graph))
        
        return {
            'bridges': bridges,
            'articulation_points': articulation_points
        }
    
    @staticmethod
    def analyze_graph_structure(graph: nx.Graph) -> Dict:
        """Análise estrutural completa do grafo"""
        analysis = {
            'basic_stats': {
                'nodes': graph.number_of_nodes(),
                'edges': graph.number_of_edges(),
                'density': nx.density(graph),
                'is_connected': nx.is_connected(graph)
            },
            'components': {
                'connected_components': nx.number_connected_components(graph),
                'largest_component_size': len(max(nx.connected_components(graph), key=len)) if graph.nodes() else 0
            },
            'clustering': {
                'average_clustering': nx.average_clustering(graph),
                'transitivity': nx.transitivity(graph)
            }
        }
        
        # Adiciona diâmetro se o grafo for conectado
        if analysis['basic_stats']['is_connected']:
            analysis['distance_metrics'] = {
                'diameter': nx.diameter(graph),
                'radius': nx.radius(graph),
                'average_shortest_path': nx.average_shortest_path_length(graph)
            }
        
        # Distribução de graus
        degrees = dict(graph.degree())
        degree_values = list(degrees.values())
        if degree_values:
            analysis['degree_distribution'] = {
                'min_degree': min(degree_values),
                'max_degree': max(degree_values),
                'avg_degree': np.mean(degree_values),
                'degree_std': np.std(degree_values)
            }
        
        return analysis

class SuspiciousPatternDetector:
    """Classe especializada em detectar padrões suspeitos em redes sociais"""
    
    def __init__(self, age_gap_threshold: int = 15):
        self.age_gap_threshold = age_gap_threshold
        self.suspicious_patterns = []
    
    def detect_age_based_anomalies(self, graph: nx.Graph, user_profiles: Dict) -> List[Dict]:
        """Detecta conexões anômalas baseadas na diferença de idade"""
        anomalies = []
        
        for edge in graph.edges():
            user1, user2 = edge
            
            if user1 in user_profiles and user2 in user_profiles:
                age1 = user_profiles[user1].get('age', 0)
                age2 = user_profiles[user2].get('age', 0)
                
                age_gap = abs(age1 - age2)
                
                if age_gap >= self.age_gap_threshold:
                    # Verifica se um é adulto e outro menor
                    if (age1 >= 18 and age2 < 18) or (age2 >= 18 and age1 < 18):
                        adult_id = user1 if age1 >= 18 else user2
                        minor_id = user2 if age2 < 18 else user1
                        adult_age = age1 if age1 >= 18 else age2
                        minor_age = age2 if age2 < 18 else age1
                        
                        anomalies.append({
                            'type': 'adult_minor_connection',
                            'adult_id': adult_id,
                            'minor_id': minor_id,
                            'adult_age': adult_age,
                            'minor_age': minor_age,
                            'age_gap': age_gap,
                            'risk_score': min(1.0, age_gap / 30)
                        })
        
        return sorted(anomalies, key=lambda x: x['risk_score'], reverse=True)
    
    def detect_content_consumption_clusters(self, user_profiles: Dict, content_data: Dict) -> List[Dict]:
        """Detecta grupos de usuários com padrões similares de consumo suspeito"""
        # Agrupa usuários por tipo de conteúdo consumido
        content_consumers = defaultdict(list)
        
        for user_id, profile in user_profiles.items():
            if profile['age'] < 18:  # Ignora menores
                continue
                
            child_content_count = 0
            for interaction in profile['content_consumed']:
                content_id = interaction['content_id']
                if content_id in content_data:
                    content_info = content_data[content_id]
                    metadata = content_info.get('metadata', {})
                    
                    if (content_info['content_type'] in ['kids_video', 'children_game', 'educational_kids'] or
                        metadata.get('target_age_max', 100) < 13):
                        child_content_count += 1
                        content_consumers[content_id].append({
                            'user_id': user_id,
                            'age': profile['age'],
                            'interaction_type': interaction['interaction_type']
                        })
            
            if child_content_count >= 3:  # Threshold para considerar suspeito
                profile['child_content_count'] = child_content_count
        
        # Identifica conteúdos com múltiplos adultos consumindo
        suspicious_clusters = []
        for content_id, consumers in content_consumers.items():
            adult_consumers = [c for c in consumers if c['age'] >= 18]
            
            if len(adult_consumers) >= 2:  # Pelo menos 2 adultos
                avg_age = np.mean([c['age'] for c in adult_consumers])
                
                suspicious_clusters.append({
                    'content_id': content_id,
                    'adult_consumer_count': len(adult_consumers),
                    'consumers': adult_consumers,
                    'avg_consumer_age': avg_age,
                    'risk_score': min(1.0, len(adult_consumers) / 10)
                })
        
        return sorted(suspicious_clusters, key=lambda x: x['risk_score'], reverse=True)
    
    def analyze_interaction_timing(self, user_profiles: Dict) -> List[Dict]:
        """Analisa padrões temporais suspeitos nas interações"""
        timing_anomalies = []
        
        for user_id, profile in user_profiles.items():
            if profile['age'] < 18 or len(profile['content_consumed']) < 5:
                continue
            
            # Analisa horários de consumo de conteúdo infantil
            child_content_hours = []
            total_interactions = len(profile['content_consumed'])
            
            for interaction in profile['content_consumed']:
                timestamp = interaction.get('timestamp')
                if timestamp and hasattr(timestamp, 'hour'):
                    # Verifica se é conteúdo infantil
                    content_type = interaction['content_type']
                    metadata = interaction.get('metadata', {})
                    
                    if (content_type in ['kids_video', 'children_game', 'educational_kids'] or
                        metadata.get('target_age_max', 100) < 13):
                        child_content_hours.append(timestamp.hour)
            
            if len(child_content_hours) >= 5:  # Mínimo de interações para análise
                # Verifica se há concentração em horários específicos
                hour_counts = defaultdict(int)
                for hour in child_content_hours:
                    hour_counts[hour] += 1
                
                # Identifica horários de pico (mais de 30% das interações)
                peak_hours = [hour for hour, count in hour_counts.items() 
                            if count / len(child_content_hours) > 0.3]
                
                # Horários suspeitos (período escolar para crianças: 8h-17h)
                school_hours_interaction = sum(1 for hour in child_content_hours 
                                             if 8 <= hour <= 17)
                school_hours_ratio = school_hours_interaction / len(child_content_hours)
                
                if school_hours_ratio > 0.6:  # Muito consumo em horário escolar
                    timing_anomalies.append({
                        'user_id': user_id,
                        'age': profile['age'],
                        'school_hours_ratio': school_hours_ratio,
                        'total_child_content_interactions': len(child_content_hours),
                        'peak_hours': peak_hours,
                        'risk_score': min(1.0, school_hours_ratio * 1.5)
                    })
        
        return sorted(timing_anomalies, key=lambda x: x['risk_score'], reverse=True)

class NetworkVisualizer:
    """Classe para visualização avançada de redes"""
    
    @staticmethod
    def plot_centrality_distribution(centrality_metrics: Dict, metric_name: str = 'degree'):
        """Plota distribuição de uma métrica de centralidade"""
        values = [metrics[metric_name] for metrics in centrality_metrics.values()]
        
        plt.figure(figsize=(12, 6))
        
        # Histograma
        plt.subplot(1, 2, 1)
        plt.hist(values, bins=20, alpha=0.7, edgecolor='black')
        plt.title(f'Distribuição de {metric_name.title()} Centrality')
        plt.xlabel(f'{metric_name.title()} Centrality')
        plt.ylabel('Frequência')
        plt.grid(True, alpha=0.3)
        
        # Box plot
        plt.subplot(1, 2, 2)
        plt.boxplot(values)
        plt.title(f'{metric_name.title()} Centrality - Box Plot')
        plt.ylabel(f'{metric_name.title()} Centrality')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_community_structure(graph: nx.Graph, communities: Dict, layout: str = 'spring'):
        """Visualiza estrutura de comunidades no grafo"""
        plt.figure(figsize=(15, 10))
        
        # Define layout
        if layout == 'spring':
            pos = nx.spring_layout(graph, k=2, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(graph)
        else:
            pos = nx.random_layout(graph)
        
        # Gera cores para comunidades
        unique_communities = set(communities.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_communities)))
        community_colors = {comm: colors[i] for i, comm in enumerate(unique_communities)}
        
        # Cores dos nós baseadas na comunidade
        node_colors = [community_colors[communities.get(node, 0)] for node in graph.nodes()]
        
        # Desenha o grafo
        nx.draw(graph, pos,
                node_color=node_colors,
                node_size=300,
                with_labels=True,
                font_size=8,
                font_weight='bold',
                edge_color='gray',
                alpha=0.8)
        
        plt.title(f'Estrutura de Comunidades\n({len(unique_communities)} comunidades detectadas)', 
                  fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_risk_heatmap(user_profiles: Dict, suspicious_users: List[Dict]):
        """Cria heatmap de scores de risco por idade"""
        # Prepara dados para o heatmap
        age_risk_data = defaultdict(list)
        
        for user in suspicious_users:
            age_group = f"{(user['age'] // 10) * 10}-{(user['age'] // 10) * 10 + 9}"
            age_risk_data[age_group].append(user['suspicion_score'])
        
        # Calcula estatísticas por grupo de idade
        heatmap_data = []
        age_groups = sorted(age_risk_data.keys())
        
        for age_group in age_groups:
            scores = age_risk_data[age_group]
            heatmap_data.append([
                len(scores),  # Quantidade
                np.mean(scores),  # Score médio
                np.max(scores),  # Score máximo
                np.std(scores) if len(scores) > 1 else 0  # Desvio padrão
            ])
        
        # Cria heatmap
        plt.figure(figsize=(12, 8))
        
        metrics = ['Quantidade', 'Score Médio', 'Score Máximo', 'Desvio Padrão']
        
        # Normaliza dados para melhor visualização
        heatmap_array = np.array(heatmap_data).T
        
        for i in range(heatmap_array.shape[0]):
            if heatmap_array[i].max() > 0:
                heatmap_array[i] = heatmap_array[i] / heatmap_array[i].max()
        
        sns.heatmap(heatmap_array, 
                   xticklabels=age_groups,
                   yticklabels=metrics,
                   annot=True, 
                   fmt='.2f',
                   cmap='Reds',
                   cbar_kws={'label': 'Score Normalizado'})
        
        plt.title('Heatmap de Risco por Faixa Etária', fontsize=14, fontweight='bold')
        plt.xlabel('Faixa Etária')
        plt.ylabel('Métricas de Risco')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_network_evolution(graph_snapshots: List[nx.Graph], titles: List[str] = None):
        """Visualiza evolução da rede ao longo do tempo"""
        n_snapshots = len(graph_snapshots)
        
        if n_snapshots == 0:
            return
        
        fig, axes = plt.subplots(1, min(n_snapshots, 4), figsize=(5*min(n_snapshots, 4), 5))
        
        if n_snapshots == 1:
            axes = [axes]
        
        for i, graph in enumerate(graph_snapshots[:4]):
            ax = axes[i] if n_snapshots > 1 else axes[0]
            
            pos = nx.spring_layout(graph, k=1, iterations=30)
            
            nx.draw(graph, pos,
                   ax=ax,
                   node_color='lightblue',
                   node_size=200,
                   with_labels=True,
                   font_size=6,
                   edge_color='gray',
                   alpha=0.7)
            
            title = titles[i] if titles and i < len(titles) else f'Snapshot {i+1}'
            ax.set_title(title)
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()