"""
Speech-to-Text Module using OpenAI Whisper
base 모델 사용 - 한국어 정확도 최적화

Supports Korean and English with good accuracy
"""
from pathlib import Path
from typing import Optional
import os


class WhisperSTT:
    """
    Whisper STT wrapper (base model)
    
    base 모델 사용:
    - 크기: 74MB
    - 로딩: ~10-15초 (첫 실행)
    - 한국어 정확도: ~85%
    - 메모리: ~200-300MB
    - Streamlit Cloud에서 작동 가능
    """
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_name: Whisper model size
                - tiny: 39MB, 60-70% accuracy (빠르지만 부정확)
                - base: 74MB, 80-85% accuracy (권장)
                - small: 244MB, 90%+ accuracy (메모리 부족 위험)
        """
        try:
            import whisper
            self.model = whisper.load_model(model_name)
            self.model_name = model_name
        except ImportError:
            raise ImportError(
                "Whisper not installed. Run: pip install openai-whisper"
            )
        except Exception as e:
            raise Exception(f"Failed to load Whisper model: {str(e)}")
    
    def transcribe(
        self, 
        audio_path: str,
        language: Optional[str] = None
    ) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file (.wav, .mp3, .m4a, etc)
            language: Language code (e.g., 'ko', 'en'). 
                     If None, auto-detected
        
        Returns:
            Transcribed text as plain string
        
        Raises:
            FileNotFoundError: If audio file doesn't exist
            Exception: If transcription fails
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Transcribe with optional language hint
        transcribe_options = {
            "fp16": False  # CPU compatibility
        }
        if language:
            transcribe_options['language'] = language
        
        try:
            result = self.model.transcribe(
                str(audio_path),
                **transcribe_options
            )
            
            # Return plain text only
            return result["text"].strip()
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_with_info(
        self,
        audio_path: str,
        language: Optional[str] = None
    ) -> dict:
        """
        Transcribe with additional metadata
        
        Returns:
            {
                'text': str,
                'language': str,  # detected or specified
                'segments': list  # optional segment info
            }
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        transcribe_options = {"fp16": False}
        if language:
            transcribe_options['language'] = language
        
        try:
            result = self.model.transcribe(
                str(audio_path),
                **transcribe_options
            )
            
            return {
                'text': result['text'].strip(),
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', [])
            }
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")


# Quick test function
def test_stt(audio_file: str):
    """
    Test STT functionality
    
    Usage:
        python -c "from thinking_box.stt.whisper_stt import test_stt; test_stt('audio.wav')"
    """
    print(f"Testing STT on: {audio_file}")
    print(f"Model: base (74MB, ~85% accuracy for Korean)")
    
    stt = WhisperSTT(model_name="base")
    text = stt.transcribe(audio_file)
    
    print(f"\nTranscribed text:\n{text}")
    return text
