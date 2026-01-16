"""
LLM Client using Anthropic Claude API
기존 thinking_box에서 사용하던 Claude API 클라이언트

Streamlit Cloud 배포용 - 원본 그대로 유지
"""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """
    Anthropic Claude API 클라이언트
    
    기존 thinking_box와 동일한 인터페이스
    """
    
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude client
        
        Args:
            model: Claude model name
                - claude-sonnet-4-20250514: Latest Sonnet (권장)
                - claude-sonnet-3-5-20241022: Previous Sonnet
                - claude-opus-4-20250514: Most capable
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError(
                "Anthropic not installed. Run: pip install anthropic"
            )
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables"
            )
        
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate response using Claude
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            temperature: Randomness (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated text
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    # Backward-compatible alias
    def call(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Alias for generate() to match 기존 에이전트 인터페이스
        """
        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_message,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def generate_with_history(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate with conversation history
        
        Args:
            system_prompt: System instruction
            messages: List of message dicts with 'role' and 'content'
            temperature: Randomness
            max_tokens: Maximum response length
            
        Returns:
            Generated text
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def call_with_history(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Alias for generate_with_history()
        """
        return self.generate_with_history(
            system_prompt=system_prompt,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )


# For backward compatibility
def create_client(model: str = "claude-sonnet-4-20250514"):
    """
    Create LLM client (Claude)
    기존 코드와 호환
    """
    return LLMClient(model=model)
