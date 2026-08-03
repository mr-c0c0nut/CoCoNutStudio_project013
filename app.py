#made by MCO (mr.coco own web) , code 003 -> nâng cấp giao diện đồng bộ với code 004 + thêm animation
from flask import Flask, jsonify, render_template_string, request, session
import json
import os
import secrets
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("ANGELTIER_SECRET_KEY", secrets.token_hex(32))

# 🔐 Cấu hình bảng điều khiển nhân viên kỹ thuật (2 lớp mật khẩu)
ADMIN_PASSWORD_1 = "33298"
ADMIN_WEBHOOK_URL = "https://discord.com/api/webhooks/1533666984867270696/g6UmiB6KgOZU3jgpjGuUcN-iR32G26RJfEkeNEAE-ssF-HSUzdg8gQ4qtlUkMntYhSks"
PLAYERS_FILE = "players.json"

# 📊 Bảng quy đổi điểm số Tier
TIER_POINTS = {
    'LT5': 10, 'HT5': 15,
    'LT4': 20, 'HT4': 25,
    'LT3': 30, 'HT3': 40,
    'LT2': 50, 'HT2': 60,
    'LT1': 70, 'HT1': 80
}


def calculate_points(tiers):
    """Hàm tính tổng điểm từ các Tier của người chơi"""
    if not tiers or not isinstance(tiers, dict):
        return 0
    total = 0
    for mode, tier in tiers.items():
        clean_tier = str(tier).strip().upper()
        total += TIER_POINTS.get(clean_tier, 0)
    return total


def load_real_players():
    """Hàm đọc dữ liệu từ file JSON nếu bot lưu ra file"""
    for filename in ['data.json', 'players.json', 'leaderboard.json']:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Lỗi đọc file {filename}: {e}")
    return None


def notify_discord(message):
    """Gửi thông báo về Discord qua webhook cấu hình sẵn ở server (không lộ ra client)."""
    try:
        requests.post(ADMIN_WEBHOOK_URL, json={"content": message}, timeout=5)
    except Exception as e:
        print(f"Không gửi được thông báo Discord: {e}")


def require_admin():
    return bool(session.get("admin_authed"))


# Dữ liệu mẫu (giữ lại 3 cái tên gốc của code 003: thekidpika, Ghost_kevin, zemnr
# rồi gộp thêm dữ liệu mẫu của code 004 để bảng xếp hạng có nhiều người chơi hơn)
DEFAULT_PLAYERS = [
    {"name": "thekidpika", "avatar": "https://mc-heads.net/avatar/thekidpika/100.png", "tiers": {"Sword": "HT1", "Nethpot": "HT1"}},
    {"name": "AGL_Mipp", "avatar": "https://mc-heads.net/avatar/AGL_Mipp/100.png", "tiers": {"Sword": "HT1", "Nethpot": "HT2"}},
    {"name": "anh5me27051", "avatar": "https://mc-heads.net/avatar/anh5me27051/100.png", "tiers": {"Sword": "HT1", "Nethpot": "HT2"}},
    {"name": "Ghost_kevin", "avatar": "https://mc-heads.net/avatar/Ghost_kevin/100.png", "tiers": {"Sword": "HT1", "Pot": "HT2"}},
    {"name": "zemnr", "avatar": "https://mc-heads.net/avatar/zemnr/100.png", "tiers": {"Sword": "HT2", "Axe": "HT2"}},
    {"name": "NeoReo_", "avatar": "https://mc-heads.net/avatar/NeoReo_/100.png", "tiers": {"Sword": "HT2", "Axe": "HT2"}},
    {"name": "Ag_qkhang", "avatar": "https://mc-heads.net/avatar/Ag_qkhang/100.png", "tiers": {"Sword": "HT2", "Nethpot": "HT3"}},
    {"name": "LikedaeMC", "avatar": "https://mc-heads.net/avatar/LikedaeMC/100.png", "tiers": {"Sword": "HT2", "Nethpot": "HT3"}},
    {"name": "Vandekynang22", "avatar": "https://mc-heads.net/avatar/Vandekynang22/100.png", "tiers": {"Sword": "HT3", "Smp": "HT2"}},
    {"name": "Uchiha_nho", "avatar": "https://mc-heads.net/avatar/Uchiha_nho/100.png", "tiers": {"Sword": "HT3", "Pot": "HT3"}},
    {"name": "Chuyenn", "avatar": "https://mc-heads.net/avatar/Chuyenn/100.png", "tiers": {"Sword": "HT3", "Pot": "HT3"}},
    {"name": "FoxXinhGai", "avatar": "https://mc-heads.net/avatar/FoxXinhGai/100.png", "tiers": {"Sword": "HT4", "Vanilla": "HT3"}},
]


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    raw_players = load_real_players()
    if raw_players is None:
        raw_players = DEFAULT_PLAYERS

    leaderboard = []
    for p in raw_players:
        tiers = p.get("tiers", {})
        pts = p.get("points_override")
        if not isinstance(pts, (int, float)):
            pts = calculate_points(tiers)
        tier_display = [f"{m}: {t}" for m, t in tiers.items()]
        leaderboard.append({
            "id": p.get("id", ""),
            "name": p.get("name", "Unknown"),
            "avatar": p.get("avatar", f"https://mc-heads.net/avatar/{p.get('name', 'Steve')}/100.png"),
            "points": pts,
            "tiers": tiers,
            "tier_display": tier_display
        })

    # 🏆 SẮP XẾP GIẢM DẦN THEO POINT (Ai cao điểm nhất đứng Top)
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    return jsonify(leaderboard)


