const API_BASE = "http://localhost:5000";

export const getAuthHeaders = () => {
    const token = localStorage.getItem("session_token");
    return {
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
    };
};

export const fetchGames = async () => {
    const res = await fetch(`${API_BASE}/api/games`, {
        headers: getAuthHeaders()
    });
    return res.json();
};

export const submitPrediction = async (gameId, prediction) => {
    const res = await fetch(`${API_BASE}/api/predict`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ game_id: gameId, prediction })
    });
    return res.json();
};