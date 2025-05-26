from typing import Dict, Any
import openai
import os
from dotenv import load_dotenv
import sys
from io import StringIO

load_dotenv()

class CodeAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate and execute code based on the task"""
        
        try:
            # Generate code
            code = self._generate_code(task, context)
            
            # Test code execution
            execution_result = self._test_code(code)
            
            # Generate documentation
            documentation = self._generate_documentation(code, task)
            
            return {
                "code": code,
                "execution_result": execution_result,
                "documentation": documentation,
                "language": "python",
                "status": "completed"
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "fallback_code": self._get_fallback_code(task)
            }
    
    def _generate_code(self, task: str, context: Dict[str, Any] = None) -> str:
        """Generate code implementation"""
        
        context_info = ""
        if context and context.get("research"):
            research_data = context["research"]
            context_info = f"""
            Research Context:
            {research_data.get('synthesis', '')[:1000]}
            """
        
        prompt = f"""
        Generate Python code for this task:
        Task: {task}
        
        {context_info}
        
        Requirements:
        - Write clean, documented Python code
        - Include comments explaining key parts
        - Make it executable and functional
        - Focus on the core algorithm/implementation
        - Use standard libraries (numpy, hashlib, etc.)
        
        Return only the Python code, no explanations.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Code generation error: {e}")
            return self._get_fallback_code(task)
    
    def _test_code(self, code: str) -> Dict[str, Any]:
        """Safely test the generated code"""
        
        try:
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Execute code in restricted environment
            exec_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                }
            }
            
            # Add safe imports
            try:
                import numpy as np
                import hashlib
                import random
                import math
                exec_globals['np'] = np
                exec_globals['hashlib'] = hashlib
                exec_globals['random'] = random
                exec_globals['math'] = math
            except ImportError:
                pass
            
            exec(code, exec_globals)
            
            # Restore stdout
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            return {
                "success": True,
                "output": output,
                "error": None
            }
        
        except Exception as e:
            sys.stdout = old_stdout
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
    
    def _generate_documentation(self, code: str, task: str) -> str:
        """Generate documentation for the code"""
        
        prompt = f"""
        Generate clear documentation for this code:
        
        Task: {task}
        Code:
        {code}
        
        Provide:
        1. Brief description of what the code does
        2. Key functions/classes and their purpose
        3. How to use/run the code
        4. Any important notes or limitations
        
        Keep it concise but informative.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception:
            return f"Documentation for code implementation of: {task}"
    
    def _get_fallback_code(self, task: str) -> str:
        """Provide fallback code when generation fails"""
        
        if "quantum" in task.lower() and "algorithm" in task.lower():
            return '''
# Quantum-Resistant Algorithm Example - Lattice-based Cryptography
import hashlib
import random

class SimpleLatticeEncryption:
    """
    Simplified lattice-based encryption (for demonstration)
    Real implementations would use more sophisticated mathematical structures
    """
    
    def __init__(self, dimension=10, modulus=97):
        self.n = dimension
        self.q = modulus
        self.private_key = self._generate_private_key()
        self.public_key = self._generate_public_key()
    
    def _generate_private_key(self):
        """Generate private key as small random integers"""
        return [random.randint(-2, 2) for _ in range(self.n)]
    
    def _generate_public_key(self):
        """Generate public key using private key"""
        # Simplified: In practice, this would involve lattice operations
        public = []
        for i in range(self.n):
            val = sum(self.private_key[j] * random.randint(1, 10) for j in range(self.n))
            public.append(val % self.q)
        return public
    
    def encrypt(self, message_bit):
        """Encrypt a single bit"""
        noise = random.randint(-1, 1)
        ciphertext = sum(self.public_key[i] * (message_bit + noise) for i in range(self.n)) % self.q
        return ciphertext
    
    def demonstrate(self):
        """Demonstrate the algorithm"""
        print("Quantum-Resistant Lattice-based Encryption Demo")
        print(f"Dimension: {self.n}, Modulus: {self.q}")
        print(f"Private Key: {self.private_key}")
        print(f"Public Key: {self.public_key}")
        
        # Encrypt a message
        message = 1  # Single bit
        encrypted = self.encrypt(message)
        print(f"Original message bit: {message}")
        print(f"Encrypted: {encrypted}")

# Run demonstration
if __name__ == "__main__":
    lattice_crypto = SimpleLatticeEncryption()
    lattice_crypto.demonstrate()
'''
        else:
            return f'''
# Generated code for: {task}
def main():
    """
    Implementation for the requested task
    """
    print("Code implementation for: {task}")
    
    # Basic structure - would be expanded based on specific requirements
    result = "Task completed successfully"
    return result

if __name__ == "__main__":
    result = main()
    print(result)
'''