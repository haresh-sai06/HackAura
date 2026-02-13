import google.generativeai as genai
from typing import List, Dict, Optional
from config import settings


class GeminiService:
    def __init__(self):
        import os
        genai.configure(api_key=settings.GEMINI_API_KEY, transport='rest')
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def get_conversation_history(self, call_sid: str) -> List[Dict]:
        """Get conversation history for a specific call"""
        if call_sid not in self.conversation_history:
            self.conversation_history[call_sid] = []
        return self.conversation_history[call_sid]
    
    def add_to_conversation(self, call_sid: str, role: str, content: str):
        """Add a message to the conversation history"""
        history = self.get_conversation_history(call_sid)
        history.append({"role": role, "content": content})
        
        # Keep conversation within max length
        if len(history) > settings.MAX_CONVERSATION_LENGTH:
            # Remove the oldest message
            history.pop(0)
    
    async def generate_response(self, call_sid: str, user_input: str) -> str:
        """Generate AI response based on user input and conversation history"""
        try:
            # Add user input to conversation
            self.add_to_conversation(call_sid, "user", user_input)
            
            # Get conversation history
            history = self.get_conversation_history(call_sid)
            
            # Build conversation context
            system_prompt = f"""You are {settings.AI_ASSISTANT_NAME}, a helpful AI assistant. 
            You are having a phone conversation with a user. Be concise, friendly, and helpful.
            Keep your responses brief and natural for speech. Avoid long paragraphs."""
            
            # Create chat history for Gemini
            chat_history = []
            for msg in history:
                if msg["role"] == "user":
                    chat_history.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    chat_history.append({"role": "model", "parts": [msg["content"]]})
            
            # Start chat with system prompt
            chat = self.model.start_chat(history=chat_history)
            
            # Generate response
            response = chat.send_message(system_prompt)
            ai_response = response.text.strip()
            
            # Add AI response to conversation
            self.add_to_conversation(call_sid, "assistant", ai_response)
            
            return ai_response
            
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return "I'm sorry, I'm having trouble understanding. Could you please repeat that?"
    
    def clear_conversation(self, call_sid: str):
        """Clear conversation history for a specific call"""
        if call_sid in self.conversation_history:
            del self.conversation_history[call_sid]


# Global instance
gemini_service = GeminiService()
