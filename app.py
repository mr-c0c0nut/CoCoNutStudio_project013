import json
import os
import secrets
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    session,
)
import requests
from supabase import create_client, Client

app = Flask(__name__)

# 🔐 Cấu hình Bảo mật qua Environment Variables (Ưu tiên lấy từ Render, nếu không có mới lấy giá trị mặc định)
app.secret_key = os.environ.get(
    "ANGELTIER_SECRET_KEY", secrets.token_hex(32) # Dùng token ngẫu nhiên nếu không set
)

ADMIN_PASSWORD_1 = os.environ.get("ADMIN_PASSWORD_1", "33298")
ADMIN_WEBHOOK_URL = os.environ.get(
    "ADMIN_WEBHOOK_URL",
    "https://discord.com/api/webhooks/1533666984867270696/g6UmiB6KgOZU3jgpjGuUcN-iR32G26RJfEkeNEAE-ssF-HSUzdg8gQ4qtlUkMntYhSks",
)

# ⚡ KẾT NỐI DATABASE SUPABASE
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://zkkkfasdwuvqrytdgqxbl.supabase.co/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_ejd9s6yhQimvU8sy8YR_ww_44db-pwP")

supabase: Client = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"⚠️ Chưa khởi tạo được Supabase Client: {e}")

# 📊 Bảng quy đổi điểm số Tier
TIER_POINTS = {
    "LT5": 10, "HT5": 15,
    "LT4": 20, "HT4": 25,
    "LT3": 30, "HT3": 40,
    "LT2": 50, "HT2": 60,
    "LT1": 70, "HT1": 80,
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


def parse_tier_data(raw_tier):
    """Xử lý định dạng dữ liệu Tier (Dict, JSON string hoặc Chuỗi đơn)"""
    if not raw_tier:
        return {}
    
    if isinstance(raw_tier, dict):
        return raw_tier

    if isinstance(raw_tier, str):
        # Thử parse xem có phải chuỗi JSON dict hay không
        try:
            parsed = json.loads(raw_tier)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        # Nếu chỉ là chuỗi đơn (ví dụ "HT1")
        return {"Tier": raw_tier.strip()}
    
    return {}


def load_real_players():
    """Hàm đọc dữ liệu từ database Supabase"""
    if not supabase:
        return None
    try:
        response = supabase.table("Angel bot - website").select("*").execute()
        data = response.data

        formatted_players = []
        for row in data:
            ign = row.get("ign") or "Unknown"
            raw_tier = row.get("tier")
            tiers_dict = parse_tier_data(raw_tier)

            formatted_players.append(
                {
                    "id": row.get("id"),
                    "name": ign,
                    "avatar": f"https://mc-heads.net/avatar/{ign}/100.png",
                    "tiers": tiers_dict,
                    "points_override": None,
                }
            )
        return formatted_players if formatted_players else None
    except Exception as e:
        print(f"Lỗi đọc dữ liệu từ Supabase: {e}")
        return None


def notify_discord(message):
    """Gửi thông báo về Discord qua webhook"""
    if not ADMIN_WEBHOOK_URL:
        return
    try:
        requests.post(ADMIN_WEBHOOK_URL, json={"content": message}, timeout=5)
    except Exception as e:
        print(f"Không gửi được thông báo Discord: {e}")


def require_admin():
    return bool(session.get("admin_authed"))


DEFAULT_PLAYERS = [
    {
        "name": "thekidpika",
        "avatar": "https://mc-heads.net/avatar/thekidpika/100.png",
        "tiers": {"Tier": "HT1"},
    },
    {
        "name": "AGL_Mipp",
        "avatar": "https://mc-heads.net/avatar/AGL_Mipp/100.png",
        "tiers": {"Tier": "HT2"},
    },
]


@app.route("/api/leaderboard", methods=["GET"])
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
        leaderboard.append(
            {
                "id": p.get("id", ""),
                "name": p.get("name", "Unknown"),
                "avatar": p.get(
                    "avatar",
                    f"https://mc-heads.net/avatar/{p.get('name', 'Steve')}/100.png",
                ),
                "points": pts,
                "tiers": tiers,
                "tier_display": tier_display,
            }
        )

    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    return jsonify(leaderboard)


@app.route("/api/admin/step1", methods=["POST"])
def admin_step1():
    data = request.get_json(silent=True) or {}
    password = str(data.get("password", "")).strip()
    if password == ADMIN_PASSWORD_1:
        session["admin_step1_ok"] = True
        return jsonify({"ok": True})
    session["admin_step1_ok"] = False
    return jsonify({"ok": False}), 401


@app.route("/api/admin/step2", methods=["POST"])
def admin_step2():
    if not session.get("admin_step1_ok"):
        return jsonify({"ok": False, "error": "Chưa hoàn thành lớp mật khẩu 1"}), 401

    data = request.get_json(silent=True) or {}
    webhook = str(data.get("webhook", "")).strip()

    if webhook == ADMIN_WEBHOOK_URL:
        session["admin_authed"] = True
        session["admin_step1_ok"] = False
        notify_discord("✅ **AngelTier** — Một nhân viên kỹ thuật vừa đăng nhập thành công.")
        return jsonify({"ok": True})
    else:
        session["admin_authed"] = False
        session["admin_step1_ok"] = False
        notify_discord("🚨 **AngelTier** — CẢNH BÁO: Đăng nhập thất bại ở lớp 2.")
        return jsonify({"ok": False}), 401


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/admin/players", methods=["GET"])
def admin_get_players():
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403
    raw_players = load_real_players()
    if raw_players is None:
        raw_players = DEFAULT_PLAYERS
    return jsonify({"ok": True, "players": raw_players})


@app.route("/api/admin/players", methods=["POST"])
def admin_save_players():
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    data = request.get_json(silent=True) or {}
    players = data.get("players")
    if not isinstance(players, list):
        return jsonify({"ok": False, "error": "Dữ liệu không hợp lệ"}), 400

    cleaned = []
    db_records = []

    for p in players:
        if not isinstance(p, dict):
            continue
        name = str(p.get("name", "")).strip()
        if not name:
            continue
        avatar = (
            str(p.get("avatar", "")).strip()
            or f"https://mc-heads.net/avatar/{name}/100.png"
        )
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

        tier_val = list(tiers.values())[0] if len(tiers) == 1 else (tiers if tiers else None)

        db_records.append({"ign": name, "tier": tier_val})

    if supabase and db_records:
        try:
            # Lưu ý: Cột 'ign' trong Supabase BẮT BUỘC phải đặt thuộc tính UNIQUE/Primary Key để upsert hoạt động
            supabase.table("Angel bot - website").upsert(
                db_records, on_conflict="ign"
            ).execute()
        except Exception as e:
            return jsonify({"ok": False, "error": f"Lỗi lưu Supabase: {str(e)}"}), 500

    notify_discord(f"🛠️ **AngelTier** — Đã cập nhật bảng xếp hạng ({len(cleaned)} người chơi).")
    return jsonify({"ok": True, "players": cleaned})


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
