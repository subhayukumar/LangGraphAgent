from typing import Dict, Any
from tavily import TavilyClient
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def execute(self, task: str) -> Dict[str, Any]:
        """Execute research for the given task"""
        
        try:
            # Extract research queries from task
            search_queries = self._extract_search_queries(task)
            
            # Perform searches
            search_results = []
            for query in search_queries[:3]:  # Limit to 3 queries
                try:
                    result = self.tavily.search(
                        query=query,
                        search_depth="advanced",
                        max_results=5
                    )
                    search_results.append({
                        "query": query,
                        "results": result.get("results", [])
                    })
                except Exception as e:
                    print(f"Search error for query '{query}': {e}")
            
            # Synthesize findings
            synthesis = self._synthesize_findings(task, search_results)
            
            return {
                "search_queries": search_queries,
                "raw_results": search_results,
                "synthesis": synthesis,
                "key_findings": self._extract_key_findings(synthesis),
                "status": "completed"
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "fallback_info": self._get_fallback_info(task)
            }
    
    def _extract_search_queries(self, task: str) -> list:
        """Extract relevant search queries from the task"""
        
        prompt = f"""
        Extract 2-3 specific search queries for this research task:
        Task: {task}
        
        Return only the search queries, one per line.
        Make them specific and research-focused.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            queries = [q.strip() for q in response.choices[0].message.content.strip().split('\n') if q.strip()]
            return queries[:3]
        
        except Exception:
            # Fallback queries based on task keywords
            if "quantum computing" in task.lower() and "cybersecurity" in task.lower():
                return [
                    "quantum computing cybersecurity threats",
                    "quantum resistant cryptography algorithms",
                    "post-quantum cryptography vulnerable sectors"
                ]
            else:
                return [task[:100]]  # Use first 100 chars as query
    
    def _synthesize_findings(self, task: str, search_results: list) -> str:
        """Synthesize research findings into a coherent summary"""
        
        # Compile all search content
        all_content = ""
        for result_set in search_results:
            for result in result_set.get("results", []):
                all_content += f"{result.get('title', '')}: {result.get('content', '')}\n"
        
        prompt = f"""
        Based on the research task and findings, provide a comprehensive synthesis:
        
        Task: {task}
        
        Research Findings:
        {all_content[:4000]}  # Limit content length
        
        Provide a well-structured synthesis covering:
        1. Key insights relevant to the task
        2. Important findings and data points
        3. Current state and trends
        4. Implications and considerations
        
        Keep it comprehensive but concise.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception:
            return "Research synthesis unavailable due to processing error."
    
    def _extract_key_findings(self, synthesis: str) -> list:
        """Extract key bullet points from synthesis"""
        
        prompt = f"""
        Extract 5-7 key findings from this research synthesis:
        
        {synthesis}
        
        Return as bullet points, each starting with a dash (-).
        Focus on the most important and actionable insights.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            
            findings = [f.strip()[1:].strip() for f in response.choices[0].message.content.split('\n') if f.strip().startswith('-')]
            return findings
        
        except Exception:
            return ["Key findings extraction unavailable"]
    
    def _get_fallback_info(self, task: str) -> Dict[str, Any]:
        """Provide fallback information when search fails"""
        
        if "quantum computing" in task.lower() and "cybersecurity" in task.lower():
            return {
                "summary": "Quantum computing poses significant threats to current cryptographic systems",
                "key_points": [
                    "RSA and ECC encryption vulnerable to quantum algorithms",
                    "Financial services and healthcare most at risk",
                    "Post-quantum cryptography standards being developed",
                    "Timeline: 10-15 years for practical quantum computers"
                ]
            }
        else:
            return {
                "summary": f"Research information for: {task}",
                "key_points": ["Detailed research unavailable due to connection issues"]
            }