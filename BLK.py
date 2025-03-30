import requests
import os
import sys
import json
import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Text, Scrollbar, Frame
from dotenv import load_dotenv
from PIL import Image, ImageTk
from tkinter import ttk
from io import BytesIO

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://open.faceit.com/data/v4"

MATCH_FILE = "match.json"
DATABASE_FILE = "database.json"

def get_match_details(match_url):
    """Fetch match details from Faceit API."""
    match_id = match_url.split("/")[-1]  # Extract match ID from URL
    url = f"{BASE_URL}/matches/{match_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch match details: {e}")
        return None

def extract_teammates(match_data):
    """Extract player CS2 ID, names, and avatars from match data."""
    try:
        teams = match_data["teams"]
        players = []
        for team in teams.values():
            for player in team["roster"]:
                players.append({
                    "cs2_id": player["player_id"],  # CS2 Unique ID (Steam ID)
                    "nickname": player["nickname"],
                    "avatar": player.get("avatar", "")
                })
        return players
    except KeyError:
        messagebox.showerror("Error", "Invalid match data format.")
        return []

def save_match_data(players):
    """Save player details to match.json (resets on each match)."""
    with open(MATCH_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4, ensure_ascii=False)

def load_database():
    """Load or create database.json."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_to_database(cs2_id, note):
    """Save player notes in database.json using CS2 ID."""
    database = load_database()
    database[cs2_id] = note
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)

def on_search():
    """Handle search button click."""
    match_url = entry.get().strip()
    if not match_url:
        messagebox.showwarning("Warning", "Please enter a Faceit matchroom link.")
        return
    
    match_data = get_match_details(match_url)
    if match_data:
        players = extract_teammates(match_data)
        save_match_data(players)
        display_players(players)

def display_players(players):
    """Display teammates with avatars and note fields, separating teams to left and right."""
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    database = load_database()

    left_team_frame = tk.Frame(frame, bg="#1e1e1e")
    right_team_frame = tk.Frame(frame, bg="#1e1e1e")

    left_team_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
    right_team_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

    teams = {"left": players[:len(players)//2], "right": players[len(players)//2:]}

    def populate_team(team_players, parent_frame):
        for player in team_players:
            cs2_id = player["cs2_id"]
            nickname = player["nickname"]
            avatar_url = player["avatar"] or "https://www.ledr.com/colours/black.jpg"

            row_frame = tk.Frame(parent_frame, bg="#1e1e1e")
            row_frame.pack(fill="x", pady=5, padx=10)

            avatar_label = tk.Label(row_frame, bg="#1e1e1e")
            avatar_label.pack(side="left", padx=10, pady=5)

            try:
                avatar_response = requests.get(avatar_url, timeout=5)
                avatar_image = Image.open(BytesIO(avatar_response.content)).resize((50, 50))
                avatar_photo = ImageTk.PhotoImage(avatar_image)
                avatar_label.config(image=avatar_photo)
                avatar_label.image = avatar_photo
            except requests.RequestException:
                pass  

            name_label = tk.Label(row_frame, text=nickname, font=("Arial", 12, "bold"), fg="white", bg="#1e1e1e")
            name_label.pack(side="left", padx=10)

            note_entry = tk.Text(row_frame, height=6, width=40, font=("Arial", 8), bg="#252526", fg="white", 
                                 insertbackground="white", borderwidth=0, highlightthickness=0)  
            note_entry.insert("1.0", database.get(cs2_id, ""))
            note_entry.pack(side="left", padx=10, pady=5)

            save_button = ttk.Button(row_frame, text="Save",
                                     command=lambda id=cs2_id, e=note_entry: save_to_database(id, e.get("1.0", "end").strip()))
            save_button.pack(side="left", padx=10)

    populate_team(teams["left"], left_team_frame)
    populate_team(teams["right"], right_team_frame)

root = tk.Tk()
root.title("BlackList")
root.geometry("1500x850")
root.configure(bg="#1e1e1e")  

style = ttk.Style()
style.theme_use("clam")  
style.configure("TFrame", background="#1e1e1e")
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5, background="#4caf50", foreground="white")
style.configure("TEntry", fieldbackground="#252526", foreground="white", insertcolor="white")

ttk.Label(root, text="Enter Faceit Matchroom Link:", font=("Arial", 14, "bold"), background="#1e1e1e", foreground="white").pack(pady=10)

entry = ttk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=5, ipady=5)

search_button = ttk.Button(root, text="Search", command=on_search, style="TButton")
search_button.pack(pady=10)

container = ttk.Frame(root)
canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)  
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
frame = ttk.Frame(canvas, style="TFrame")

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack(fill="both", expand=True, padx=10, pady=10)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
