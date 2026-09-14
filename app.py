import os
import sys
import time
import json
import sqlite3
import socket
import datetime
from io import StringIO

# Ensure safe console printing on Windows
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from flask import (
    Flask, render_template, request, jsonify, session,
    redirect, url_for, Response, send_file
)
from questions_data import QUESTIONS, TEAM_CREDENTIALS, ADMIN_CREDENTIALS

app = Flask(__name__)
app.secret_key = "AI_DST_QUIZ_COMPETITION_SECRET_2026_SUPER_SECURE"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz.db")
EXAM_DURATION_SECONDS = 3600  # 60 minutes

# -------------------------------------------------------------
# Database Setup & Helpers
# -------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Config table
    c.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    
    # Teams table
    c.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            username TEXT PRIMARY KEY,
            display_name TEXT,
            status TEXT DEFAULT 'waiting', -- 'waiting', 'in_progress', 'submitted', 'disqualified'
            start_time REAL DEFAULT NULL,
            end_time REAL DEFAULT NULL,
            score INTEGER DEFAULT 0,
            violations_count INTEGER DEFAULT 0,
            disqualified_reason TEXT DEFAULT NULL
        )
    """)
    
    # Answers table
    c.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            team_id TEXT,
            question_id INTEGER,
            selected_option TEXT,
            is_correct INTEGER DEFAULT 0,
            marked_for_review INTEGER DEFAULT 0,
            saved_at REAL,
            PRIMARY KEY (team_id, question_id)
        )
    """)
    
    # Violations table
    c.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id TEXT,
            violation_type TEXT,
            details TEXT,
            timestamp REAL
        )
    """)
    
    # Initialize competition state if not present
    c.execute("SELECT value FROM config WHERE key = 'competition_active'")
    if not c.fetchone():
        c.execute("INSERT INTO config (key, value) VALUES ('competition_active', '0')")
        c.execute("INSERT INTO config (key, value) VALUES ('competition_start_time', '')")
        
    # Pre-seed 20 teams
    for username in TEAM_CREDENTIALS.keys():
        c.execute("SELECT username FROM teams WHERE username = ?", (username,))
        if not c.fetchone():
            c.execute(
                "INSERT INTO teams (username, display_name, status) VALUES (?, ?, 'waiting')",
                (username, f"Team {username.replace('team', '')}")
            )
            
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# -------------------------------------------------------------
# Authentication & State Helper
# -------------------------------------------------------------
def get_current_user():
    return session.get("user")

def get_current_role():
    return session.get("role")

def is_competition_active():
    conn = get_db()
    row = conn.execute("SELECT value FROM config WHERE key = 'competition_active'").fetchone()
    conn.close()
    return row["value"] == "1" if row else False

def format_timestamp(ts):
    if not ts:
        return "-"
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%I:%M:%S %p")

def format_duration(seconds):
    if seconds is None:
        return "-"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m {s}s"

# -------------------------------------------------------------
# Web Page Routes
# -------------------------------------------------------------
@app.route("/")
def index():
    user = get_current_user()
    role = get_current_role()
    if not user:
        return render_template("login.html")
    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    return render_template("index.html", username=user)

@app.route("/admin")
def admin_dashboard():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return redirect(url_for("login_page"))
    return render_template("admin.html", admin_user=user)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        data = request.get_json() or request.form
        username = (data.get("username") or "").strip().lower()
        password = (data.get("password") or "").strip()
        
        # Admin check (case-insensitive for username)
        if username in ["maha", "admin"] and password == ADMIN_CREDENTIALS.get("MAHA"):
            session["user"] = "MAHA"
            session["role"] = "admin"
            return jsonify({"success": True, "redirect": "/admin", "role": "admin"})
            
        # Team check
        if username in TEAM_CREDENTIALS and password == TEAM_CREDENTIALS[username]:
            session["user"] = username
            session["role"] = "team"
            return jsonify({"success": True, "redirect": "/", "role": "team"})
            
        return jsonify({"success": False, "error": "Invalid Username or Password! Please check and retry."}), 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# -------------------------------------------------------------
# Student & Exam API Endpoints
# -------------------------------------------------------------
@app.route("/api/me")
def api_me():
    user = get_current_user()
    role = get_current_role()
    if not user:
        return jsonify({"authenticated": False})
    return jsonify({
        "authenticated": True,
        "username": user,
        "role": role
    })

@app.route("/api/competition_status")
def api_competition_status():
    active = is_competition_active()
    user = get_current_user()
    role = get_current_role()
    
    team_info = None
    if role == "team" and user:
        conn = get_db()
        row = conn.execute("SELECT * FROM teams WHERE username = ?", (user,)).fetchone()
        conn.close()
        if row:
            team_info = dict(row)
            
    return jsonify({
        "competition_active": active,
        "team_info": team_info
    })

@app.route("/api/start_quiz", methods=["POST"])
def api_start_quiz():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "team":
        return jsonify({"success": False, "error": "Unauthorized"}), 401
        
    if not is_competition_active():
        return jsonify({
            "success": False,
            "error": "Admin MAHA has not started the competition yet. Please wait in the lobby!"
        }), 403
        
    conn = get_db()
    team = conn.execute("SELECT * FROM teams WHERE username = ?", (user,)).fetchone()
    
    if team["status"] in ["submitted", "disqualified"]:
        conn.close()
        return jsonify({"success": False, "error": f"Exam already {team['status']}"}), 400
        
    now = time.time()
    start_time = team["start_time"]
    
    if team["status"] == "waiting" or not start_time:
        start_time = now
        conn.execute(
            "UPDATE teams SET status = 'in_progress', start_time = ? WHERE username = ?",
            (start_time, user)
        )
        conn.commit()
        
    elapsed = now - start_time
    remaining = max(0, EXAM_DURATION_SECONDS - elapsed)
    
    conn.close()
    return jsonify({
        "success": True,
        "start_time": start_time,
        "elapsed_seconds": elapsed,
        "remaining_seconds": int(remaining)
    })

@app.route("/api/questions")
def api_questions():
    user = get_current_user()
    role = get_current_role()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
        
    sanitized = []
    for q in QUESTIONS:
        item = {
            "id": q["id"],
            "category": q.get("category", ""),
            "question": q["question"],
            "options": q["options"],
            "passage": q.get("passage"),
            "code_snippet": q.get("code_snippet"),
            "image_svg": q.get("image_svg")
        }
        if role == "admin":
            item["answer"] = q["answer"]
        sanitized.append(item)
        
    user_answers = {}
    if role == "team" and user:
        conn = get_db()
        rows = conn.execute("SELECT * FROM answers WHERE team_id = ?", (user,)).fetchall()
        for r in rows:
            user_answers[str(r["question_id"])] = {
                "selected_option": r["selected_option"],
                "marked_for_review": bool(r["marked_for_review"])
            }
        conn.close()
        
    return jsonify({
        "questions": sanitized,
        "user_answers": user_answers,
        "total": len(sanitized)
    })

@app.route("/api/save_answer", methods=["POST"])
def api_save_answer():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "team":
        return jsonify({"success": False, "error": "Unauthorized"}), 401
        
    data = request.get_json() or {}
    q_id = int(data.get("question_id", 0))
    selected = data.get("selected_option")
    marked = 1 if data.get("marked_for_review") else 0
    
    if q_id < 1 or q_id > len(QUESTIONS):
        return jsonify({"success": False, "error": "Invalid question ID"}), 400
        
    conn = get_db()
    team = conn.execute("SELECT * FROM teams WHERE username = ?", (user,)).fetchone()
    if not team or team["status"] != "in_progress":
        conn.close()
        return jsonify({"success": False, "error": "Exam is not active"}), 400
        
    # Check if timer expired
    now = time.time()
    if team["start_time"] and (now - team["start_time"]) > (EXAM_DURATION_SECONDS + 30):
        # Auto-submit if exceeded
        conn.execute("UPDATE teams SET status = 'submitted', end_time = ? WHERE username = ?", (now, user))
        conn.commit()
        conn.close()
        return jsonify({"success": False, "error": "Time has expired! Exam submitted.", "time_expired": True}), 403
        
    correct_key = QUESTIONS[q_id - 1]["answer"]
    is_correct = 1 if selected == correct_key else 0
    
    conn.execute("""
        INSERT INTO answers (team_id, question_id, selected_option, is_correct, marked_for_review, saved_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(team_id, question_id) DO UPDATE SET
            selected_option = excluded.selected_option,
            is_correct = excluded.is_correct,
            marked_for_review = excluded.marked_for_review,
            saved_at = excluded.saved_at
    """, (user, q_id, selected, is_correct, marked, now))
    
    # Recalculate score
    score_row = conn.execute("SELECT COUNT(*) as score FROM answers WHERE team_id = ? AND is_correct = 1", (user,)).fetchone()
    current_score = score_row["score"]
    conn.execute("UPDATE teams SET score = ? WHERE username = ?", (current_score, user))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "success": True,
        "question_id": q_id,
        "selected_option": selected,
        "marked_for_review": bool(marked),
        "saved_at": now
    })

@app.route("/api/submit_quiz", methods=["POST"])
def api_submit_quiz():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "team":
        return jsonify({"success": False, "error": "Unauthorized"}), 401
        
    conn = get_db()
    team = conn.execute("SELECT * FROM teams WHERE username = ?", (user,)).fetchone()
    if not team:
        conn.close()
        return jsonify({"success": False, "error": "Team not found"}), 404
        
    if team["status"] == "submitted":
        conn.close()
        return jsonify({"success": True, "message": "Already submitted", "score": team["score"]})
        
    now = time.time()
    # Compute score
    score_row = conn.execute("SELECT COUNT(*) as score FROM answers WHERE team_id = ? AND is_correct = 1", (user,)).fetchone()
    final_score = score_row["score"]
    
    conn.execute("""
        UPDATE teams 
        SET status = 'submitted', end_time = ?, score = ?
        WHERE username = ?
    """, (now, final_score, user))
    
    conn.commit()
    conn.close()
    
    time_taken = (now - team["start_time"]) if team["start_time"] else 0
    return jsonify({
        "success": True,
        "status": "submitted",
        "score": final_score,
        "total": len(QUESTIONS),
        "time_taken_seconds": time_taken,
        "submitted_at": format_timestamp(now)
    })

@app.route("/api/report_violation", methods=["POST"])
def api_report_violation():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "team":
        return jsonify({"success": False, "error": "Unauthorized"}), 401
        
    data = request.get_json() or {}
    v_type = data.get("type", "tab_switch")
    details = data.get("details", "Switched tab or minimized browser window")
    now = time.time()
    
    conn = get_db()
    team = conn.execute("SELECT * FROM teams WHERE username = ?", (user,)).fetchone()
    if not team or team["status"] not in ["in_progress"]:
        conn.close()
        return jsonify({"success": False, "action": "ignored"})
        
    new_count = (team["violations_count"] or 0) + 1
    
    conn.execute(
        "INSERT INTO violations (team_id, violation_type, details, timestamp) VALUES (?, ?, ?, ?)",
        (user, v_type, details, now)
    )
    
    # 2-Strike Disqualification Policy:
    # 1st violation: Strict Warning Popup
    # 2nd violation: Immediate Disqualification & Disconnect
    if new_count >= 2:
        reason = f"Disqualified for {new_count} tab switches/screen exits during exam."
        # Calculate score so far
        score_row = conn.execute("SELECT COUNT(*) as score FROM answers WHERE team_id = ? AND is_correct = 1", (user,)).fetchone()
        conn.execute("""
            UPDATE teams 
            SET violations_count = ?, status = 'disqualified', end_time = ?, disqualified_reason = ?, score = ?
            WHERE username = ?
        """, (new_count, now, reason, score_row["score"], user))
        conn.commit()
        conn.close()
        return jsonify({
            "success": True,
            "action": "disqualify",
            "violation_count": new_count,
            "message": "🚨 EXAM TERMINATED: You switched tabs or navigated away from the exam. You have been DISQUALIFIED from the competition."
        })
    else:
        conn.execute("UPDATE teams SET violations_count = ? WHERE username = ?", (new_count, user))
        conn.commit()
        conn.close()
        return jsonify({
            "success": True,
            "action": "warn",
            "violation_count": new_count,
            "max_violations": 2,
            "message": "⚠️ WARNING 1 OF 2: Tab switching is strictly forbidden! If you switch tabs or leave this window one more time, you will be permanently DISQUALIFIED and disconnected!"
        })

# -------------------------------------------------------------
# Admin API Endpoints
# -------------------------------------------------------------
@app.route("/api/admin/live_dashboard")
def api_admin_dashboard():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db()
    teams_rows = conn.execute("SELECT * FROM teams").fetchall()
    
    teams_list = []
    counts = {"waiting": 0, "in_progress": 0, "submitted": 0, "disqualified": 0}
    
    now = time.time()
    for row in teams_rows:
        t = dict(row)
        status = t["status"]
        counts[status] = counts.get(status, 0) + 1
        
        # Count answered questions
        ans_count = conn.execute("SELECT COUNT(*) as cnt FROM answers WHERE team_id = ?", (t["username"],)).fetchone()["cnt"]
        t["answered_count"] = ans_count
        
        # Time calculations
        if t["start_time"]:
            t["start_time_str"] = format_timestamp(t["start_time"])
            if t["end_time"]:
                t["end_time_str"] = format_timestamp(t["end_time"])
                t["time_taken_str"] = format_duration(t["end_time"] - t["start_time"])
                t["time_taken_seconds"] = int(t["end_time"] - t["start_time"])
            else:
                t["end_time_str"] = "Running..."
                elapsed = now - t["start_time"]
                t["time_taken_str"] = format_duration(elapsed)
                t["time_taken_seconds"] = int(elapsed)
        else:
            t["start_time_str"] = "—"
            t["end_time_str"] = "—"
            t["time_taken_str"] = "—"
            t["time_taken_seconds"] = 999999
            
        teams_list.append(t)
        
    # Sort for leaderboard: highest score first, then lowest time taken
    def sort_key(item):
        status_rank = 0 if item["status"] == "submitted" else (1 if item["status"] == "in_progress" else 2)
        return (status_rank, -item["score"], item["time_taken_seconds"])
        
    teams_list.sort(key=sort_key)
    
    # Assign leaderboard ranks
    rank = 1
    for t in teams_list:
        if t["status"] in ["submitted", "in_progress"] and t["answered_count"] > 0:
            t["rank"] = rank
            rank += 1
        else:
            t["rank"] = "—"

    active = is_competition_active()
    conn.close()
    
    return jsonify({
        "competition_active": active,
        "counts": counts,
        "total_teams": len(teams_list),
        "teams": teams_list,
        "server_time": format_timestamp(now),
        "local_ip": get_local_ip()
    })

@app.route("/api/admin/start_competition", methods=["POST"])
def api_admin_start_competition():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
        
    now = time.time()
    conn = get_db()
    conn.execute("UPDATE config SET value = '1' WHERE key = 'competition_active'")
    conn.execute("UPDATE config SET value = ? WHERE key = 'competition_start_time'", (str(now),))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Competition started! All teams can now begin their exam."})

@app.route("/api/admin/stop_competition", methods=["POST"])
def api_admin_stop_competition():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db()
    conn.execute("UPDATE config SET value = '0' WHERE key = 'competition_active'")
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Competition paused/stopped."})

@app.route("/api/admin/team_details/<team_id>")
def api_admin_team_details(team_id):
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db()
    team = conn.execute("SELECT * FROM teams WHERE username = ?", (team_id,)).fetchone()
    if not team:
        conn.close()
        return jsonify({"error": "Team not found"}), 404
        
    answers_rows = conn.execute("SELECT * FROM answers WHERE team_id = ?", (team_id,)).fetchall()
    answers_map = {r["question_id"]: dict(r) for r in answers_rows}
    
    violations_rows = conn.execute("SELECT * FROM violations WHERE team_id = ? ORDER BY timestamp DESC", (team_id,)).fetchall()
    violations_list = [
        {
            "type": r["violation_type"],
            "details": r["details"],
            "time": format_timestamp(r["timestamp"])
        } for r in violations_rows
    ]
    
    breakdown = []
    for q in QUESTIONS:
        ans = answers_map.get(q["id"])
        selected = ans["selected_option"] if ans else None
        is_correct = (selected == q["answer"]) if selected else False
        
        breakdown.append({
            "id": q["id"],
            "category": q.get("category", ""),
            "question": q["question"],
            "options": q["options"],
            "correct_answer": q["answer"],
            "selected_option": selected,
            "is_correct": is_correct,
            "status": "correct" if (selected and is_correct) else ("incorrect" if selected else "unanswered")
        })
        
    conn.close()
    return jsonify({
        "team": dict(team),
        "breakdown": breakdown,
        "violations": violations_list
    })

@app.route("/api/admin/reset_team", methods=["POST"])
def api_admin_reset_team():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.get_json() or {}
    team_id = data.get("team_id")
    action_type = data.get("action_type", "unlock") # "unlock" or "full_reset"
    
    conn = get_db()
    if action_type == "unlock":
        # Forgive / unlock disqualified team so they can resume
        conn.execute("""
            UPDATE teams 
            SET status = 'in_progress', disqualified_reason = NULL, violations_count = 1
            WHERE username = ?
        """, (team_id,))
    elif action_type == "full_reset":
        # Full reset of answers and timer
        conn.execute("DELETE FROM answers WHERE team_id = ?", (team_id,))
        conn.execute("DELETE FROM violations WHERE team_id = ?", (team_id,))
        conn.execute("""
            UPDATE teams 
            SET status = 'waiting', start_time = NULL, end_time = NULL, score = 0, violations_count = 0, disqualified_reason = NULL
            WHERE username = ?
        """, (team_id,))
        
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Team {team_id} updated successfully."})

@app.route("/api/admin/export_csv")
def api_admin_export_csv():
    user = get_current_user()
    role = get_current_role()
    if not user or role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db()
    teams = conn.execute("SELECT * FROM teams ORDER BY score DESC").fetchall()
    
    output = StringIO()
    output.write("Rank,Team ID,Team Name,Status,Score (out of 60),Answered,Violations,Start Time,End Time,Time Taken\n")
    
    rank = 1
    for t in teams:
        ans_count = conn.execute("SELECT COUNT(*) as cnt FROM answers WHERE team_id = ?", (t["username"],)).fetchone()["cnt"]
        st = format_timestamp(t["start_time"])
        et = format_timestamp(t["end_time"])
        tt = format_duration(t["end_time"] - t["start_time"]) if (t["start_time"] and t["end_time"]) else "-"
        
        output.write(f'{rank},{t["username"]},"{t["display_name"]}",{t["status"]},{t["score"]},{ans_count},{t["violations_count"]},"{st}","{et}","{tt}"\n')
        rank += 1
        
    conn.close()
    
    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=quiz_competition_results.csv"}
    )

# -------------------------------------------------------------
# Main Entry Point
# -------------------------------------------------------------
if __name__ == "__main__":
    local_ip = get_local_ip()
    print("=" * 65)
    print("   AI&DST 2026 QUIZ COMPETITION PLATFORM SERVER STARTED")
    print("=" * 65)
    print(f"   -> Local URL:      http://localhost:5000")
    print(f"   -> Wi-Fi/LAN URL:  http://{local_ip}:5000")
    print(f"   -> Admin Username: MAHA")
    print(f"   -> Admin Password: AI&DSA2026")
    print(f"   -> Teams:          team1 to team20 (Password: AI&DST2026)")
    print("=" * 65)
    app.run(host="0.0.0.0", port=5000, debug=False)
