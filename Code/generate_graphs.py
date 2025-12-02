import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
INPUT_FILE = "./Data/output/bvboutput.txt"
OUTPUT_GRAPH_DIR = "./Data/output/graphs/"

def generate():
    # Ensure graph directory exists
    os.makedirs(OUTPUT_GRAPH_DIR, exist_ok=True)

    # Read the data file
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}")
        print("Please run bot_vs_bot.py first.")
        return

    with open(INPUT_FILE, "r") as f:
        raw_log = f.read()

    # --- PARSING DATA ---
    neg_nodes = []
    ab_nodes = []
    neg_times = []
    ab_times = []

    # Simple parsing logic
    for line in raw_log.split('\n'):
        parts = [p.strip() for p in line.split('|')]
        # We look for lines that have the structure: Move | Player | Time | Nodes | Status
        if len(parts) < 5 or not parts[0].isdigit(): 
            continue
        
        player = parts[1]
        time_val = float(parts[2])
        nodes_val = int(parts[3])
        
        if player == "Negamax":
            neg_nodes.append(nodes_val)
            neg_times.append(time_val)
        elif player == "Alpha-Beta":
            ab_nodes.append(nodes_val)
            ab_times.append(time_val)

    if not neg_nodes or not ab_nodes:
        print("Error: No valid game data found in the text file.")
        return

    # Calculate Averages
    avg_neg_node = sum(neg_nodes) / len(neg_nodes)
    avg_ab_node = sum(ab_nodes) / len(ab_nodes)
    avg_neg_time = sum(neg_times) / len(neg_times)
    avg_ab_time = sum(ab_times) / len(ab_times)

    labels = ['Negamax', 'Alpha-Beta']

    # --- GRAPH 1: NODES VISITED ---
    plt.figure(figsize=(8, 6))
    values = [avg_neg_node, avg_ab_node]
    colors = ['#ff9999', '#66b3ff']
    bars = plt.bar(labels, values, color=colors, edgecolor='black')
    plt.title('Average Nodes Evaluated per Move', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Nodes', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (yval*0.01), int(yval), ha='center', va='bottom', fontweight='bold')

    save_path = os.path.join(OUTPUT_GRAPH_DIR, 'nodes_visited_comparison.png')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved: {save_path}")

    # --- GRAPH 2: EXECUTION TIME ---
    plt.figure(figsize=(8, 6))
    values_time = [avg_neg_time, avg_ab_time]
    bars = plt.bar(labels, values_time, color=['#ff4d4d', '#3399ff'], edgecolor='black')
    plt.title('Average Execution Time per Move', fontsize=14, fontweight='bold')
    plt.ylabel('Time (Seconds)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (yval*0.01), f"{yval:.4f}s", ha='center', va='bottom', fontweight='bold')

    save_path = os.path.join(OUTPUT_GRAPH_DIR, 'execution_time_comparison.png')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved: {save_path}")

    # --- GRAPH 3: EFFICIENCY OVER TIME ---
    plt.figure(figsize=(10, 6))
    # Align moves to graph x-axis
    turns_neg = range(0, len(neg_nodes)*2, 2)
    turns_ab = range(1, len(ab_nodes)*2 + 1, 2)

    plt.plot(turns_neg, neg_nodes, marker='o', linestyle='-', color='red', label='Negamax')
    plt.plot(turns_ab, ab_nodes, marker='s', linestyle='-', color='blue', label='Alpha-Beta')

    plt.title('Search Efficiency Over Game Duration', fontsize=14, fontweight='bold')
    plt.xlabel('Game Move Number', fontsize=12)
    plt.ylabel('Nodes Visited', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    save_path = os.path.join(OUTPUT_GRAPH_DIR, 'efficiency_over_game_line.png')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved: {save_path}")

if __name__ == "__main__":
    generate()