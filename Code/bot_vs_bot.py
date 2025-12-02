import connect4_board as c4
import Minmax     # Imports your Negamax implementation
import alphabeta  # Imports your Alpha-Beta implementation
import time
import os

# CONFIGURATION
TEST_DEPTH = 4 
OUTPUT_DIR = "./Data/output/"
OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, "bvboutput.txt")

def log(message, file_handle):
    """Helper to print to console and write to file simultaneously."""
    print(message)
    file_handle.write(message + "\n")

def run_battle():
    # Create directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize the board
    board = c4.position()
    turn = 0
    data_log = [] 

    with open(OUTPUT_FILE_PATH, "w") as f:
        log(f"--- STARTING BATTLE: NEGAMAX vs ALPHA-BETA (Depth {TEST_DEPTH}) ---", f)
        log(f"{'Turn':<5} | {'Player':<12} | {'Time (s)':<10} | {'Nodes Visited':<15} | {'Move Selected'}", f)
        log("-" * 65, f)

        while not board.tie_board():
            start_time = time.time()
            nodes = 0
            chosen_board = None
            player_name = ""

            if turn == 0:
                player_name = "Negamax"
                Minmax.NODES_VISITED = 0
                result = Minmax.negmax(board, TEST_DEPTH)
                chosen_board = result[1]
                nodes = Minmax.NODES_VISITED
            else:
                player_name = "Alpha-Beta"
                alphabeta.NODES_VISITED = 0
                result = alphabeta.alphabeta(board, TEST_DEPTH, -float('inf'), float('inf'))
                chosen_board = result[1]
                nodes = alphabeta.NODES_VISITED

            end_time = time.time()
            duration = end_time - start_time
            
            # Log the move
            log(f"{board.get_move():<5} | {player_name:<12} | {duration:<10.4f} | {nodes:<15} | Completed", f)
            
            data_log.append({
                "player": player_name,
                "time": duration,
                "nodes": nodes
            })

            board = chosen_board
            
            piece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE
            if board.winning_move(piece):
                log("-" * 65, f)
                log(f"WINNER: {player_name} wins on move {board.get_move()}!", f)
                break
                
            turn = (turn + 1) % 2

        if board.tie_board():
            log("It's a tie!", f)

        # --- SUMMARY ---
        log("\n\n=== FINAL RESULTS FOR PRESENTATION ===", f)
        
        neg_times = [d['time'] for d in data_log if d['player'] == "Negamax"]
        neg_nodes = [d['nodes'] for d in data_log if d['player'] == "Negamax"]
        
        ab_times = [d['time'] for d in data_log if d['player'] == "Alpha-Beta"]
        ab_nodes = [d['nodes'] for d in data_log if d['player'] == "Alpha-Beta"]

        if neg_times and ab_times:
            avg_neg_time = sum(neg_times) / len(neg_times)
            avg_neg_node = sum(neg_nodes) / len(neg_nodes)
            avg_ab_time = sum(ab_times) / len(ab_times)
            avg_ab_node = sum(ab_nodes) / len(ab_nodes)
            
            log(f"Average Execution Time (Depth {TEST_DEPTH}):", f)
            log(f"  Negamax:    {avg_neg_time:.4f} seconds", f)
            log(f"  Alpha-Beta: {avg_ab_time:.4f} seconds", f)
            log(f"  Speedup:    {avg_neg_time / avg_ab_time:.2f}x faster", f)
            
            log(f"\nAverage Nodes Expanded (Depth {TEST_DEPTH}):", f)
            log(f"  Negamax:    {int(avg_neg_node)} nodes", f)
            log(f"  Alpha-Beta: {int(avg_ab_node)} nodes", f)
            log(f"  Efficiency: {avg_neg_node / avg_ab_node:.2f}x fewer nodes", f)

    print(f"\nDone! Results saved to: {OUTPUT_FILE_PATH}")

if __name__ == "__main__":
    run_battle()