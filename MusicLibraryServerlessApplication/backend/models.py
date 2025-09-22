from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    user_id: str
    email: str
    username: str
    created_at: datetime

class Song(BaseModel):
    song_id: str
    title: str
    artist: str
    album: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    duration: Optional[int] = None  # in seconds
    cover_art_url: Optional[str] = None
    
    @property
    def formatted_duration(self) -> str:
        """Get duration formatted as MM:SS"""
        return format_duration(self.duration)

class UserSong(BaseModel):
    user_id: str
    song_id: str
    added_at: datetime
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    play_count: int = 0
    last_played: Optional[datetime] = None

class Playlist(BaseModel):
    playlist_id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    is_public: bool = False

class PlaylistSong(BaseModel):
    playlist_id: str
    song_id: str
    position: int
    added_at: datetime

# Request/Response Models
class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class CreateSongRequest(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    cover_art_url: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None

class UpdateSongRequest(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    cover_art_url: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None

class CreatePlaylistRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class UpdatePlaylistRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class AddSongToPlaylistRequest(BaseModel):
    song_id: str
    position: Optional[int] = None


# Utility functions
def format_duration(seconds: Optional[int]) -> str:
    """
    Format duration from seconds to MM:SS format.
    
    Args:
        seconds: Duration in seconds, or None
        
    Returns:
        Formatted duration string (e.g., "3:45") or "0:00" if None
        
    Examples:
        >>> format_duration(225)
        "3:45"
        >>> format_duration(61)
        "1:01"
        >>> format_duration(None)
        "0:00"
    
    Usage with Song model:
        song = Song(song_id="1", title="Test", artist="Artist", duration=225)
        print(song.formatted_duration)  # Outputs: "3:45"
    """
    if seconds is None or seconds < 0:
        return "0:00"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    return f"{minutes}:{remaining_seconds:02d}"