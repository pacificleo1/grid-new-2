
from fastapi.middleware.cors import CORSMiddleware

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games = {}

@app.post("/start-game/")
def start_game(player_name: str, rows: int, cols: int):
    if not (3 <= rows <= 10 and 3 <= cols <= 10):
        return {"error": "Rows and Columns must be between 3 and 10"}
    
    game_id = player_name  
    games[game_id] = {
        "player_name": player_name,
        "rows": rows,
        "cols": cols,
        "grid": [["" for _ in range(cols)] for _ in range(rows)],
        "turn": "player",
        "moves": 0
    }
    
    return {"message": f"Game started for {player_name}", "game_id": game_id, "rows": rows, "cols": cols}


@app.post("/player-move/")
def player_move(game_id: str, row: int, col: int):
    game = games.get(game_id)
    
    if not game:
        return {"error": "Game not found"}
    
    if game["grid"][row][col] != "":
        return {"error": "Cell already occupied"}
    
    game["grid"][row][col] = "O"
    game["moves"] += 1

    if check_winner(game["grid"], "O"):
        return {"winner": game["player_name"], "moves": game["moves"], "grid": game["grid"]}

    ai_row, ai_col = get_best_move(game["grid"])
    if ai_row is not None and ai_col is not None:
        game["grid"][ai_row][ai_col] = "*"
        game["moves"] += 1
        
        if check_winner(game["grid"], "*"):
            return {"winner": "Computer", "moves": game["moves"], "grid": game["grid"]}
    
    return {"grid": game["grid"], "moves": game["moves"]}

def get_best_move(grid):
    empty_cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == ""]
    return random.choice(empty_cells) if empty_cells else (None, None)

def check_winner(grid, symbol):
    rows, cols = len(grid), len(grid[0])
    
    for row in grid:
        if all(cell == symbol for cell in row):
            return True

    for col in range(cols):
        if all(grid[row][col] == symbol for row in range(rows)):
            return True

    if all(grid[i][i] == symbol for i in range(min(rows, cols))):
        return True

    if all(grid[i][cols - i - 1] == symbol for i in range(min(rows, cols))):
        return True

    return False
