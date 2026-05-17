from app.database.connection import _load_db, _save_db

def init_settings():
    data = _load_db()
    data["settings"] = {
        "clock_emotions": {
            "1": "#6366f1", "2": "#818cf8", "3": "#a78bfa", "4": "#f472b6", "5": "#fb923c",
            "6": "#34d399", "7": "#fbbf24", "8": "#60a5fa", "9": "#a78bfa", "10": "#f9a8d4"
        },
        "puzzle_emotions": {
            "Happy": "#22c55e", "Sad": "#3b82f6", "Mad": "#ef4444", "Scared": "#334155", "Worried": "#eab308", "Excited": "#ec4899"
        }
    }
    _save_db(data)
    print("Reset settings in db.")

init_settings()
