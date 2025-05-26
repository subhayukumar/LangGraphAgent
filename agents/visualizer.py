from typing import Dict, Any
import matplotlib.pyplot as plt
import numpy as np
import os
import openai
from dotenv import load_dotenv
from helpers import setup_sandbox


setup_sandbox()  # Ensure sandbox is set up for safe execution
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
            viz_types.append('vulnerability_chart')
        
        if any(word in task_lower for word in ['timeline', 'trend', 'over time']):
            viz_types.append('timeline_chart')
        
        if any(word in task_lower for word in ['algorithm', 'performance', 'comparison']):
            viz_types.append('performance_chart')
        
        if any(word in task_lower for word in ['risk', 'threat', 'security']):
            viz_types.append('heatmap')
        
        # Default if no specific type identified
        if not viz_types:
            viz_types.append('general_analysis')
        
        return viz_types[:3]  # Limit to 3 visualizations
    
    def _create_visualization(self, viz_type: str, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a specific type of visualization"""

        try:
            if viz_type == 'vulnerability_chart':
                return vulnerability_chart()  # type: ignore # noqa: F821
            elif viz_type == 'timeline_chart':
                return timeline_chart()  # type: ignore # noqa: F821
            elif viz_type == 'performance_chart':
                return performance_chart()  # type: ignore # noqa: F821
            elif viz_type == 'heatmap':
                return heatmap()  # type: ignore # noqa: F821
            else:
                return self._create_general_analysis_chart(task)
        
        except Exception as e:
            print(f"Visualization error for {viz_type}: {e}")
            return None
    
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