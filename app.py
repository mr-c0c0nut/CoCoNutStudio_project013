import json
import os
from datetime import datetime
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
app.secret_key = os.environ.get(
    "ANGELTIER_SECRET_KEY", "ANGELTIER_SUPER_SECRET_KEY_2026"
)

# ── Cấu hình bảo mật ──────────────────────────────────
ADMIN_PASSWORD_1 = "33298"
ADMIN_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1533666984867270696/"
    "g6UmiB6KgOZU3jgpjGuUcN-iR32G26RJfEkeNEAE-ssF-"
    "HSUzdg8gQ4qtlUkMntYhSks"
)

# ── Kết nối Supabase ──────────────────────────────────
SUPABASE_URL = "https://zkkkfasdwuvqrytdgqxbl.supabase.co/"
SUPABASE_KEY = "sb_publishable_ejd9s6yhQimvU8sy8YR_ww_44db-pwP"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Đã khởi tạo Supabase Client thành công")
except Exception as e:
    supabase = None
    print(f"⚠️ Chưa khởi tạo được Supabase Client: {e}")

TABLE = "Angel bot - website"

# ── Bảng quy đổi điểm ────────────────────────────────
TIER_POINTS = {
    "LT5": 10, "HT5": 15, "LT4": 20, "HT4": 25,
    "LT3": 30, "HT3": 40, "LT2": 50, "HT2": 60,
    "LT1": 70, "HT1": 80,
}

# ── Danh sách mode PvP (PHẢI khớp với mảng MODES trong index.html) ──
PVP_MODES = [
    "Sword", "Nethpot", "Pot", "UHC",
    "Axe", "Mace", "Smp", "Vanilla",
]


def calculate_points(tiers):
    """Tính tổng điểm từ dict tier {mode: tier_name}"""
    if not tiers or not isinstance(tiers, dict):
        return 0
    total = 0
    for mode, tier in tiers.items():
        clean = str(tier).strip().upper()
        total += TIER_POINTS.get(clean, 0)
    return total


def normalize_tiers(raw):
    """Chuẩn hóa dữ liệu tier về dạng dict {mode: tier}"""
    if not raw:
        return {}
    if isinstance(raw, dict):
        return {str(k).strip(): str(v).strip().upper() for k, v in raw.items() if str(k).strip() and str(v).strip()}
    if isinstance(raw, str):
        clean = raw.strip().upper()
        if clean in TIER_POINTS:
            return {"Tier": clean}
    if isinstance(raw, list):
        result = {}
        for item in raw:
            if isinstance(item, dict):
                for k, v in item.items():
                    if str(k).strip() and str(v).strip():
                        result[str(k).strip()] = str(v).strip().upper()
        return result
    return {}


def load_all_players():
    """Đọc TẤT CẢ player từ database"""
    if not supabase:
        return []
    try:
        resp = supabase.table(TABLE).select("*").order("points", desc=True).execute()
        return resp.data or []
    except Exception as e:
        print(f"Lỗi đọc dữ liệu: {e}")
        return []


def load_approved_players():
    """Chỉ đọc player đã được duyệt"""
    if not supabase:
        return []
    try:
        resp = (
            supabase.table(TABLE)
            .select("*")
            .eq("status", "approved")
            .order("points", desc=True)
            .execute()
        )
        return resp.data or []
    except Exception as e:
        print(f"Lỗi đọc dữ liệu approved: {e}")
        return []


def format_player(row):
    """Định dạng 1 row database thành dict chuẩn cho frontend"""
    tiers = normalize_tiers(row.get("tier"))
    ign = row.get("ign") or "Unknown"
    avatar = (
        row.get("avatar_url")
        or f"https://mc-heads.net/avatar/{ign}/100.png"
    )
    return {
        "id": row.get("id"),
        "name": ign,
        "avatar": avatar,
        "tiers": tiers,
        "points": row.get("points") or calculate_points(tiers),
        "status": row.get("status", "approved"),
        "review_note": row.get("review_note", ""),
        "discord_id": row.get("discord_id", ""),
        "created_at": row.get("created_at", ""),
        "updated_at": row.get("updated_at", ""),
    }


def notify_discord(message):
    """Gửi thông báo Discord qua webhook (server-side, không lộ ra client)"""
    try:
        requests.post(ADMIN_WEBHOOK_URL, json={"content": message}, timeout=5)
    except Exception as e:
        print(f"Không gửi được Discord: {e}")


def require_admin():
    """Kiểm tra admin đã đăng nhập chưa"""
    return bool(session.get("admin_authed"))


