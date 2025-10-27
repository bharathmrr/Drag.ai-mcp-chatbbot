"""Translator MCP Tool - Translate text between languages"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TranslatorTool:
    """MCP tool for text translation"""
    
    def __init__(self):
        self.name = "translator"
        self.description = "Translate text between different languages"
        self.enabled = True
        
        # Common language codes
        self.languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "ar": "Arabic",
            "hi": "Hindi"
        }
        
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute translator operation
        
        Args:
            action: Operation type (translate, detect, languages)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with operation result
        """
        try:
            if action == "translate":
                return await self._translate(
                    kwargs.get("text"),
                    kwargs.get("from_lang", "auto"),
                    kwargs.get("to_lang", "en")
                )
            elif action == "detect":
                return await self._detect_language(kwargs.get("text"))
            elif action == "languages":
                return await self._list_languages()
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Translator error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _translate(self, text: str, from_lang: str, to_lang: str) -> Dict[str, Any]:
        """Translate text"""
        if not text:
            return {"success": False, "error": "No text provided"}
        
        try:
            # Try using googletrans (free Google Translate API)
            from googletrans import Translator
            
            translator = Translator()
            result = translator.translate(text, src=from_lang, dest=to_lang)
            
            return {
                "success": True,
                "action": "translate",
                "original_text": text,
                "translated_text": result.text,
                "from_language": result.src,
                "to_language": to_lang,
                "pronunciation": result.pronunciation if hasattr(result, 'pronunciation') else None
            }
            
        except ImportError:
            # Fallback: Mock translation
            return {
                "success": True,
                "action": "translate",
                "original_text": text,
                "translated_text": f"[Translation: {text}]",
                "from_language": from_lang,
                "to_language": to_lang,
                "note": "Install googletrans for actual translation (pip install googletrans==4.0.0-rc1)"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text"""
        if not text:
            return {"success": False, "error": "No text provided"}
        
        try:
            from googletrans import Translator
            
            translator = Translator()
            detection = translator.detect(text)
            
            return {
                "success": True,
                "action": "detect",
                "text": text,
                "language": detection.lang,
                "language_name": self.languages.get(detection.lang, "Unknown"),
                "confidence": detection.confidence
            }
            
        except ImportError:
            return {
                "success": True,
                "action": "detect",
                "text": text,
                "language": "en",
                "language_name": "English",
                "confidence": 0.5,
                "note": "Install googletrans for actual detection"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _list_languages(self) -> Dict[str, Any]:
        """List supported languages"""
        return {
            "success": True,
            "action": "languages",
            "languages": self.languages,
            "count": len(self.languages)
        }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for LangChain"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["translate", "detect", "languages"],
                        "description": "Translation operation to perform"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to translate or detect"
                    },
                    "from_lang": {
                        "type": "string",
                        "description": "Source language code (auto for auto-detect)"
                    },
                    "to_lang": {
                        "type": "string",
                        "description": "Target language code (default: en)"
                    }
                },
                "required": ["action"]
            }
        }