# ============================================================
# 🛠️ BẢNG ĐIỀU KHIỂN NHÂN VIÊN KỸ THUẬT — xác thực 2 lớp
# ============================================================

@app.route('/api/admin/step1', methods=['POST'])
def admin_step1():
    data = request.get_json(silent=True) or {}
    password = str(data.get("password", "")).strip()
    if password == ADMIN_PASSWORD_1:
        session["admin_step1_ok"] = True
        return jsonify({"ok": True})
    session["admin_step1_ok"] = False
    return jsonify({"ok": False}), 401


@app.route('/api/admin/step2', methods=['POST'])
def admin_step2():
    if not session.get("admin_step1_ok"):
        return jsonify({"ok": False, "error": "Chưa hoàn thành lớp mật khẩu 1"}), 401

    data = request.get_json(silent=True) or {}
    webhook = str(data.get("webhook", "")).strip()

    if webhook == ADMIN_WEBHOOK_URL:
        session["admin_authed"] = True
        session["admin_step1_ok"] = False
        notify_discord("✅ **AngelTier** — Một nhân viên kỹ thuật vừa đăng nhập thành công vào bảng điều khiển.")
        return jsonify({"ok": True})
    else:
        session["admin_authed"] = False
        session["admin_step1_ok"] = False
        notify_discord("🚨 **AngelTier** — CẢNH BÁO: có người nhập sai mật khẩu lớp 2 khi cố truy cập bảng điều khiển (khả năng đột nhập).")
        return jsonify({"ok": False}), 401


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session["admin_authed"] = False
    session["admin_step1_ok"] = False
    return jsonify({"ok": True})


@app.route('/api/admin/players', methods=['GET'])
def admin_get_players():
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403
    raw_players = load_real_players()
    if raw_players is None:
        raw_players = DEFAULT_PLAYERS
    return jsonify({"ok": True, "players": raw_players})


@app.route('/api/admin/players', methods=['POST'])
def admin_save_players():
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    data = request.get_json(silent=True) or {}
    players = data.get("players")
    if not isinstance(players, list):
        return jsonify({"ok": False, "error": "Dữ liệu không hợp lệ"}), 400

    cleaned = []
    for p in players:
        if not isinstance(p, dict):
            continue
        name = str(p.get("name", "")).strip()
        if not name:
            continue
        avatar = str(p.get("avatar", "")).strip() or f"https://mc-heads.net/avatar/{name}/100.png"
        tiers_in = p.get("tiers", {}) or {}
        tiers = {}
        if isinstance(tiers_in, dict):
            for mode, tier in tiers_in.items():
                mode = str(mode).strip()
                tier = str(tier).strip().upper()
                if mode and tier:
                    tiers[mode] = tier
        entry = {"name": name, "avatar": avatar, "tiers": tiers}
        po = p.get("points_override")
        if isinstance(po, (int, float)):
            entry["points_override"] = po
        cleaned.append(entry)

    try:
        with open(PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({"ok": False, "error": f"Không thể lưu file: {e}"}), 500

    notify_discord(f"🛠️ **AngelTier** — Nhân viên kỹ thuật vừa cập nhật bảng xếp hạng ({len(cleaned)} người chơi).")
    return jsonify({"ok": True, "players": cleaned})


@app.route('/')
def home():
    return render_template("index.html")


# [EXTRACTED] HTML Template -> templates/index.html


if __name__ == '__main__':
    print("🔥 Server AngelTier (giao diện mới + animation) đang chạy tại http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
