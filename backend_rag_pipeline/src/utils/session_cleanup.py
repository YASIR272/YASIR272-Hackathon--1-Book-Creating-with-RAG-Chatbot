"""
Session Cleanup Utility for RAG Chatbot API
Manages cleanup of expired sessions to free up memory
"""

import asyncio
from datetime import datetime
from typing import Dict
from ..models.session_context import SessionContext


class SessionCleanupManager:
    """
    Manager for cleaning up expired sessions
    """
    def __init__(self, sessions_dict: Dict[str, SessionContext], cleanup_interval_minutes: int = 5):
        self.sessions = sessions_dict
        self.cleanup_interval = cleanup_interval_minutes * 60  # Convert to seconds
        self.cleanup_task = None
        self.is_running = False

    async def start_cleanup_task(self):
        """
        Start the background cleanup task
        """
        if not self.is_running:
            self.is_running = True
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def stop_cleanup_task(self):
        """
        Stop the background cleanup task
        """
        if self.is_running and self.cleanup_task:
            self.is_running = False
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass  # Expected when cancelling

    async def _cleanup_loop(self):
        """
        Main loop for periodic cleanup
        """
        while self.is_running:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self.cleanup_expired_sessions()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error during session cleanup: {e}")

    async def cleanup_expired_sessions(self):
        """
        Remove all expired sessions from memory
        """
        current_time = datetime.utcnow()
        expired_sessions = []

        for session_id, session in self.sessions.items():
            if session.should_cleanup():
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.sessions[session_id]
            print(f"Cleaned up expired session: {session_id}")

        if expired_sessions:
            print(f"Cleaned up {len(expired_sessions)} expired sessions")

    def force_cleanup_session(self, session_id: str):
        """
        Force cleanup of a specific session
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"Force cleaned up session: {session_id}")


# Global cleanup manager instance
cleanup_manager = None


def init_cleanup_manager(sessions_dict: Dict[str, SessionContext]):
    """
    Initialize the cleanup manager with the sessions dictionary
    """
    global cleanup_manager
    cleanup_manager = SessionCleanupManager(sessions_dict)
    return cleanup_manager