# Dữ liệu mẫu dự phòng (chỉ dùng khi DB trống/mất kết nối)
DEFAULT_PLAYERS = [
    {"name": "thekidpika", "tiers": {"Tier": "HT1"}},
    {"name": "AGL_Mipp", "tiers": {"Tier": "HT2"}},
]


# ═══════════════════════════════════════════════════════
#  PUBLIC API — Không cần xác thực
# ═══════════════════════════════════════════════════════

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """API public: Lấy bảng xếp hạng (chỉ player đã duyệt)"""
    rows = load_approved_players()
    if not rows:
        players = DEFAULT_PLAYERS
        leaderboard = []
        for p in players:
            tiers = p.get("tiers", {})
            leaderboard.append({
                "id": "", "name": p.get("name", "Unknown"),
                "avatar": p.get("avatar", f"https://mc-heads.net/avatar/{p.get('name','Steve')}/100.png"),
                "points": calculate_points(tiers), "tiers": tiers,
                "status": "approved", "review_note": "", "discord_id": "",
                "created_at": "", "updated_at": "",
            })
        return jsonify(leaderboard)

    return jsonify([format_player(r) for r in rows])


@app.route("/api/modes", methods=["GET"])
def get_modes():
    """API public: Danh sách mode PvP"""
    return jsonify(PVP_MODES)


@app.route("/api/tier-points", methods=["GET"])
def get_tier_points():
    """API public: Bảng quy đổi điểm tier"""
    return jsonify(TIER_POINTS)


