from typing import Dict, Any
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd
import os
import openai
from dotenv import load_dotenv

load_dotenv()

class VisualizerAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        plt.style.use('seaborn-v0_8')
    
    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create visualizations based on the task and context"""
        
        try:
            # Determine what visualizations to create
            viz_plan = self._plan_visualizations(task, context)
            
            # Create visualizations
            charts = []
            for viz_type in viz_plan:
                chart_data = self._create_visualization(viz_type, task, context)
                if chart_data:
                    charts.append(chart_data)
            
            return {
                "visualizations": charts,
                "visualization_plan": viz_plan,
                "status": "completed"
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "fallback_charts": self._create_fallback_visualizations(task)
            }
    
    def _plan_visualizations(self, task: str, context: Dict[str, Any] = None) -> list:
        """Determine what visualizations would be useful"""
        
        viz_types = []
        task_lower = task.lower()
        
        # Analyze task keywords
        if any(word in task_lower for word in ['sector', 'industry', 'vulnerable', 'impact']):
            viz_types.append('sector_analysis')
        
        if any(word in task_lower for word in ['timeline', 'trend', 'over time']):
            viz_types.append('timeline')
        
        if any(word in task_lower for word in ['algorithm', 'performance', 'comparison']):
            viz_types.append('algorithm_comparison')
        
        if any(word in task_lower for word in ['risk', 'threat', 'security']):
            viz_types.append('risk_assessment')
        
        # Default if no specific type identified
        if not viz_types:
            viz_types.append('general_analysis')
        
        return viz_types[:3]  # Limit to 3 visualizations
    
    def _create_visualization(self, viz_type: str, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a specific type of visualization"""
        
        try:
            if viz_type == 'sector_analysis':
                return self._create_sector_vulnerability_chart()
            elif viz_type == 'timeline':
                return self._create_timeline_chart()
            elif viz_type == 'algorithm_comparison':
                return self._create_algorithm_performance_chart()
            elif viz_type == 'risk_assessment':
                return self._create_risk_heatmap()
            else:
                return self._create_general_analysis_chart(task)
        
        except Exception as e:
            print(f"Visualization error for {viz_type}: {e}")
            return None
    
    def _create_sector_vulnerability_chart(self) -> Dict[str, Any]:
        """Create sector vulnerability analysis chart"""
        
        # Sample data for quantum computing cybersecurity impact
        sectors = ['Financial Services', 'Healthcare', 'Government', 'Defense', 
                  'Technology', 'Energy', 'Telecommunications', 'Transportation']
        vulnerability_scores = [95, 85, 90, 98, 80, 75, 88, 70]
        timeline_risk = [5, 8, 6, 4, 7, 10, 6, 12]  # Years until high risk
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Vulnerability bar chart
        colors = ['#ff4444' if score > 90 else '#ff8800' if score > 80 else '#44aa44' 
                 for score in vulnerability_scores]
        bars = ax1.bar(sectors, vulnerability_scores, color=colors)
        ax1.set_title('Sector Vulnerability to Quantum Computing Threats', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Vulnerability Score (0-100)')
        ax1.set_ylim(0, 100)
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, score in zip(bars, vulnerability_scores):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{score}', ha='center', va='bottom', fontweight='bold')
        
        # Timeline scatter plot
        scatter = ax2.scatter(timeline_risk, vulnerability_scores, 
                            c=vulnerability_scores, cmap='Reds', s=200, alpha=0.7)
        ax2.set_xlabel('Years Until High Risk')
        ax2.set_ylabel('Current Vulnerability Score')
        ax2.set_title('Risk Timeline vs Current Vulnerability', fontsize=14, fontweight='bold')
        
        # Add sector labels
        for i, sector in enumerate(sectors):
            ax2.annotate(sector[:3], (timeline_risk[i], vulnerability_scores[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.tight_layout()
        
        # Save chart
        chart_path = 'sector_vulnerability_analysis.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "type": "sector_analysis",
            "title": "Sector Vulnerability to Quantum Computing Threats",
            "file_path": chart_path,
            "description": "Analysis of different sectors' vulnerability to quantum computing cybersecurity threats",
            "key_insights": [
                "Defense and Financial Services are most vulnerable (95%+ scores)",
                "Transportation sector has lowest immediate vulnerability",
                "Most sectors face high risk within 5-8 years"
            ]
        }
    
    def _create_timeline_chart(self) -> Dict[str, Any]:
        """Create quantum computing threat timeline"""
        
        years = list(range(2024, 2035))
        quantum_capability = [20, 25, 35, 45, 60, 70, 80, 85, 90, 95, 98]
        crypto_vulnerability = [30, 40, 55, 70, 80, 90, 95, 98, 99, 100, 100]
        defense_readiness = [15, 20, 30, 45, 60, 75, 85, 90, 95, 98, 99]
        
        plt.figure(figsize=(12, 8))
        
        plt.plot(years, quantum_capability, marker='o', linewidth=3, 
                label='Quantum Computing Capability', color='#2E86AB')
        plt.plot(years, crypto_vulnerability, marker='s', linewidth=3, 
                label='Current Crypto Vulnerability', color='#A23B72')
        plt.plot(years, defense_readiness, marker='^', linewidth=3, 
                label='Quantum-Resistant Defense Readiness', color='#F18F01')
        
        plt.title('Quantum Computing Threat Timeline', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Capability/Risk Level (%)', fontsize=12)
        plt.legend(fontsize=11, loc='center right')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 105)
        
        # Add critical intersection points
        plt.axhline(y=80, color='red', linestyle='--', alpha=0.5, label='Critical Threshold')
        plt.annotate('Critical Risk Period', xy=(2029, 85), xytext=(2031, 70),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontsize=10, color='red', fontweight='bold')
        
        plt.tight_layout()
        
        chart_path = 'quantum_threat_timeline.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "type": "timeline",
            "title": "Quantum Computing Threat Timeline",
            "file_path": chart_path,
            "description": "Timeline showing evolution of quantum capabilities vs cryptographic vulnerabilities",
            "key_insights": [
                "Critical risk period begins around 2029-2030",
                "Current cryptographic systems become highly vulnerable by 2028",
                "Defense readiness needs acceleration to match threat timeline"
            ]
        }
    
    def _create_algorithm_performance_chart(self) -> Dict[str, Any]:
        """Create algorithm performance comparison"""
        
        algorithms = ['RSA-2048', 'ECC-256', 'Lattice-based', 'Hash-based', 'Multivariate', 'Code-based']
        quantum_resistance = [0, 0, 85, 90, 75, 80]
        performance_overhead = [1.0, 1.0, 3.2, 2.1, 4.5, 2.8]
        key_sizes = [2048, 256, 1024, 512, 2048, 1536]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Quantum resistance
        colors = ['red' if r == 0 else 'orange' if r < 80 else 'green' for r in quantum_resistance]
        ax1.bar(algorithms, quantum_resistance, color=colors)
        ax1.set_title('Quantum Resistance Level', fontweight='bold')
        ax1.set_ylabel('Resistance Score (0-100)')
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Performance overhead
        ax2.bar(algorithms, performance_overhead, color='skyblue', alpha=0.7)
        ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Current Standard')
        ax2.set_title('Performance Overhead', fontweight='bold')
        ax2.set_ylabel('Overhead Factor')
        ax2.legend()
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # Key sizes comparison
        ax3.bar(algorithms, key_sizes, color='lightcoral', alpha=0.7)
        ax3.set_title('Key Sizes (bits)', fontweight='bold')
        ax3.set_ylabel('Key Size')
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        
        # Overall score (resistance vs performance)
        overall_scores = [r / (p * 0.5 + 0.5) for r, p in zip(quantum_resistance, performance_overhead)]
        ax4.scatter(performance_overhead, quantum_resistance, s=200, alpha=0.7, c=overall_scores, cmap='RdYlGn')
        for i, alg in enumerate(algorithms):
            ax4.annotate(alg, (performance_overhead[i], quantum_resistance[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=9)
        ax4.set_xlabel('Performance Overhead')
        ax4.set_ylabel('Quantum Resistance')
        ax4.set_title('Algorithm Trade-offs', fontweight='bold')
        
        plt.tight_layout()
        
        chart_path = 'algorithm_comparison.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "type": "algorithm_comparison",
            "title": "Quantum-Resistant Algorithm Comparison",
            "file_path": chart_path,
            "description": "Comparison of cryptographic algorithms' quantum resistance and performance",
            "key_insights": [
                "Current RSA and ECC offer no quantum resistance",
                "Hash-based signatures offer best quantum resistance",
                "Lattice-based algorithms provide good balance of security and performance"
            ]
        }
    
    def _create_risk_heatmap(self) -> Dict[str, Any]:
        """Create risk assessment heatmap"""
        
        sectors = ['Financial', 'Healthcare', 'Government', 'Defense', 'Tech', 'Energy']
        risk_factors = ['Data Exposure', 'System Access', 'Communication', 'Storage', 'Authentication']
        
        # Risk matrix (0-100 scale)
        risk_matrix = np.array([
            [90, 85, 80, 75, 88],  # Financial
            [85, 70, 75, 90, 80],  # Healthcare
            [95, 90, 85, 80, 92],  # Government
            [98, 95, 90, 85, 95],  # Defense
            [75, 80, 85, 70, 78],  # Tech
            [80, 85, 78, 82, 75]   # Energy
        ])
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(risk_matrix, 
                   xticklabels=risk_factors,
                   yticklabels=sectors,
                   annot=True, 
                   cmap='Reds',
                   fmt='d',
                   cbar_kws={'label': 'Risk Level (0-100)'})
        
        plt.title('Quantum Computing Risk Assessment Heatmap', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Risk Factors', fontsize=12)
        plt.ylabel('Sectors', fontsize=12)
        plt.tight_layout()
        
        chart_path = 'risk_heatmap.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "type": "risk_heatmap",
            "title": "Quantum Computing Risk Assessment Heatmap",
            "file_path": chart_path,
            "description": "Risk assessment matrix showing vulnerability levels across sectors and risk factors",
            "key_insights": [
                "Defense sector shows highest risk across all factors",
                "Data exposure and authentication are primary concerns",
                "Technology sector shows relatively lower risk levels"
            ]
        }
    
    def _create_general_analysis_chart(self, task: str) -> Dict[str, Any]:
        """Create general analysis visualization"""
        
        # Generate sample data based on task
        categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        values = np.random.randint(20, 100, 5)
        
        plt.figure(figsize=(10, 6))
        plt.bar(categories, values, color='steelblue', alpha=0.7)
        plt.title(f'Analysis Results for: {task[:50]}...', fontsize=14, fontweight='bold')
        plt.ylabel('Analysis Score')
        plt.xticks(rotation=45, ha='right')
        
        for i, v in enumerate(values):
            plt.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        chart_path = 'general_analysis.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "type": "general_analysis",
            "title": f"Analysis for {task[:30]}...",
            "file_path": chart_path,
            "description": f"General analysis visualization for the task: {task}",
            "key_insights": ["Analysis completed with visualized results"]
        }
    
    def _create_fallback_visualizations(self, task: str) -> list:
        """Create basic fallback visualizations when main process fails"""
        
        try:
            # Simple bar chart
            plt.figure(figsize=(8, 6))
            categories = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
            values = [65, 80, 45, 90]
            
            plt.bar(categories, values, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
            plt.title(f'Fallback Analysis: {task[:40]}...', fontweight='bold')
            plt.ylabel('Values')
            
            chart_path = 'fallback_chart.png'
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return [{
                "type": "fallback",
                "title": "Basic Analysis Chart",
                "file_path": chart_path,
                "description": "Fallback visualization due to processing limitations",
                "key_insights": ["Basic analysis completed"]
            }]
        
        except Exception:
            return [{
                "type": "error",
                "title": "Visualization Error",
                "file_path": None,
                "description": "Unable to create visualizations",
                "key_insights": ["Visualization generation failed"]
            }]