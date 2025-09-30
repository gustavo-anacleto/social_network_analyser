# content_analyzer.py - Análise de padrões de consumo de conteúdo

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re

class ContentAnalyzer:
    """Classe especializada em análise de padrões de consumo de conteúdo"""
    
    def __init__(self):
        self.content_patterns = {}
        self.risk_keywords = {
            'high_risk': ['criança', 'menino', 'menina', 'bebê', 'infantil', 'kids', 'children'],
            'medium_risk': ['jovem', 'adolescente', 'teen', 'escola', 'school'],
            'suspicious_actions': ['baixar', 'download', 'salvar', 'share', 'compartilhar']
        }
    
    def classify_content_risk(self, content_metadata: Dict) -> Dict:
        """Classifica o nível de risco de um conteúdo"""
        risk_score = 0.0
        risk_factors = []
        
        # Análise de idade alvo
        target_age_max = content_metadata.get('target_age_max', 100)
        target_age_min = content_metadata.get('target_age_min', 0)
        
        if target_age_max <= 8:
            risk_score += 0.8
            risk_factors.append('Conteúdo para crianças muito pequenas')
        elif target_age_max <= 12:
            risk_score += 0.6
            risk_factors.append('Conteúdo infantil')
        elif target_age_max <= 16:
            risk_score += 0.3
            risk_factors.append('Conteúdo adolescente')
        
        # Análise de título e descrição
        text_content = f"{content_metadata.get('title', '')} {content_metadata.get('description', '')}"
        text_content = text_content.lower()
        
        for keyword in self.risk_keywords['high_risk']:
            if keyword in text_content:
                risk_score += 0.3
                risk_factors.append(f'Palavra-chave de alto risco: {keyword}')
        
        for keyword in self.risk_keywords['medium_risk']:
            if keyword in text_content:
                risk_score += 0.1
                risk_factors.append(f'Palavra-chave de médio risco: {keyword}')
        
        # Análise de categoria
        category = content_metadata.get('category', '').lower()
        if category in ['kids', 'children', 'family', 'educational']:
            risk_score += 0.2
            risk_factors.append(f'Categoria suspeita: {category}')
        
        # Análise de duração (vídeos muito curtos podem ser suspeitos)
        duration = content_metadata.get('duration_seconds', 0)
        if 0 < duration < 60:  # Menos de 1 minuto
            risk_score += 0.1
            risk_factors.append('Duração muito curta')
        
        return {
            'risk_score': min(1.0, risk_score),
            'risk_level': self._get_risk_level(min(1.0, risk_score)),
            'risk_factors': risk_factors
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Converte score numérico em nível de risco"""
        if score >= 0.7:
            return 'ALTO'
        elif score >= 0.4:
            return 'MÉDIO'
        elif score >= 0.2:
            return 'BAIXO'
        else:
            return 'MÍNIMO'
    
    def analyze_user_content_patterns(self, user_profiles: Dict, content_data: Dict) -> Dict:
        """Analisa padrões de consumo de conteúdo por usuário"""
        user_patterns = {}
        
        for user_id, profile in user_profiles.items():
            if len(profile['content_consumed']) == 0:
                continue
            
            pattern_analysis = {
                'user_id': user_id,
                'age': profile['age'],
                'total_interactions': len(profile['content_consumed']),
                'content_types': defaultdict(int),
                'risk_distribution': defaultdict(int),
                'temporal_patterns': self._analyze_temporal_patterns(profile['content_consumed']),
                'interaction_types': defaultdict(int),
                'suspicious_indicators': []
            }
            
            total_risk_score = 0
            high_risk_content_count = 0
            
            for interaction in profile['content_consumed']:
                content_id = interaction['content_id']
                interaction_type = interaction['interaction_type']
                
                # Conta tipos de conteúdo
                pattern_analysis['content_types'][interaction['content_type']] += 1
                pattern_analysis['interaction_types'][interaction_type] += 1
                
                # Analisa risco do conteúdo
                if content_id in content_data:
                    content_risk = self.classify_content_risk(content_data[content_id]['metadata'])
                    risk_level = content_risk['risk_level']
                    
                    pattern_analysis['risk_distribution'][risk_level] += 1
                    total_risk_score += content_risk['risk_score']
                    
                    if risk_level in ['ALTO', 'MÉDIO']:
                        high_risk_content_count += 1
                    
                    # Verifica ações suspeitas
                    if interaction_type in ['download', 'save', 'share']:
                        if risk_level in ['ALTO', 'MÉDIO']:
                            pattern_analysis['suspicious_indicators'].append(
                                f'{interaction_type} em conteúdo de risco {risk_level}'
                            )
            
            # Calcula métricas resumo
            pattern_analysis['avg_risk_score'] = total_risk_score / len(profile['content_consumed'])
            pattern_analysis['high_risk_ratio'] = high_risk_content_count / len(profile['content_consumed'])
            
            # Detecta padrões suspeitos específicos
            self._detect_suspicious_patterns(pattern_analysis, profile)
            
            user_patterns[user_id] = pattern_analysis
        
        return user_patterns
    
    def _analyze_temporal_patterns(self, interactions: List[Dict]) -> Dict:
        """Analisa padrões temporais de consumo"""
        timestamps = [interaction.get('timestamp') for interaction in interactions 
                     if interaction.get('timestamp')]
        
        if not timestamps:
            return {'error': 'Sem dados temporais'}
        
        # Análise por hora do dia
        hours = [ts.hour for ts in timestamps if hasattr(ts, 'hour')]
        hour_distribution = Counter(hours)
        
        # Análise por dia da semana
        weekdays = [ts.weekday() for ts in timestamps if hasattr(ts, 'weekday')]
        weekday_distribution = Counter(weekdays)
        
        # Detecta concentrações suspeitas
        peak_hours = [hour for hour, count in hour_distribution.items() 
                     if count > len(hours) * 0.2]  # Mais de 20% em uma hora
        
        # Horários escolares (8h-17h em dias úteis)
        school_time_interactions = sum(1 for ts in timestamps 
                                     if hasattr(ts, 'hour') and hasattr(ts, 'weekday')
                                     and 8 <= ts.hour <= 17 and ts.weekday() < 5)
        
        school_time_ratio = school_time_interactions / len(timestamps) if timestamps else 0
        
        return {
            'hour_distribution': dict(hour_distribution),
            'weekday_distribution': dict(weekday_distribution),
            'peak_hours': peak_hours,
            'school_time_ratio': school_time_ratio,
            'total_interactions': len(timestamps)
        }
    
    def _detect_suspicious_patterns(self, pattern_analysis: Dict, profile: Dict):
        """Detecta padrões específicos suspeitos"""
        age = profile['age']
        
        # Padrão 1: Adulto consumindo muito conteúdo infantil
        if age >= 18:
            high_risk_ratio = pattern_analysis['high_risk_ratio']
            if high_risk_ratio > 0.3:  # Mais de 30% conteúdo de alto risco
                pattern_analysis['suspicious_indicators'].append(
                    f'Adulto ({age} anos) com {high_risk_ratio:.1%} de conteúdo de alto risco'
                )
        
        # Padrão 2: Consumo concentrado em horários específicos
        temporal = pattern_analysis['temporal_patterns']
        if 'school_time_ratio' in temporal and temporal['school_time_ratio'] > 0.6:
            pattern_analysis['suspicious_indicators'].append(
                'Alto consumo em horário escolar (possível targeting de menores)'
            )
        
        # Padrão 3: Muitas ações de download/share em conteúdo suspeito
        download_actions = pattern_analysis['interaction_types'].get('download', 0)
        share_actions = pattern_analysis['interaction_types'].get('share', 0)
        total_actions = download_actions + share_actions
        
        if total_actions > 5 and pattern_analysis['high_risk_ratio'] > 0.2:
            pattern_analysis['suspicious_indicators'].append(
                f'{total_actions} ações de download/compartilhamento em conteúdo suspeito'
            )
        
        # Padrão 4: Diversidade baixa de tipos de conteúdo (muito focado)
        content_types = pattern_analysis['content_types']
        if len(content_types) <= 2 and pattern_analysis['total_interactions'] > 10:
            dominant_types = list(content_types.keys())
            if any(ctype in ['kids_video', 'children_game', 'educational_kids'] 
                   for ctype in dominant_types):
                pattern_analysis['suspicious_indicators'].append(
                    f'Consumo muito focado em poucos tipos: {dominant_types}'
                )
    
    def generate_content_risk_report(self, user_patterns: Dict, content_data: Dict) -> Dict:
        """Gera relatório completo de análise de risco de conteúdo"""
        
        # Análise de usuários por nível de risco
        risk_summary = {
            'ALTO': [],
            'MÉDIO': [],
            'BAIXO': [],
            'MÍNIMO': []
        }
        
        for user_id, pattern in user_patterns.items():
            if pattern['age'] < 18:  # Ignora menores
                continue
            
            avg_risk = pattern['avg_risk_score']
            high_risk_ratio = pattern['high_risk_ratio']
            num_indicators = len(pattern['suspicious_indicators'])
            
            # Score combinado
            combined_score = (avg_risk * 0.4 + high_risk_ratio * 0.4 + 
                            min(1.0, num_indicators / 5) * 0.2)
            
            risk_level = self._get_risk_level(combined_score)
            
            user_summary = {
                'user_id': user_id,
                'age': pattern['age'],
                'combined_score': combined_score,
                'avg_risk_score': avg_risk,
                'high_risk_ratio': high_risk_ratio,
                'suspicious_indicators': pattern['suspicious_indicators'],
                'total_interactions': pattern['total_interactions']
            }
            
            risk_summary[risk_level].append(user_summary)
        
        # Ordena por score dentro de cada categoria
        for level in risk_summary:
            risk_summary[level].sort(key=lambda x: x['combined_score'], reverse=True)
        
        # Análise de conteúdo mais problemático
        content_risk_analysis = {}
        for content_id, content_info in content_data.items():
            risk_info = self.classify_content_risk(content_info['metadata'])
            interactions_count = len(content_info['interactions'])
            
            adult_interactions = sum(1 for interaction in content_info['interactions']
                                   if interaction['user_id'] in user_patterns and
                                   user_patterns[interaction['user_id']]['age'] >= 18)
            
            if adult_interactions > 0 and risk_info['risk_score'] > 0.3:
                content_risk_analysis[content_id] = {
                    'content_id': content_id,
                    'risk_score': risk_info['risk_score'],
                    'risk_level': risk_info['risk_level'],
                    'total_interactions': interactions_count,
                    'adult_interactions': adult_interactions,
                    'adult_ratio': adult_interactions / interactions_count,
                    'risk_factors': risk_info['risk_factors']
                }
        
        # Ordena conteúdos por risco
        problematic_content = sorted(content_risk_analysis.values(),
                                   key=lambda x: x['risk_score'] * x['adult_ratio'],
                                   reverse=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_users_analyzed': len([p for p in user_patterns.values() if p['age'] >= 18]),
                'high_risk_users': len(risk_summary['ALTO']),
                'medium_risk_users': len(risk_summary['MÉDIO']),
                'total_content_analyzed': len(content_data),
                'problematic_content_count': len(problematic_content)
            },
            'user_risk_analysis': risk_summary,
            'problematic_content': problematic_content[:20],  # Top 20
            'recommendations': self._generate_content_recommendations(risk_summary, problematic_content)
        }
        
        return report
    
    def _generate_content_recommendations(self, risk_summary: Dict, problematic_content: List) -> List[str]:
        """Gera recomendações baseadas na análise de conteúdo"""
        recommendations = []
        
        high_risk_count = len(risk_summary['ALTO'])
        if high_risk_count > 0:
            recommendations.append(
                f"AÇÃO IMEDIATA: {high_risk_count} usuários de alto risco identificados. "
                "Recomenda-se investigação detalhada de seus padrões de consumo."
            )
        
        if len(problematic_content) > 10:
            recommendations.append(
                f"CONTEÚDO PROBLEMÁTICO: {len(problematic_content)} conteúdos com alta "
                "interação de adultos em material infantil. Considere revisão e "
                "possível remoção."
            )
        
        # Analisa padrões temporais preocupantes
        school_time_users = []
        for level in ['ALTO', 'MÉDIO']:
            for user in risk_summary[level]:
                # Esta verificação precisaria dos dados temporais do usuário
                pass
        
        recommendations.append(
            "MONITORAMENTO: Implemente alertas automáticos para usuários adultos "
            "com consumo súbito de conteúdo infantil."
        )
        
        recommendations.append(
            "PREVENÇÃO: Considere implementar verificações de idade mais rigorosas "
            "e limitações de acesso a conteúdo infantil para usuários adultos."
        )
        
        return recommendations

class ContentSimilarityAnalyzer:
    """Análise de similaridade entre conteúdos para detectar padrões"""
    
    def __init__(self):
        self.similarity_threshold = 0.7
    
    def calculate_content_similarity(self, content1: Dict, content2: Dict) -> float:
        """Calcula similaridade entre dois conteúdos"""
        similarity_score = 0.0
        
        # Similaridade de tipo
        if content1.get('content_type') == content2.get('content_type'):
            similarity_score += 0.3
        
        # Similaridade de idade alvo
        age1_max = content1.get('metadata', {}).get('target_age_max', 100)
        age2_max = content2.get('metadata', {}).get('target_age_max', 100)
        
        age_diff = abs(age1_max - age2_max)
        age_similarity = max(0, 1 - age_diff / 20)  # Normaliza por 20 anos
        similarity_score += age_similarity * 0.3
        
        # Similaridade textual (título e descrição)
        text1 = f"{content1.get('metadata', {}).get('title', '')} {content1.get('metadata', {}).get('description', '')}"
        text2 = f"{content2.get('metadata', {}).get('title', '')} {content2.get('metadata', {}).get('description', '')}"
        
        text_similarity = self._calculate_text_similarity(text1, text2)
        similarity_score += text_similarity * 0.4
        
        return min(1.0, similarity_score)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade textual simples baseada em palavras comuns"""
        if not text1 or not text2:
            return 0.0
        
        # Limpa e tokeniza texto
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        # Calcula Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def find_content_clusters(self, content_data: Dict) -> List[List[str]]:
        """Encontra clusters de conteúdo similar"""
        content_ids = list(content_data.keys())
        clusters = []
        processed = set()
        
        for i, content_id1 in enumerate(content_ids):
            if content_id1 in processed:
                continue
            
            cluster = [content_id1]
            processed.add(content_id1)
            
            for j, content_id2 in enumerate(content_ids[i+1:], i+1):
                if content_id2 in processed:
                    continue
                
                similarity = self.calculate_content_similarity(
                    content_data[content_id1], 
                    content_data[content_id2]
                )
                
                if similarity >= self.similarity_threshold:
                    cluster.append(content_id2)
                    processed.add(content_id2)
            
            if len(cluster) > 1:  # Só inclui clusters com múltiplos itens
                clusters.append(cluster)
        
        return clusters