@app.route("/api/register", methods=["POST"])
def register_player():
    """API public: Player đăng ký xét duyệt"""
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"ok": False, "error": "Thiếu tên Minecraft"}), 400

    # Kiểm tra tên đã tồn tại chưa
    if supabase:
        existing = (
            supabase.table(TABLE)
            .select("id")
            .eq("ign", name)
            .execute()
        )
        if existing.data and len(existing.data) > 0:
            return jsonify({"ok": False, "error": "Tên này đã được đăng ký"}), 409

    discord_id = str(data.get("discord_id", "")).strip()
    note = str(data.get("note", "")).strip()
    avatar_url = str(data.get("avatar_url", "")).strip() or f"https://mc-heads.net/avatar/{name}/100.png"
    selected_modes = data.get("modes", [])
    tiers = {}
    if isinstance(selected_modes, list):
        for mode_name in selected_modes:
            tiers[str(mode_name).strip()] = "Chưa xếp"

    record = {
        "ign": name,
        "tier": tiers if tiers else {"Tier": "Chưa xếp"},
        "status": "pending",
        "review_note": note,
        "discord_id": discord_id,
        "avatar_url": avatar_url,
        "points": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    if supabase:
        try:
            resp = supabase.table(TABLE).insert(record).execute()
            player = resp.data[0] if resp.data else None
        except Exception as e:
            return jsonify({"ok": False, "error": f"Lỗi database: {e}"}), 500
    else:
        player = record
        player["id"] = "local"

    notify_discord(
        f"📝 **AngelTier** — Player **{name}** vừa đăng ký xét duyệt."
    )

    return jsonify({"ok": True, "player": format_player(player) if player else None})


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    """API public: Xem trạng thái xét duyệt (ai cũng xem được)"""
    name_filter = request.args.get("name", "").strip().lower()
    status_filter = request.args.get("status", "all").strip()

    rows = load_all_players()
    players = [format_player(r) for r in rows]

    if name_filter:
        players = [p for p in players if name_filter in p["name"].lower()]
    if status_filter != "all":
        players = [p for p in players if p["status"] == status_filter]

    return jsonify(players)


# ═══════════════════════════════════════════════════════
#  ADMIN API — Cần xác thực 2 lớp
# ═══════════════════════════════════════════════════════

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
        notify_discord(
            "✅ **AngelTier** — Nhân viên kỹ thuật đăng nhập thành công."
        )
        return jsonify({"ok": True})
    else:
        session["admin_authed"] = False
        session["admin_step1_ok"] = False
        notify_discord(
            "🚨 **AngelTier** — CẢNH BÁO: Nhập sai mật khẩu lớp 2!"
        )
        return jsonify({"ok": False}), 401


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session["admin_authed"] = False
    session["admin_step1_ok"] = False
    return jsonify({"ok": True})


@app.route("/api/admin/players", methods=["GET"])
def admin_get_players():
    """Admin: Lấy TẤT CẢ player"""
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403
    rows = load_all_players()
    return jsonify({"ok": True, "players": [format_player(r) for r in rows]})


@app.route("/api/admin/players", methods=["POST"])
def admin_save_players():
    """
    Admin: Lưu toàn bộ danh sách (từ Bảng Điều Khiển -> nút "Lưu thay đổi").

    QUAN TRỌNG: người chơi ĐÃ có "id" sẽ được UPDATE theo id (khóa chính,
    luôn có ràng buộc UNIQUE mặc định trên Supabase). Người chơi CHƯA có
    "id" (mới thêm ở admin) sẽ được INSERT. Trước đây code dùng
    upsert(..., on_conflict="ign") cho TẤT CẢ bản ghi — nếu cột "ign"
    không có ràng buộc UNIQUE trong bảng Supabase (trường hợp thường gặp),
    Postgres từ chối toàn bộ upsert và không có gì được lưu, dù response
    trông như thành công. Tách update/insert như dưới đây không phụ thuộc
    vào ràng buộc đó nữa nên sẽ lưu được trong mọi trường hợp.
    """
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    data = request.get_json(silent=True) or {}
    players = data.get("players")
    if not isinstance(players, list):
        return jsonify({"ok": False, "error": "Dữ liệu không hợp lệ"}), 400

    if not supabase:
        return jsonify({"ok": False, "error": "Không có kết nối DB (Supabase chưa khởi tạo được)"}), 500

    to_update = []
    to_insert = []

    for p in players:
        if not isinstance(p, dict):
            continue
        name = str(p.get("name", "")).strip()
        if not name:
            continue
        tiers = normalize_tiers(p.get("tiers", {}))
        pts = p.get("points")
        if not isinstance(pts, (int, float)):
            pts = calculate_points(tiers)

        rec = {
            "ign": name,
            "tier": tiers if tiers else None,
            "avatar_url": p.get("avatar", ""),
            "discord_id": p.get("discord_id", ""),
            "points": pts,
            "status": p.get("status", "approved"),
            "review_note": p.get("review_note", ""),
            "updated_at": datetime.utcnow().isoformat(),
        }

        has_valid_id = p.get("id") and isinstance(p["id"], str) and len(p["id"]) > 10
        if has_valid_id:
            rec["id"] = p["id"]
            to_update.append(rec)
        else:
            rec["created_at"] = datetime.utcnow().isoformat()
            to_insert.append(rec)

    try:
        # Cập nhật người chơi đã tồn tại — xung đột theo "id" (khóa chính),
        # KHÔNG theo "ign", nên không cần ràng buộc UNIQUE trên "ign".
        if to_update:
            supabase.table(TABLE).upsert(to_update, on_conflict="id").execute()
        # Thêm người chơi hoàn toàn mới (chưa có id) — insert thẳng.
        if to_insert:
            supabase.table(TABLE).insert(to_insert).execute()
    except Exception as e:
        return jsonify({"ok": False, "error": f"Lỗi lưu: {e}"}), 500

    notify_discord(
        f"🛠️ **AngelTier** — Cập nhật {len(to_update)} người chơi, thêm mới {len(to_insert)} người chơi."
    )
    return jsonify({"ok": True, "count": len(to_update) + len(to_insert)})


@app.route("/api/admin/players/<player_id>", methods=["PUT"])
def admin_update_player(player_id):
    """Admin: Cập nhật 1 player theo ID"""
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    data = request.get_json(silent=True) or {}
    update_data = {"updated_at": datetime.utcnow().isoformat()}

    # Cho phép cập nhật các trường này
    allowed = ["ign", "tier", "avatar_url", "discord_id", "points", "status", "review_note"]
    for field in allowed:
        if field in data:
            update_data[field] = data[field]

    # Nếu đổi tier, tính lại điểm nếu chưa có points
    if "tier" in data and "points" not in data:
        tiers = normalize_tiers(data["tier"])
        update_data["points"] = calculate_points(tiers)

    if not supabase:
        return jsonify({"ok": False, "error": "Không có kết nối DB"}), 500

    # Nếu duyệt, tự động tính điểm
    if data.get("status") == "approved" and "points" not in data:
        tiers = normalize_tiers(data.get("tier", {}))
        if not tiers:
            # Lấy tier hiện tại từ DB
            current = supabase.table(TABLE).select("tier").eq("id", player_id).execute()
            if current.data:
                tiers = normalize_tiers(current.data[0].get("tier"))
        update_data["points"] = calculate_points(tiers)

    try:
        resp = (
            supabase.table(TABLE)
            .update(update_data)
            .eq("id", player_id)
            .execute()
        )
        if not resp.data:
            return jsonify({"ok": False, "error": "Không tìm thấy player"}), 404
        return jsonify({"ok": True, "player": format_player(resp.data[0])})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Lỗi cập nhật: {e}"}), 500


@app.route("/api/admin/players/<player_id>", methods=["DELETE"])
def admin_delete_player(player_id):
    """Admin: Xóa 1 player"""
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    if not supabase:
        return jsonify({"ok": False, "error": "Không có kết nối DB"}), 500

    try:
        # Lấy tên trước khi xóa để thông báo
        name_resp = supabase.table(TABLE).select("ign").eq("id", player_id).execute()
        player_name = name_resp.data[0]["ign"] if name_resp.data else "Unknown"

        resp = supabase.table(TABLE).delete().eq("id", player_id).execute()
        if not resp.data:
            return jsonify({"ok": False, "error": "Không tìm thấy player"}), 404

        notify_discord(
            f"🗑️ **AngelTier** — Đã xóa player **{player_name}** khỏi hệ thống."
        )
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Lỗi xóa: {e}"}), 500


@app.route("/api/admin/players/<player_id>/tier", methods=["POST"])
def admin_add_tier(player_id):
    """Admin: Thêm/cập nhật tier cho 1 mode"""
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    data = request.get_json(silent=True) or {}
    mode_name = str(data.get("mode", "")).strip()
    tier_name = str(data.get("tier", "")).strip().upper()
    if not mode_name or not tier_name:
        return jsonify({"ok": False, "error": "Thiếu mode hoặc tier"}), 400

    if not supabase:
        return jsonify({"ok": False, "error": "Không có kết nối DB"}), 500

    try:
        # Lấy tier hiện tại
        resp = supabase.table(TABLE).select("tier, ign").eq("id", player_id).execute()
        if not resp.data:
            return jsonify({"ok": False, "error": "Không tìm thấy player"}), 404

        current_tiers = normalize_tiers(resp.data[0].get("tier"))
        current_tiers[mode_name] = tier_name
        pts = calculate_points(current_tiers)

        update_resp = (
            supabase.table(TABLE)
            .update({
                "tier": current_tiers,
                "points": pts,
                "updated_at": datetime.utcnow().isoformat(),
            })
            .eq("id", player_id)
            .execute()
        )

        return jsonify({"ok": True, "player": format_player(update_resp.data[0])})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Lỗi: {e}"}), 500


@app.route("/api/admin/players/<player_id>/tier", methods=["DELETE"])
def admin_remove_tier(player_id):
    """Admin: Xóa tier của 1 mode"""
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    data = request.get_json(silent=True) or {}
    mode_name = str(data.get("mode", "")).strip()
    if not mode_name:
        return jsonify({"ok": False, "error": "Thiếu mode"}), 400

    if not supabase:
        return jsonify({"ok": False, "error": "Không có kết nối DB"}), 500

    try:
        resp = supabase.table(TABLE).select("tier").eq("id", player_id).execute()
        if not resp.data:
            return jsonify({"ok": False, "error": "Không tìm thấy player"}), 404

        current_tiers = normalize_tiers(resp.data[0].get("tier"))
        current_tiers.pop(mode_name, None)
        pts = calculate_points(current_tiers)

        update_resp = (
            supabase.table(TABLE)
            .update({
                "tier": current_tiers if current_tiers else None,
                "points": pts,
                "updated_at": datetime.utcnow().isoformat(),
            })
            .eq("id", player_id)
            .execute()
        )

        return jsonify({"ok": True, "player": format_player(update_resp.data[0])})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Lỗi: {e}"}), 500


@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():
    """Admin: Thống kê tổng quan"""
    if not require_admin():
        return jsonify({"ok": False, "error": "Chưa xác thực"}), 403

    rows = load_all_players()
    total = len(rows)
    pending = sum(1 for r in rows if r.get("status") == "pending")
    approved = sum(1 for r in rows if r.get("status") == "approved")
    rejected = sum(1 for r in rows if r.get("status") == "rejected")
    total_points = sum(r.get("points", 0) or 0 for r in rows)

    # Phân bố tier
    tier_dist = {}
    for r in rows:
        tiers = normalize_tiers(r.get("tier"))
        for mode, t in tiers.items():
            if t in TIER_POINTS:
                tier_dist[t] = tier_dist.get(t, 0) + 1

    return jsonify({
        "ok": True,
        "stats": {
            "total": total, "pending": pending,
            "approved": approved, "rejected": rejected,
            "total_points": total_points,
            "tier_distribution": tier_dist,
        }
    })


# ═══════════════════════════════════════════════════════
#  TRANG CHỦ
# ═══════════════════════════════════════════════════════

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    print("🔥 Server AngelTier đang chạy tại http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
