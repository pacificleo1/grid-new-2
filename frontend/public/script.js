console.log("JavaScript is working!");
const API_URL = "https://grid-new-2-backend-3.onrender.com";  // Insert this at the top
const BACKEND_URL = "https://grid-new-2-backend-3.onrender.com";


document.getElementById("startGame").addEventListener("click", () => {
    const playerName = document.getElementById("playerName").value;
    
    fetch(`https://grid-new-2-backend-3.onrender.com/start-game/`, {  // Replace hardcoded URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_name: playerName, rows: 3, cols: 3 })
    })
    .then(response => response.json())
    .then(data => {
        generateGrid(3, 3, data.game_id);
    });
});

function generateGrid(rows, cols, gameId) {
    const grid = document.getElementById("grid");
    grid.innerHTML = "";
    grid.style.gridTemplateColumns = `repeat(${cols}, 50px)`;

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            let cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener("click", () => makeMove(r, c, gameId));
            grid.appendChild(cell);
        }
    }
}

function makeMove(row, col, gameId) {
    fetch(`https://grid-new-2-backend-3.onrender.com/player-move/`, {  // Replace hardcoded URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, row: row, col: col })
    })
    .then(response => response.json())
    .then(data => {
        if (data.winner) {
            document.getElementById("status").innerText = `${data.winner} won in ${data.moves} moves!`;
        } else {
            updateGrid(data.grid);
        }
    });
}

function updateGrid(gridData) {
    const cells = document.querySelectorAll(".cell");
    let i = 0;
    for (let row of gridData) {
        for (let col of row) {
            cells[i].textContent = col;
            i++;
        }
    }
}
