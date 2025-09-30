# report_generator.py - Geração de relatórios em formato de planilha Excel

import pandas as pd
from datetime import datetime
from typing import Dict, List
import os

class ReportGenerator:
    """Classe para geração de relatórios em formato de planilha Excel"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Garante que o diretório de saída existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_comprehensive_excel_report(self, analysis_data: Dict, content_analysis: Dict = None, filename: str = None) -> str:
        """
        Gera relatório completo em formato Excel com múltiplas abas
        
        Args:
            analysis_data: Dados da análise principal de risco
            content_analysis: Dados da análise de conteúdo (opcional)
            filename: Nome do arquivo (opcional, gera automaticamente se não fornecido)
        
        Returns:
            Caminho completo do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_analise_rede_social_{timestamp}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # ABA 1: RESUMO EXECUTIVO
            self._create_summary_sheet(analysis_data, writer)
            
            # ABA 2: USUÁRIOS SUSPEITOS DETALHADO
            self._create_suspicious_users_sheet(analysis_data, writer)
            
            # ABA 3: ANÁLISE DE REDES
            self._create_network_analysis_sheet(analysis_data, writer)
            
            # ABA 4: INFLUENCIADORES SUSPEITOS
            self._create_influencers_sheet(analysis_data, writer)
            
            # ABA 5: MÉTRICAS DE CENTRALIDADE
            self._create_centrality_metrics_sheet(analysis_data, writer)
            
            # ABA 6: PADRÕES DE CONTEÚDO (se disponível)
            if content_analysis:
                self._create_content_patterns_sheet(content_analysis, writer)
            
            # ABA 7: RECOMENDAÇÕES E AÇÕES
            self._create_recommendations_sheet(analysis_data, writer)
            
            # ABA 8: DADOS BRUTOS PARA INVESTIGAÇÃO
            self._create_raw_data_sheet(analysis_data, writer)
        
        print(f"✅ Relatório Excel gerado com sucesso: {filepath}")
        return filepath
    
    def _create_summary_sheet(self, analysis_data: Dict, writer):
        """Cria aba de resumo executivo"""
        summary = analysis_data.get('summary', {})
        network = analysis_data.get('network_analysis', {})
        
        # Calcula taxa de suspeição
        total_users = summary.get('total_users', 1)
        suspicious_count = summary.get('suspicious_users_count', 0)
        suspicion_rate = (suspicious_count / max(1, total_users)) * 100
        
        # Prepara dados do resumo
        summary_data = [
            ['MÉTRICA', 'VALOR', 'DESCRIÇÃO'],
            ['Data/Hora da Análise', datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Momento da geração do relatório'],
            ['', '', ''],
            ['═════ ESTATÍSTICAS GERAIS ═════', '', ''],
            ['Total de Usuários Analisados', summary.get('total_users', 0), 'Todos os usuários na rede'],
            ['Total de Conexões', summary.get('total_connections', 0), 'Conexões entre usuários'],
            ['', '', ''],
            ['═════ DETECÇÃO DE RISCOS ═════', '', ''],
            ['Usuários Suspeitos Detectados', suspicious_count, 'Usuários com padrões anômalos'],
            ['Usuários de Alto Risco (>0.7)', summary.get('high_risk_users', 0), 'Requerem atenção imediata'],
            ['Taxa de Suspeição', f"{suspicion_rate:.2f}%", 'Percentual de usuários suspeitos'],
            ['', '', ''],
            ['═════ ANÁLISE DE REDES ═════', '', ''],
            ['Componentes Conectados', network.get('connected_components', 0), 'Grupos isolados na rede'],
            ['Maior Componente (usuários)', network.get('largest_component_size', 0), 'Tamanho do maior grupo conectado'],
            ['Redes Suspeitas Identificadas', len(network.get('components_analysis', [])), 'Grupos com múltiplos usuários suspeitos'],
        ]
        
        # Adiciona alertas críticos se necessário
        high_risk = summary.get('high_risk_users', 0)
        if high_risk > 0:
            summary_data.extend([
                ['', '', ''],
                ['⚠️ ═════ ALERTAS CRÍTICOS ═════', '', ''],
                ['Status de Segurança', '🚨 ATENÇÃO IMEDIATA NECESSÁRIA', f"{high_risk} usuários de alto risco identificados"],
                ['Ação Recomendada', 'INVESTIGAÇÃO URGENTE', 'Revisar os usuários de alto risco nas próximas 24h'],
            ])
        elif suspicious_count > 0:
            summary_data.extend([
                ['', '', ''],
                ['⚠️ ═════ ALERTAS ═════', '', ''],
                ['Status de Segurança', '⚠️ MONITORAMENTO NECESSÁRIO', f"{suspicious_count} usuários suspeitos detectados"],
                ['Ação Recomendada', 'INVESTIGAÇÃO REGULAR', 'Revisar os usuários suspeitos esta semana'],
            ])
        else:
            summary_data.extend([
                ['', '', ''],
                ['✅ ═════ STATUS ═════', '', ''],
                ['Status de Segurança', '✅ NORMAL', 'Nenhum usuário suspeito detectado'],
            ])
        
        # Cria DataFrame e salva
        summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
        summary_df.to_excel(writer, sheet_name='01_Resumo_Executivo', index=False)
        
        # Ajusta largura das colunas
        worksheet = writer.sheets['01_Resumo_Executivo']
        worksheet.column_dimensions['A'].width = 30
        worksheet.column_dimensions['B'].width = 20
        worksheet.column_dimensions['C'].width = 50
    
    def _create_suspicious_users_sheet(self, analysis_data: Dict, writer):
        """Cria aba detalhada de usuários suspeitos"""
        suspicious_users = analysis_data.get('suspicious_users', [])
        
        if not suspicious_users:
            # Cria planilha vazia com cabeçalhos
            empty_data = {
                'ID_Usuario': ['Nenhum usuário suspeito detectado'],
                'Idade': [''],
                'Score_Risco': [''],
                'Nivel_Risco': [''],
                'Conteudo_Infantil_Qtd': [''],
                'Conteudo_Infantil_Perc': [''],
                'Total_Conteudo': [''],
                'Total_Conexoes': [''],
                'Prioridade': [''],
                'Observacoes': ['']
            }
            empty_df = pd.DataFrame(empty_data)
            empty_df.to_excel(writer, sheet_name='02_Usuarios_Suspeitos', index=False)
            return
        
        # Prepara dados dos usuários suspeitos
        users_data = []
        for user in suspicious_users:
            score = user.get('suspicion_score', 0)
            
            # Define nível de risco
            if score >= 0.8:
                nivel_risco = 'CRÍTICO'
                prioridade = '🔴 URGENTE'
            elif score >= 0.7:
                nivel_risco = 'ALTO'
                prioridade = '🟠 ALTA'
            elif score >= 0.5:
                nivel_risco = 'MÉDIO'
                prioridade = '🟡 MÉDIA'
            else:
                nivel_risco = 'BAIXO'
                prioridade = '🟢 BAIXA'
            
            child_content_perc = user.get('child_content_ratio', 0) * 100
            
            users_data.append({
                'ID_Usuario': user.get('user_id', ''),
                'Idade': user.get('age', 0),
                'Score_Risco': round(score, 3),
                'Nivel_Risco': nivel_risco,
                'Conteudo_Infantil_Qtd': user.get('child_content_count', 0),
                'Conteudo_Infantil_Perc': f"{child_content_perc:.1f}%",
                'Total_Conteudo': user.get('total_content_count', 0),
                'Total_Conexoes': user.get('connections_count', 0),
                'Prioridade': prioridade,
                'Observacoes': f'Adulto de {user.get("age", 0)} anos com {child_content_perc:.1f}% de conteúdo infantil consumido'
            })
        
        users_df = pd.DataFrame(users_data)
        users_df.to_excel(writer, sheet_name='02_Usuarios_Suspeitos', index=False)
        
        # Ajusta largura das colunas
        worksheet = writer.sheets['02_Usuarios_Suspeitos']
        worksheet.column_dimensions['A'].width = 15
        worksheet.column_dimensions['B'].width = 8
        worksheet.column_dimensions['C'].width = 12
        worksheet.column_dimensions['D'].width = 12
        worksheet.column_dimensions['E'].width = 20
        worksheet.column_dimensions['F'].width = 20
        worksheet.column_dimensions['G'].width = 15
        worksheet.column_dimensions['H'].width = 15
        worksheet.column_dimensions['I'].width = 15
        worksheet.column_dimensions['J'].width = 60
    
    def _create_network_analysis_sheet(self, analysis_data: Dict, writer):
        """Cria aba de análise de redes"""
        network_data = analysis_data.get('network_analysis', {})
        components = network_data.get('components_analysis', [])
        
        if not components:
            # Dados básicos de rede quando não há componentes suspeitos
            basic_data = {
                'Informação': [
                    'Total de Componentes Conectados',
                    'Maior Componente (usuários)',
                    'Total de Usuários Suspeitos',
                    'Status'
                ],
                'Valor': [
                    network_data.get('connected_components', 0),
                    network_data.get('largest_component_size', 0),
                    network_data.get('total_suspicious_users', 0),
                    'Nenhuma rede suspeita identificada'
                ]
            }
            basic_df = pd.DataFrame(basic_data)
            basic_df.to_excel(writer, sheet_name='03_Analise_Redes', index=False)
            
            worksheet = writer.sheets['03_Analise_Redes']
            worksheet.column_dimensions['A'].width = 30
            worksheet.column_dimensions['B'].width = 40
            return
        
        # Dados detalhados dos componentes
        components_data = []
        for comp in components:
            suspicious_count = comp.get('suspicious_users', 0)
            
            # Define nível de preocupação
            if suspicious_count >= 5:
                nivel = '🔴 CRÍTICO'
                investigacao = 'SIM - URGENTE'
            elif suspicious_count >= 3:
                nivel = '🟠 ALTO'
                investigacao = 'SIM - PRIORITÁRIO'
            elif suspicious_count >= 2:
                nivel = '🟡 MÉDIO'
                investigacao = 'SIM'
            else:
                nivel = '🟢 BAIXO'
                investigacao = 'MONITORAR'
            
            components_data.append({
                'ID_Rede': f"Rede_{comp.get('component_id', 0) + 1}",
                'Total_Usuarios': comp.get('total_users', 0),
                'Usuarios_Suspeitos': suspicious_count,
                'Densidade': round(comp.get('density', 0), 3),
                'Clustering_Medio': round(comp.get('avg_clustering', 0), 3),
                'Diametro': comp.get('diameter', 'N/A'),
                'Nivel_Preocupacao': nivel,
                'Requer_Investigacao': investigacao,
                'IDs_Usuarios_Suspeitos': ', '.join(comp.get('suspicious_user_ids', []))
            })
        
        components_df = pd.DataFrame(components_data)
        components_df.to_excel(writer, sheet_name='03_Analise_Redes', index=False)
        
        # Ajusta largura das colunas
        worksheet = writer.sheets['03_Analise_Redes']
        worksheet.column_dimensions['A'].width = 12
        worksheet.column_dimensions['B'].width = 15
        worksheet.column_dimensions['C'].width = 18
        worksheet.column_dimensions['D'].width = 12
        worksheet.column_dimensions['E'].width = 18
        worksheet.column_dimensions['F'].width = 12
        worksheet.column_dimensions['G'].width = 20
        worksheet.column_dimensions['H'].width = 22
        worksheet.column_dimensions['I'].width = 40
    
    def _create_influencers_sheet(self, analysis_data: Dict, writer):
        """Cria aba de influenciadores suspeitos"""
        influencers = analysis_data.get('influential_suspicious', [])
        
        if not influencers:
            empty_data = {
                'ID_Usuario': ['Nenhum influenciador suspeito identificado'],
                'Idade': [''],
                'Score_Risco': [''],
                'Centralidade_Grau': [''],
                'Centralidade_Intermediacao': [''],
                'Centralidade_Proximidade': [''],
                'Influencia': [''],
                'Risco_Propagacao': [''],
                'Acao_Recomendada': ['']
            }
            empty_df = pd.DataFrame(empty_data)
            empty_df.to_excel(writer, sheet_name='04_Influenciadores', index=False)
            return
        
        influencers_data = []
        for inf in influencers:
            degree = inf.get('degree', 0)
            score = inf.get('suspicion_score', 0)
            
            # Determina nível de influência
            if degree > 0.15:
                influencia = '🔴 MUITO ALTA'
            elif degree > 0.10:
                influencia = '🟠 ALTA'
            elif degree > 0.05:
                influencia = '🟡 MÉDIA'
            else:
                influencia = '🟢 BAIXA'
            
            # Determina risco de propagação (combinação de score e influência)
            propagation_risk = score * (1 + degree * 2)
            if propagation_risk > 0.8:
                risco = '🔴 CRÍTICO'
                acao = 'MONITORAMENTO INTENSIVO + POSSÍVEL SUSPENSÃO'
            elif propagation_risk > 0.6:
                risco = '🟠 ALTO'
                acao = 'MONITORAMENTO INTENSIVO'
            elif propagation_risk > 0.4:
                risco = '🟡 MÉDIO'
                acao = 'MONITORAMENTO REGULAR'
            else:
                risco = '🟢 BAIXO'
                acao = 'MONITORAMENTO PASSIVO'
            
            influencers_data.append({
                'ID_Usuario': inf.get('user_id', ''),
                'Idade': inf.get('age', 0),
                'Score_Risco': round(score, 3),
                'Centralidade_Grau': round(degree, 3),
                'Centralidade_Intermediacao': round(inf.get('betweenness', 0), 3),
                'Centralidade_Proximidade': round(inf.get('closeness', 0), 3),
                'Influencia_Estimada': influencia,
                'Risco_Propagacao': risco,
                'Acao_Recomendada': acao
            })
        
        influencers_df = pd.DataFrame(influencers_data)
        influencers_df.to_excel(writer, sheet_name='04_Influenciadores', index=False)
        
        # Ajusta largura das colunas
        worksheet = writer.sheets['04_Influenciadores']
        worksheet.column_dimensions['A'].width = 15
        worksheet.column_dimensions['B'].width = 8
        worksheet.column_dimensions['C'].width = 12
        worksheet.column_dimensions['D'].width = 18
        worksheet.column_dimensions['E'].width = 25
        worksheet.column_dimensions['F'].width = 25
        worksheet.column_dimensions['G'].width = 20
        worksheet.column_dimensions['H'].width = 20
        worksheet.column_dimensions['I'].width = 45
    
    def _create_centrality_metrics_sheet(self, analysis_data: Dict, writer):
        """Cria aba com métricas de centralidade para todos os usuários"""
        headers = {
            'ID_Usuario': ['Esta aba contém métricas de centralidade para análise detalhada'],
            'Centralidade_Grau': [''],
            'Centralidade_Intermediacao': [''],
            'Centralidade_Proximidade': [''],
            'PageRank': [''],
            'Classificacao_Influencia': [''],
            'Observacoes': ['Métricas disponíveis quando análise avançada é executada']
        }
        
        empty_df = pd.DataFrame(headers)
        empty_df.to_excel(writer, sheet_name='05_Metricas_Centralidade', index=False)
        
        worksheet = writer.sheets['05_Metricas_Centralidade']
        worksheet.column_dimensions['A'].width = 15
        worksheet.column_dimensions['B'].width = 22
        worksheet.column_dimensions['C'].width = 28
        worksheet.column_dimensions['D'].width = 28
        worksheet.column_dimensions['E'].width = 15
        worksheet.column_dimensions['F'].width = 25
        worksheet.column_dimensions['G'].width = 50
    
    def _create_content_patterns_sheet(self, content_analysis: Dict, writer):
        """Cria aba com análise de padrões de conteúdo"""
        if not content_analysis:
            return
        
        problematic_content = content_analysis.get('problematic_content', [])
        
        if not problematic_content:
            empty_data = {
                'ID_Conteudo': ['Nenhum conteúdo problemático identificado'],
                'Nivel_Risco': [''],
                'Score_Risco': [''],
                'Total_Interacoes': [''],
                'Interacoes_Adultos': [''],
                'Proporcao_Adultos': [''],
                'Acao_Recomendada': [''],
                'Fatores_Risco': ['']
            }
            empty_df = pd.DataFrame(empty_data)
            empty_df.to_excel(writer, sheet_name='06_Conteudo_Problematico', index=False)
            return
        
        content_data = []
        for content in problematic_content:
            risk_score = content.get('risk_score', 0)
            adult_ratio = content.get('adult_ratio', 0)
            
            # Define ação recomendada
            if risk_score > 0.8 or adult_ratio > 0.8:
                acao = '🔴 REMOVER IMEDIATAMENTE'
            elif risk_score > 0.6 or adult_ratio > 0.6:
                acao = '🟠 REVISAR URGENTE'
            elif risk_score > 0.4 or adult_ratio > 0.4:
                acao = '🟡 REVISAR'
            else:
                acao = '🟢 MONITORAR'
            
            content_data.append({
                'ID_Conteudo': content.get('content_id', ''),
                'Nivel_Risco': content.get('risk_level', ''),
                'Score_Risco': round(risk_score, 3),
                'Total_Interacoes': content.get('total_interactions', 0),
                'Interacoes_Adultos': content.get('adult_interactions', 0),
                'Proporcao_Adultos': f"{adult_ratio * 100:.1f}%",
                'Acao_Recomendada': acao,
                'Fatores_Risco': '; '.join(content.get('risk_factors', []))
            })
        
        content_df = pd.DataFrame(content_data)
        content_df.to_excel(writer, sheet_name='06_Conteudo_Problematico', index=False)
        
        worksheet = writer.sheets['06_Conteudo_Problematico']
        worksheet.column_dimensions['A'].width = 20
        worksheet.column_dimensions['B'].width = 15
        worksheet.column_dimensions['C'].width = 15
        worksheet.column_dimensions['D'].width = 18
        worksheet.column_dimensions['E'].width = 20
        worksheet.column_dimensions['F'].width = 20
        worksheet.column_dimensions['G'].width = 30
        worksheet.column_dimensions['H'].width = 60
    
    def _create_recommendations_sheet(self, analysis_data: Dict, writer):
        """Cria aba com recomendações detalhadas"""
        recommendations = analysis_data.get('recommendations', [])
        
        # Estrutura de recomendações
        rec_data = []
        
        # Adiciona recomendações do sistema
        for i, rec in enumerate(recommendations, 1):
            # Determina prioridade baseada no texto
            if any(word in rec.upper() for word in ['ALERTA', 'CRÍTICO', 'URGENTE', 'IMEDIATA']):
                prioridade = '🔴 CRÍTICA'
                prazo = 'IMEDIATO (até 24h)'
            elif any(word in rec.upper() for word in ['PRIORIDADE', 'ALTA', 'IMPORTANTE']):
                prioridade = '🟠 ALTA'
                prazo = '24-48 horas'
            elif any(word in rec.upper() for word in ['MÉDIA', 'MODERADA']):
                prioridade = '🟡 MÉDIA'
                prazo = '7 dias'
            else:
                prioridade = '🟢 BAIXA'
                prazo = '30 dias'
            
            rec_data.append({
                'Numero': f'Rec. {i}',
                'Prioridade': prioridade,
                'Prazo': prazo,
                'Recomendacao': rec,
                'Responsavel': 'A definir',
                'Status': 'PENDENTE',
                'Data_Implementacao': '',
                'Observacoes': ''
            })
        
        # Adiciona recomendações padrão de segurança
        standard_recommendations = [
            {
                'Numero': f'Rec. {len(recommendations) + 1}',
                'Prioridade': '🟠 ALTA',
                'Prazo': '48 horas',
                'Recomendacao': 'Implementar sistema de alertas automáticos para novos usuários com scores de risco > 0.7',
                'Responsavel': 'Equipe Técnica',
                'Status': 'PENDENTE',
                'Data_Implementacao': '',
                'Observacoes': 'Integrar com sistema de monitoramento existente'
            },
            {
                'Numero': f'Rec. {len(recommendations) + 2}',
                'Prioridade': '🟡 MÉDIA',
                'Prazo': '7 dias',
                'Recomendacao': 'Revisar e atualizar políticas de verificação de idade no cadastro de usuários',
                'Responsavel': 'Equipe de Compliance',
                'Status': 'PENDENTE',
                'Data_Implementacao': '',
                'Observacoes': 'Considerar verificação em duas etapas'
            },
            {
                'Numero': f'Rec. {len(recommendations) + 3}',
                'Prioridade': '🟠 ALTA',
                'Prazo': '72 horas',
                'Recomendacao': 'Estabelecer protocolo formal de comunicação com autoridades para casos críticos',
                'Responsavel': 'Equipe Jurídica',
                'Status': 'PENDENTE',
                'Data_Implementacao': '',
                'Observacoes': 'Incluir contatos de Polícia Civil, MPF e Conselho Tutelar'
            },
            {
                'Numero': f'Rec. {len(recommendations) + 4}',
                'Prioridade': '🟢 BAIXA',
                'Prazo': '30 dias',
                'Recomendacao': 'Desenvolver campanhas educativas sobre segurança online para usuários',
                'Responsavel': 'Equipe de Marketing',
                'Status': 'PENDENTE',
                'Data_Implementacao': '',
                'Observacoes': 'Focar em conscientização de pais e responsáveis'
            }
        ]
        
        rec_data.extend(standard_recommendations)
        
        rec_df = pd.DataFrame(rec_data)
        rec_df.to_excel(writer, sheet_name='07_Recomendacoes', index=False)
        
        # Ajusta largura das colunas
        worksheet = writer.sheets['07_Recomendacoes']
        worksheet.column_dimensions['A'].width = 10
        worksheet.column_dimensions['B'].width = 15
        worksheet.column_dimensions['C'].width = 18
        worksheet.column_dimensions['D'].width = 60
        worksheet.column_dimensions['E'].width = 20
        worksheet.column_dimensions['F'].width = 12
        worksheet.column_dimensions['G'].width = 18
        worksheet.column_dimensions['H'].width = 40
    
    def _create_raw_data_sheet(self, analysis_data: Dict, writer):
        """Cria aba com dados brutos para investigação detalhada"""
        suspicious_users = analysis_data.get('suspicious_users', [])
        
        if not suspicious_users:
            empty_data = {
                'Timestamp': ['Nenhum dado para investigação'],
                'ID_Usuario': [''],
                'Idade': [''],
                'Score_Risco': [''],
                'Conteudo_Infantil_Qtd': [''],
                'Conteudo_Infantil_Ratio': [''],
                'Total_Conteudo': [''],
                'Total_Conexoes': [''],
                'Hash_Usuario': [''],
                'Flag_Investigacao': [''],
                'Exportado_Autoridades': [''],
                'Status_Conta': [''],
                'Ultima_Atividade': [''],
                'Observacoes_Investigador': ['']
            }
            empty_df = pd.DataFrame(empty_data)
            empty_df.to_excel(writer, sheet_name='08_Dados_Investigacao', index=False)
            return
        
        # Dados expandidos para investigação
        raw_data = []
        for user in suspicious_users:
            score = user.get('suspicion_score', 0)
            
            # Define flag de investigação
            if score > 0.8:
                flag = '🔴 REVISAR URGENTE - CRÍTICO'
            elif score > 0.7:
                flag = '🟠 REVISAR URGENTE - ALTO'
            elif score > 0.5:
                flag = '🟡 REVISAR - MÉDIO'
            else:
                flag = '🟢 REVISAR - BAIXO'
            
            raw_data.append({
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ID_Usuario': user.get('user_id', ''),
                'Idade': user.get('age', 0),
                'Score_Risco': round(score, 4),
                'Conteudo_Infantil_Qtd': user.get('child_content_count', 0),
                'Conteudo_Infantil_Ratio': round(user.get('child_content_ratio', 0), 4),
                'Total_Conteudo': user.get('total_content_count', 0),
                'Total_Conexoes': user.get('connections_count', 0),
                'Hash_Usuario': f"hash_{abs(hash(user.get('user_id', '')))}",
                'Flag_Investigacao': flag,
                'Exportado_Autoridades': 'NÃO',
                'Status_Conta': 'ATIVA',
                'Ultima_Atividade': 'N/A',
                'Observacoes_Investigador': ''
            })
        
        raw_df = pd.DataFrame(raw_data)
        raw_df.to_excel(writer, sheet_name='08_Dados_Investigacao', index=False)
        
        # Ajusta largura das colunas
        worksheet = writer.sheets['08_Dados_Investigacao']
        worksheet.column_dimensions['A'].width = 20
        worksheet.column_dimensions['B'].width = 15
        worksheet.column_dimensions['C'].width = 8
        worksheet.column_dimensions['D'].width = 12
        worksheet.column_dimensions['E'].width = 22
        worksheet.column_dimensions['F'].width = 22
        worksheet.column_dimensions['G'].width = 15
        worksheet.column_dimensions['H'].width = 15
        worksheet.column_dimensions['I'].width = 20
        worksheet.column_dimensions['J'].width = 30
        worksheet.column_dimensions['K'].width = 20
        worksheet.column_dimensions['L'].width = 15
        worksheet.column_dimensions['M'].width = 18
        worksheet.column_dimensions['N'].width = 50
    
    def generate_summary_csv(self, analysis_data: Dict, filename: str = None) -> str:
        """Gera CSV simples com resumo dos usuários suspeitos"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"usuarios_suspeitos_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        suspicious_users = analysis_data.get('suspicious_users', [])
        
        if not suspicious_users:
            empty_data = {
                'mensagem': ['Nenhum usuário suspeito detectado na análise'],
                'data_analise': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }
            empty_df = pd.DataFrame(empty_data)
            empty_df.to_csv(filepath, index=False, encoding='utf-8')
            print(f"✅ CSV gerado (sem dados suspeitos): {filepath}")
            return filepath
        
        csv_data = []
        for user in suspicious_users:
            nivel_risco = 'CRITICO' if user.get('suspicion_score', 0) >= 0.8 else \
                         'ALTO' if user.get('suspicion_score', 0) >= 0.7 else \
                         'MEDIO' if user.get('suspicion_score', 0) >= 0.5 else 'BAIXO'
            
            csv_data.append({
                'id_usuario': user.get('user_id', ''),
                'idade': user.get('age', 0),
                'score_risco': round(user.get('suspicion_score', 0), 3),
                'nivel_risco': nivel_risco,
                'conteudo_infantil_qtd': user.get('child_content_count', 0),
                'conteudo_infantil_perc': round(user.get('child_content_ratio', 0) * 100, 1),
                'total_conteudo': user.get('total_content_count', 0),
                'conexoes': user.get('connections_count', 0),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        csv_df = pd.DataFrame(csv_data)
        csv_df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"✅ CSV resumido gerado com sucesso: {filepath}")
        return filepath
    
    def generate_network_connections_csv(self, analysis_data: Dict, filename: str = None) -> str:
        """Gera CSV com as conexões entre usuários suspeitos"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conexoes_suspeitas_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        network_analysis = analysis_data.get('network_analysis', {})
        components = network_analysis.get('components_analysis', [])
        
        if not components:
            empty_data = {
                'mensagem': ['Nenhuma rede suspeita identificada'],
                'data_analise': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }
            empty_df = pd.DataFrame(empty_data)
            empty_df.to_csv(filepath, index=False, encoding='utf-8')
            return filepath
        
        connections_data = []
        for comp in components:
            component_id = comp.get('component_id', 0)
            suspicious_ids = comp.get('suspicious_user_ids', [])
            
            for user_id in suspicious_ids:
                connections_data.append({
                    'rede_id': f"Rede_{component_id + 1}",
                    'usuario_id': user_id,
                    'total_usuarios_rede': comp.get('total_users', 0),
                    'usuarios_suspeitos_rede': comp.get('suspicious_users', 0),
                    'densidade_rede': round(comp.get('density', 0), 3),
                    'clustering': round(comp.get('avg_clustering', 0), 3),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        connections_df = pd.DataFrame(connections_data)
        connections_df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"✅ CSV de conexões gerado com sucesso: {filepath}")
        return filepath
    
    def generate_combined_report(self, analysis_data: Dict, content_analysis: Dict = None) -> Dict[str, str]:
        """Gera todos os tipos de relatórios de uma vez"""
        print("\n" + "="*60)
        print("📊 GERANDO RELATÓRIOS COMPLETOS")
        print("="*60)
        
        files_generated = {}
        
        print("\n1️⃣ Gerando relatório Excel completo...")
        excel_file = self.generate_comprehensive_excel_report(analysis_data, content_analysis)
        files_generated['excel_completo'] = excel_file
        
        print("\n2️⃣ Gerando CSV resumido de usuários suspeitos...")
        csv_users = self.generate_summary_csv(analysis_data)
        files_generated['csv_usuarios'] = csv_users
        
        print("\n3️⃣ Gerando CSV de conexões suspeitas...")
        csv_connections = self.generate_network_connections_csv(analysis_data)
        files_generated['csv_conexoes'] = csv_connections
        
        print("\n4️⃣ Gerando estatísticas de exportação...")
        stats_file = self._generate_export_statistics(analysis_data)
        files_generated['estatisticas'] = stats_file
        
        print("\n" + "="*60)
        print("✅ TODOS OS RELATÓRIOS GERADOS COM SUCESSO!")
        print("="*60)
        print(f"\n📁 Arquivos gerados em: {self.output_dir}/")
        for key, filepath in files_generated.items():
            print(f"  • {key}: {os.path.basename(filepath)}")
        
        return files_generated
    
    def _generate_export_statistics(self, analysis_data: Dict) -> str:
        """Gera arquivo de texto com estatísticas da exportação"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"estatisticas_exportacao_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        summary = analysis_data.get('summary', {})
        network = analysis_data.get('network_analysis', {})
        suspicious = analysis_data.get('suspicious_users', [])
        recommendations = analysis_data.get('recommendations', [])
        
        high_risk = [u for u in suspicious if u.get('suspicion_score', 0) >= 0.7]
        critical_risk = [u for u in suspicious if u.get('suspicion_score', 0) >= 0.8]
        
        stats_content = f"""
════════════════════════════════════════════════════════════
    ESTATÍSTICAS DE EXPORTAÇÃO - ANÁLISE DE REDE SOCIAL
════════════════════════════════════════════════════════════

📅 Data/Hora: {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}
📊 Tipo de Análise: Detecção de Padrões Suspeitos

════════════════════════════════════════════════════════════
                    ESTATÍSTICAS GERAIS
════════════════════════════════════════════════════════════

Total de Usuários Analisados:        {summary.get('total_users', 0):>6}
Total de Conexões na Rede:           {summary.get('total_connections', 0):>6}

════════════════════════════════════════════════════════════
                    DETECÇÃO DE RISCOS
════════════════════════════════════════════════════════════

Usuários Suspeitos Total:            {len(suspicious):>6}
  • Risco Crítico (≥0.8):            {len(critical_risk):>6}
  • Risco Alto (≥0.7):                {len(high_risk):>6}

Taxa de Detecção:                    {(len(suspicious)/max(1,summary.get('total_users',1))*100):>5.2f}%

════════════════════════════════════════════════════════════
                    ANÁLISE DE REDES
════════════════════════════════════════════════════════════

Componentes Conectados:              {network.get('connected_components', 0):>6}
Maior Componente (usuários):         {network.get('largest_component_size', 0):>6}
Redes Suspeitas Identificadas:       {len(network.get('components_analysis', [])):>6}

════════════════════════════════════════════════════════════
                    RECOMENDAÇÕES
════════════════════════════════════════════════════════════

Total de Recomendações:              {len(recommendations):>6}

Principais Ações:
"""
        
        for i, rec in enumerate(recommendations[:5], 1):
            stats_content += f"{i}. {rec}\n"
        
        stats_content += """
════════════════════════════════════════════════════════════
                    ARQUIVOS GERADOS
════════════════════════════════════════════════════════════

✓ Relatório Excel completo (8 abas)
✓ CSV resumido de usuários suspeitos
✓ CSV de conexões suspeitas
✓ Este arquivo de estatísticas

════════════════════════════════════════════════════════════
                    PRÓXIMOS PASSOS
════════════════════════════════════════════════════════════

1. Revisar usuários de risco crítico nas próximas 24h
2. Investigar redes suspeitas identificadas
3. Implementar recomendações de segurança
4. Notificar autoridades competentes se necessário
5. Manter monitoramento contínuo

════════════════════════════════════════════════════════════
⚠️  AVISO DE CONFIDENCIALIDADE
════════════════════════════════════════════════════════════

Este relatório contém informações sensíveis e deve ser
tratado com máxima confidencialidade. Acesso restrito a
pessoal autorizado. Armazenar em local seguro.

════════════════════════════════════════════════════════════
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(stats_content)
        
        return filepath


if __name__ == "__main__":
    # Teste com dados de exemplo
    exemplo_dados = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_users': 50,
            'total_connections': 80,
            'suspicious_users_count': 10,
            'high_risk_users': 3
        },
        'suspicious_users': [
            {
                'user_id': 'user_001',
                'age': 45,
                'suspicion_score': 0.85,
                'child_content_count': 25,
                'child_content_ratio': 0.75,
                'total_content_count': 33,
                'connections_count': 12
            }
        ],
        'network_analysis': {
            'connected_components': 2,
            'largest_component_size': 25,
            'total_suspicious_users': 10,
            'components_analysis': []
        },
        'influential_suspicious': [],
        'recommendations': [
            'ALERTA: 3 usuários de alto risco detectados.'
        ]
    }
    
    print("🧪 Testando geração de relatórios...\n")
    generator = ReportGenerator()
    arquivos = generator.generate_combined_report(exemplo_dados)
    print("\n✅ Teste concluído!")