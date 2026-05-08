# Maze Generator & Solver

A Python + Pygame program that generates a perfect maze using a stack-based DFS algorithm and solves it using backtracking, with full animation at every step.

---


## Getting Started

### Prerequisites

- Python 3.7+
- Pygame

### Installation

```bash
# Clone the repository
git clone https://github.com/Abe-Alefew/build-and-run-maze.git
cd build-and-run-maze

# Install dependencies
pip install pygame
```

### Running the Program

```bash
python maze_assignment.py
```

You will be prompted in the terminal:

```
Enter number of rows: 15
Enter number of columns: 15
```

---

## Controls

| Key | Action |
|---|---|
| `C` | Add cycles to the perfect maze (optional) |
| Any other key | Skip cycles and proceed to solver |
| Any key (after cycles added) | Start the solver |
| Close window | Exit |

---

##  How It Works

### Maze Representation

The maze is stored in two 2D arrays:

```python
northWall[rows + 1][cols]   # True = wall intact above cell (i, j)
eastWall[rows][cols + 1]    # True = wall intact to the right of cell (i, j)
```

Only **north** and **east** walls are stored per cell because:
- The **south** wall of `(i, j)` = the **north** wall of `(i-1, j)`
- The **west** wall of `(i, j)` = the **east** wall of `(i, j-1)`

This avoids double-storing any wall. A phantom row (`northWall[0]`) forms the bottom border of the maze, and `eastWall[row][0]` controls the left border.

---

### Maze Generation — Stack-Based DFS Algorithm

The generator uses a **depth-first search with an explicit stack**, simulating an invisible mouse that eats through walls:

```
1. Place the mouse at a random starting cell, mark it visited
2. Push it onto the stack
3. Loop:
   a. Find all unvisited neighbors (N, S, E, W)
   b. If any exist:
        → Pick one randomly
        → Remove the wall between current and chosen
        → Mark chosen as visited
        → Push current onto stack
        → Move to chosen
   c. If none exist (dead end):
        → Pop from stack  ← backtrack
4. Stack empty → every cell visited → maze complete
```

This produces a **perfect maze** — a spanning tree where every cell is connected by exactly one unique path. No cycles, no isolated regions.

> **Why DFS?** Because DFS explores deep before backtracking, it produces long winding corridors — the classic maze aesthetic. A BFS (queue) would produce wider, more uniform paths instead.

---

### Wall Removal — Index Logic

The trickiest part is knowing *which array entry* to set to `False` for each direction:

| Direction | Neighbor | Wall removed |
|---|---|---|
| North | `(row+1, col)` | `northWall[row+1][col]` |
| South | `(row-1, col)` | `northWall[row][col]` |
| East | `(row, col+1)` | `eastWall[row][col+1]` |
| West | `(row, col-1)` | `eastWall[row][col]` |

---

### Maze Solving — Backtracking DFS

The solver uses the same stack-based DFS approach, but instead of removing walls it **checks** them:

```
1. Start at the entrance cell (gap in left border)
2. Loop:
   a. Find all reachable, unvisited neighbors (no wall between them)
   b. If any exist:
        → Pick one randomly
        → Push current onto stack (this stack IS the solution path)
        → Move to neighbor
   c. If none (dead end):
        → Mark cell as dead end (blue dot)
        → Pop from stack  ← backtrack
3. Stop when current == exit cell
4. Stack = solution path
```

**Key distinction:** A separate `visited_solver` array is used so the solver never revisits cells, preventing infinite loops even in mazes with cycles.

---

### Optional — Cycle Mode

After generating the perfect maze, pressing `C` introduces **cycles** by randomly removing extra interior walls (~5% of total cells). This converts the spanning tree into a graph with loops.

**Why cycles matter:**
- The **shoulder-to-the-wall** rule always works on perfect mazes because they are trees — dead ends always force you back toward the exit
- Cycles break this by creating loops with no dead end, potentially trapping the shoulder rule forever
- The DFS solver is **unaffected** because `visited_solver` prevents it from looping

---

##  Visualization

| Color | Meaning |
|---|---|
| 🔴 Small red dot | Solution path cells |
| 🔴 Large red dot | Current solver position |
| 🔵 Blue dot | Dead end — solver backtracked here |
| ⬜ White | Unvisited cells |

---

##  Code Structure

```
maze_assignment.py
│
├── cell_to_pixel()          # Convert (row, col) → pixel coordinates
├── initialize_maze()        # Create northWall and eastWall arrays
├── set_visited()            # Create visited tracking array
├── draw_maze()              # Render walls, path, and dead ends
│
├── get_unvisited_neighbors()  # DFS generation helper
├── remove_wall()              # Wall removal with correct index logic
├── generate_maze()            # Stack-based DFS maze generation
├── create_entrance_exit()     # Open left and right border gaps
│
├── find_entrance_exit()       # Locate entrance/exit from wall arrays
├── can_move()                 # Check if a wall is passable
├── get_reachable_neighbors()  # DFS solver helper
├── solve_maze()               # Stack-based DFS backtracking solver
│
└── add_cycles()               # Optional: remove extra walls for loops
```

---

##  Conceptual Questions (from assignment)

**Q: Would a queue be better than a stack for generation?**
A queue gives BFS — producing wide, uniform paths instead of long winding corridors. The maze would still be perfect (spanning tree) but would look very different. A stack (DFS) is preferred for the classic maze aesthetic.

**Q: Why does the shoulder-to-the-wall rule always work on perfect mazes?**
Because a perfect maze is a tree. Every dead end forces a turn, and since there are no cycles, following the left wall will always eventually reach the exit as long as both start and end are on the outer boundary.

**Q: Why does DFS still solve cyclic mazes correctly?**
Because `visited_solver` prevents the solver from entering any cell twice. Cycles become irrelevant — the solver treats them like any other junction and moves on.



