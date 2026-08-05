#code 004
from flask import Flask, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# 📊 Bảng quy đổi điểm số Tier
TIER_POINTS = {
    'LT5': 10,
    'HT5': 15,
    'LT4': 20,
    'HT4': 25,
    'LT3': 30,
    'HT3': 40,
    'LT2': 50,
    'HT2': 60,
    'LT1': 70,
    'HT1': 80
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


DEFAULT_PLAYERS = [
    {"name": "AGL_Mipp", "avatar": "https://mc-heads.net/avatar/AGL_Mipp/60.png", "tiers": {"Sword": "HT1", "Nethpot": "HT2"}},
    {"name": "Ag_qkhang", "avatar": "https://mc-heads.net/avatar/Ag_qkhang/60.png", "tiers": {"Sword": "HT2", "Nethpot": "HT3"}},
    {"name": "Uchiha_nho", "avatar": "https://mc-heads.net/avatar/Uchiha_nho/60.png", "tiers": {"Sword": "HT3", "Pot": "HT3"}},
    {"name": "anh5me27051", "avatar": "https://mc-heads.net/avatar/anh5me27051/60.png", "tiers": {"Sword": "HT1", "Nethpot": "HT2"}},
    {"name": "LikedaeMC", "avatar": "https://mc-heads.net/avatar/LikedaeMC/60.png", "tiers": {"Sword": "HT2", "Nethpot": "HT3"}},
    {"name": "Chuyenn", "avatar": "https://mc-heads.net/avatar/Chuyenn/60.png", "tiers": {"Sword": "HT3", "Pot": "HT3"}},
    {"name": "NeoReo_", "avatar": "https://mc-heads.net/avatar/NeoReo_/60.png", "tiers": {"Sword": "HT2", "Axe": "HT2"}},
    {"name": "Vandekynang22", "avatar": "https://mc-heads.net/avatar/Vandekynang22/60.png", "tiers": {"Sword": "HT3", "Smp": "HT2"}},
    {"name": "FoxXinhGai", "avatar": "https://mc-heads.net/avatar/FoxXinhGai/60.png", "tiers": {"Sword": "HT4", "Vanilla": "HT3"}}
]


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    raw_players = load_real_players()
    if raw_players is None:
        raw_players = DEFAULT_PLAYERS

    leaderboard = []
    for p in raw_players:
        tiers = p.get("tiers", {})
        pts = calculate_points(tiers)
        tier_display = [f"{m}: {t}" for m, t in tiers.items()]
        leaderboard.append({
            "id": p.get("id", ""),
            "name": p.get("name", "Unknown"),
            "avatar": p.get("avatar", f"https://mc-heads.net/avatar/{p.get('name', 'Steve')}/60.png"),
            "points": pts,
            "tiers": tiers,
            "tier_display": tier_display
        })

    # 🏆 SẮP XẾP GIẢM DẦN THEO POINT (Ai cao điểm nhất đứng Top)
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    return jsonify(leaderboard)


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AngelTier — Bảng Xếp Hạng PvP Việt Nam</title>
<meta name="description" content="AngelTier — nơi kỹ năng PvP Minecraft được tôi luyện qua lửa và phán xét bởi hệ thống Tier công tâm nhất Việt Nam.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cdefs%3E%3ClinearGradient id='f' x1='0' y1='1' x2='0' y2='0'%3E%3Cstop offset='0' stop-color='%237a1608'/%3E%3Cstop offset='.55' stop-color='%23ff7a29'/%3E%3Cstop offset='1' stop-color='%23f7c873'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M100,42 C78,76 68,104 100,142 C132,104 122,76 100,42 Z' fill='url(%23f)'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Teko:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{
  --void:#030106;
  --void-2:#0a0512;
  --panel:#0f0818;
  --panel-2:#171025;
  --line: rgba(247,200,115,0.10);
  --line-soft: rgba(255,255,255,0.055);
  --gold:#f7c873;
  --gold-deep:#c98f3e;
  --fire:#ff7a29;
  --fire-hot:#ff4519;
  --fire-deep:#7a1608;
  --celestial:#8ec9ff;
  --celestial-soft: rgba(142,201,255,0.5);
  --celestial-deep:#3f6fa8;
  --feather:#f5efe4;
  --text:#f4eee2;
  --text-dim:#ab9fb4;
  --text-mute:#6c6178;
  --r-lg:18px;
  --r-md:12px;
  --r-sm:8px;
}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  background:
    radial-gradient(ellipse 900px 500px at 50% -10%, rgba(255,122,41,0.14), transparent 60%),
    radial-gradient(ellipse 700px 400px at 90% 20%, rgba(142,201,255,0.05), transparent 60%),
    radial-gradient(ellipse 700px 400px at 5% 60%, rgba(247,200,115,0.05), transparent 60%),
    var(--void);
  color:var(--text);
  font-family:'Manrope',sans-serif;
  min-height:100vh;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
::selection{background:rgba(255,122,41,0.35);color:#fff;}
::-webkit-scrollbar{width:10px;}
::-webkit-scrollbar-track{background:var(--void);}
::-webkit-scrollbar-thumb{background:linear-gradient(var(--gold-deep),var(--fire-deep));border-radius:10px;}

.display{font-family:'Teko',sans-serif;font-weight:600;letter-spacing:0.5px;}
.mono{font-family:'JetBrains Mono',monospace;}
.mythic{font-family:'Cinzel',serif;}

a,button,input,textarea{font-family:inherit;}
:focus-visible{outline:2px solid var(--celestial);outline-offset:3px;border-radius:4px;}

.container{max-width:1120px;margin:0 auto;padding:0 20px;position:relative;z-index:2;}

/* ===================================================== */
/*  CUSTOM CURSOR                                          */
/* ===================================================== */
body.has-fine-pointer, body.has-fine-pointer a, body.has-fine-pointer button,
body.has-fine-pointer .player-row, body.has-fine-pointer .mode-card,
body.has-fine-pointer .faq-item, body.has-fine-pointer .rk-tab,
body.has-fine-pointer .lb-filter, body.has-fine-pointer .logo{
  cursor:none;
}
#cursor-dot,#cursor-ring{
  position:fixed;top:0;left:0;pointer-events:none;z-index:10000;
  border-radius:50%;transform:translate3d(-100px,-100px,0);will-change:transform;
}
#cursor-dot{
  width:6px;height:6px;background:var(--gold);
  box-shadow:0 0 8px 2px rgba(247,200,115,0.65);
  transition:background-color .25s, box-shadow .25s;
}
#cursor-ring{
  width:34px;height:34px;margin:-17px 0 0 -17px;
  border:1.4px solid rgba(247,200,115,0.55);
  background:radial-gradient(circle, rgba(255,122,41,0.08), transparent 70%);
  transition:width .28s cubic-bezier(.2,.8,.2,1), height .28s cubic-bezier(.2,.8,.2,1),
             margin .28s cubic-bezier(.2,.8,.2,1), border-color .28s, background .28s, opacity .2s;
}
#cursor-ring.hover{
  width:56px;height:56px;margin:-28px 0 0 -28px;
  border-color:rgba(142,201,255,0.75);
  background:radial-gradient(circle, rgba(142,201,255,0.14), transparent 72%);
}
#cursor-dot.hover{background:var(--celestial);box-shadow:0 0 10px 3px rgba(142,201,255,0.7);}
#cursor-ring.click{width:26px;height:26px;margin:-13px 0 0 -13px;}
body:not(.has-fine-pointer) #cursor-dot,body:not(.has-fine-pointer) #cursor-ring{display:none;}

/* ===================================================== */
/*  INTRO / IGNITION LOADER                                */
/* ===================================================== */
#loader{
  position:fixed;inset:0;z-index:99999;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;
  background:
    radial-gradient(ellipse 700px 500px at 50% 45%, rgba(255,122,41,0.16), transparent 65%),
    var(--void);
  transition:opacity .7s ease, visibility .7s ease;
}
#loader.exit{opacity:0;visibility:hidden;}
#loader .sigil-mark{width:104px;height:104px;filter:drop-shadow(0 0 26px rgba(255,122,41,0.35));}
#loader-word{
  font-family:'Cinzel',serif;font-weight:700;font-size:20px;letter-spacing:7px;
  color:var(--feather);opacity:0;animation:loaderFade .6s .5s ease forwards;
}
#loader-bar-wrap{
  width:220px;height:2px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;
  opacity:0;animation:loaderFade .6s .7s ease forwards;
}
#loader-bar{width:0%;height:100%;background:linear-gradient(90deg,var(--gold),var(--fire));transition:width .2s linear;}
#loader-status{
  font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:2px;color:var(--text-mute);
  opacity:0;animation:loaderFade .6s .8s ease forwards;text-transform:uppercase;
}
@keyframes loaderFade{to{opacity:1;}}
body.loading{overflow:hidden;}

/* ===================================================== */
/*  SIGIL — signature emblem (shared symbol)                */
/* ===================================================== */
.sigil-mark{display:block;overflow:visible;}
.sigil-tick{transform-origin:100px 90px;}
.sigil-feather{transform-origin:0 0;}
.sigil-flame,.sigil-core{transform-origin:100px 150px;}

#loader .sigil-tick{stroke-dasharray:16;stroke-dashoffset:16;opacity:0;
  animation:tickDraw .5s cubic-bezier(.2,.8,.2,1) forwards;}
#loader .sigil-feather{opacity:0;transform:scale(0.4);
  animation:featherGrow .55s cubic-bezier(.2,.8,.2,1) forwards;}
#loader .sigil-flame,#loader .sigil-core{opacity:0;transform:scale(0.5);
  animation:flameGrow .6s cubic-bezier(.2,.8,.2,1) forwards;}
@keyframes tickDraw{to{stroke-dashoffset:0;opacity:1;}}
@keyframes featherGrow{to{opacity:1;transform:scale(1);}}
@keyframes flameGrow{to{opacity:1;transform:scale(1);}}
#loader .sigil-tick:nth-child(1){animation-delay:.02s;}
#loader .sigil-tick:nth-child(2){animation-delay:.06s;}
#loader .sigil-tick:nth-child(3){animation-delay:.10s;}
#loader .sigil-tick:nth-child(4){animation-delay:.14s;}
#loader .sigil-tick:nth-child(5){animation-delay:.18s;}
#loader .sigil-tick:nth-child(6){animation-delay:.22s;}
#loader .sigil-tick:nth-child(7){animation-delay:.26s;}
#loader .sigil-tick:nth-child(8){animation-delay:.30s;}
#loader .sigil-tick:nth-child(9){animation-delay:.34s;}
#loader .sigil-tick:nth-child(10){animation-delay:.38s;}
#loader .wing-r{animation-delay:.30s;}
#loader .wing-l{animation-delay:.30s;}
#loader .sigil-flame{animation-delay:.55s;}
#loader .sigil-core{animation-delay:.68s;animation-name:flameGrow, coreFlicker;animation-duration:.6s,2.4s;animation-delay:.68s,1.3s;animation-iteration-count:1,infinite;animation-timing-function:cubic-bezier(.2,.8,.2,1),ease-in-out;}
@keyframes coreFlicker{0%,100%{opacity:.85;}50%{opacity:1;}}

.sigil-mark.ambient .sigil-flame{animation:coreFlicker 3s ease-in-out infinite;}
.sigil-mark.ambient .sigil-core{animation:coreFlicker 2.4s ease-in-out infinite reverse;}

/* ===== HEADER ===== */
header{
  position:sticky;top:0;z-index:50;
  backdrop-filter:blur(14px);
  background:rgba(3,1,6,0.72);
  border-bottom:1px solid var(--line-soft);
}
header .container{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;}
.logo{display:flex;align-items:center;gap:11px;text-decoration:none;cursor:pointer;background:none;border:none;}
.logo .sigil-mark{width:32px;height:32px;}
.logo-text{
  font-family:'Cinzel',serif;font-weight:700;font-size:18px;letter-spacing:2.5px;
  background:linear-gradient(90deg,#e9e4da 0%,#c9c2b4 40%, var(--gold) 62%, var(--fire) 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.nav-links{display:flex;gap:8px;list-style:none;align-items:center;}
.nav-links a{
  color:var(--text-dim);text-decoration:none;font-size:13px;font-weight:600;cursor:pointer;
  padding:9px 14px;border-radius:8px;transition:.25s;letter-spacing:.2px;
}
.nav-links a:hover{color:#fff;background:rgba(255,122,41,0.08);}
.nav-links a.cta{
  color:#1a0e05;background:linear-gradient(90deg,var(--gold),var(--fire));
  font-weight:700;box-shadow:0 4px 18px rgba(255,110,30,0.28);
}
.nav-links a.cta:hover{filter:brightness(1.08);background:linear-gradient(90deg,var(--gold),var(--fire));}

.view-section{display:none;}
.view-section.active{display:block;}

/* ===== EMBERS ===== */
.ember-field{position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:0;}
.ember{
  position:absolute;bottom:-10px;border-radius:50%;
  background:radial-gradient(circle,#ffdca0 0%, var(--fire) 55%, transparent 75%);
  opacity:0;
  animation:rise linear infinite;
  filter:blur(0.2px);
}
.ember.spark{background:radial-gradient(circle,#fff 0%, var(--celestial) 55%, transparent 75%);}
@keyframes rise{
  0%{transform:translateY(0) translateX(0) scale(1);opacity:0;}
  8%{opacity:.9;}
  50%{transform:translateY(-260px) translateX(var(--drift,18px)) scale(0.8);}
  92%{opacity:.5;}
  100%{transform:translateY(-540px) translateX(calc(var(--drift,18px) * 2)) scale(0.2);opacity:0;}
}
.cursor-spark{position:fixed;width:4px;height:4px;border-radius:50%;pointer-events:none;z-index:9999;
  background:radial-gradient(circle,#ffe3ae,var(--fire) 70%,transparent 100%);
  animation:sparkFade .7s ease-out forwards;}
@keyframes sparkFade{to{transform:translateY(-26px) scale(0.2);opacity:0;}}

/* ===== HERO ===== */
.hero{position:relative;padding:70px 0 46px;text-align:center;}
.hero-glow{
  position:absolute;left:50%;top:6%;transform:translateX(-50%);
  width:600px;height:600px;border-radius:50%;
  background:radial-gradient(circle, rgba(255,122,41,0.22) 0%, rgba(255,122,41,0.06) 45%, transparent 72%);
  filter:blur(10px);z-index:0;animation:pulse-glow 5s ease-in-out infinite;
}
@keyframes pulse-glow{0%,100%{opacity:.75;transform:translateX(-50%) scale(1);}50%{opacity:1;transform:translateX(-50%) scale(1.08);}}
.hero-tag{
  position:relative;z-index:2;
  font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
  color:var(--gold);background:rgba(247,200,115,0.08);
  border:1px solid rgba(247,200,115,0.25);
  padding:7px 16px;border-radius:30px;display:inline-block;margin-bottom:30px;
  opacity:0;animation:reveal .7s .05s ease forwards;
}
.hero-sigil-wrap{position:relative;z-index:2;display:flex;justify-content:center;
  opacity:0;animation:reveal .8s .15s ease forwards;}
.hero-sigil-wrap .sigil-mark{width:min(150px,32vw);height:min(150px,32vw);
  filter:drop-shadow(0 0 40px rgba(255,122,41,0.35)) drop-shadow(0 0 90px rgba(255,90,20,0.16));}
.hero-word{
  position:relative;z-index:2;margin-top:18px;
  font-family:'Cinzel',serif;font-weight:700;font-size:clamp(34px,7vw,56px);letter-spacing:9px;
  background:linear-gradient(90deg,#e9e4da 0%,#c9c2b4 35%, var(--gold) 58%, var(--fire) 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  opacity:0;animation:reveal .8s .25s ease forwards;
}
.hero-sub{
  position:relative;z-index:2;
  font-size:10.5px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
  color:var(--text-mute);margin-top:12px;
  opacity:0;animation:reveal .7s .35s ease forwards;
}
.hero p.lead{
  position:relative;z-index:2;color:var(--text-dim);font-size:14.5px;max-width:600px;
  margin:20px auto 30px;line-height:1.7;
  opacity:0;animation:reveal .7s .45s ease forwards;
}
@keyframes reveal{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
.hero-btns{position:relative;z-index:2;display:flex;justify-content:center;gap:14px;flex-wrap:wrap;
  opacity:0;animation:reveal .7s .55s ease forwards;}
.btn{
  border:none;cursor:pointer;font-family:'Manrope',sans-serif;
  padding:13px 26px;border-radius:11px;font-size:13.5px;font-weight:700;
  display:inline-flex;align-items:center;gap:8px;text-decoration:none;letter-spacing:.2px;
  transition:transform .25s, box-shadow .25s, filter .25s;
}
.btn-fire{
  color:#1c0d04;background:linear-gradient(90deg,var(--gold) 0%, var(--fire) 100%);
  box-shadow:0 8px 26px rgba(255,110,30,0.32);
  position:relative;overflow:hidden;
}
.btn-fire::after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(120deg,transparent 30%,rgba(255,255,255,.55) 48%,transparent 66%);
  transform:translateX(-120%);transition:transform .6s;
}
.btn-fire:hover::after{transform:translateX(120%);}
.btn-fire:hover{transform:translateY(-2px);box-shadow:0 12px 32px rgba(255,110,30,0.42);}
.btn-ghost{
  color:var(--text);background:var(--panel);border:1px solid var(--line-soft);
}
.btn-ghost:hover{border-color:rgba(142,201,255,0.4);transform:translateY(-2px);background:var(--panel-2);}

/* ===== WING DIVIDER ===== */
.wing-divider{display:flex;align-items:center;justify-content:center;gap:14px;margin:6px 0 34px;opacity:0;}
.wing-divider svg{opacity:.55;}
.wing-orb{
  width:7px;height:7px;border-radius:50%;
  background:radial-gradient(circle,#fff,var(--fire) 60%,transparent 100%);
  box-shadow:0 0 12px 3px rgba(255,122,41,0.55);
}

/* ===== reveal-on-scroll ===== */
.reveal{opacity:0;transform:translateY(22px);transition:opacity .7s ease, transform .7s ease;}
.reveal.in{opacity:1;transform:translateY(0);}

/* ===== CARD BASE ===== */
.card{
  background:linear-gradient(160deg, var(--panel) 0%, var(--void-2) 130%);
  border:1px solid var(--line-soft);
  border-radius:var(--r-lg);
  position:relative;
  transition:border-color .3s;
}
.card::before{
  content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;
  background:linear-gradient(160deg, rgba(247,200,115,0.18), transparent 40%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;
}

/* ===== TIER FLAME LADDER ===== */
.tier-card{padding:28px;margin-bottom:28px;}
.tier-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:22px;gap:16px;flex-wrap:wrap;}
.tier-eyebrow{font-size:10.5px;font-weight:700;letter-spacing:2px;color:var(--fire);text-transform:uppercase;}
.tier-title{font-family:'Cinzel',serif;font-size:21px;font-weight:600;color:#fff;margin-top:6px;}
.tier-badge{
  background:var(--panel-2);border:1px solid var(--line-soft);color:var(--gold);
  padding:6px 14px;border-radius:20px;font-size:11.5px;font-weight:700;font-family:'JetBrains Mono',monospace;
}
.flame-ladder{
  display:flex;align-items:flex-end;justify-content:space-between;gap:6px;
  height:170px;padding:0 4px 0;border-bottom:1px solid var(--line-soft);margin-bottom:10px;
}
.flame-col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:8px;}
.flame-bar{
  width:100%;max-width:38px;border-radius:9px 9px 4px 4px;
  transform-origin:bottom;transform:scaleY(0);transition:transform 1s cubic-bezier(.2,.8,.2,1);
  position:relative;
}
.flame-ladder.in .flame-bar{transform:scaleY(1);}
.flame-bar.t5{background:linear-gradient(180deg,#bfe9ff,#5eb8dd);box-shadow:0 0 10px rgba(94,184,221,.4);}
.flame-bar.t4{background:linear-gradient(180deg,#ffe9ad,#e8b95a);box-shadow:0 0 10px rgba(232,185,90,.4);}
.flame-bar.t3{background:linear-gradient(180deg,#ffcf7a,#f0982e);box-shadow:0 0 12px rgba(240,152,46,.45);}
.flame-bar.t2{background:linear-gradient(180deg,#ffb15e,var(--fire));box-shadow:0 0 14px rgba(255,122,41,.5);}
.flame-bar.t1{background:linear-gradient(180deg,#ffd27a,var(--fire-hot));box-shadow:0 0 22px rgba(255,69,25,.65);animation:flicker 2.4s ease-in-out infinite;}
@keyframes flicker{0%,100%{filter:brightness(1);}50%{filter:brightness(1.18);}}
.flame-label{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;color:var(--text-mute);letter-spacing:.5px;}
.flame-col.hi .flame-label{color:var(--gold);}
.tier-desc{font-size:12.5px;color:var(--text-dim);line-height:1.6;}

/* ===== LEADERBOARD (home top3) ===== */
.lb-box{padding:26px;margin-bottom:28px;}
.lb-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-wrap:wrap;gap:12px;}
.lb-live{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;letter-spacing:1px;color:#ff5555;text-transform:uppercase;}
.lb-dot{width:6px;height:6px;border-radius:50%;background:#ff3d3d;box-shadow:0 0 8px #ff3d3d;animation:blink 1.6s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.25;}}
.lb-title{font-family:'Cinzel',serif;font-size:16.5px;font-weight:600;color:#fff;margin-top:3px;letter-spacing:.5px;}
.lb-filter{
  background:var(--panel-2);border:1px solid var(--line-soft);color:var(--text);
  padding:9px 18px;border-radius:9px;font-size:12.5px;font-weight:700;cursor:pointer;transition:.2s;
}
.lb-filter:hover{border-color:var(--celestial);color:var(--celestial);}

.player-row{
  background:var(--panel-2);border:1px solid var(--line-soft);border-radius:11px;
  padding:13px 18px;display:flex;align-items:center;justify-content:space-between;
  margin-bottom:9px;transition:.25s;position:relative;overflow:hidden;
}
.player-row:hover{border-color:rgba(247,200,115,0.3);transform:translateX(3px);background:#1a1324;}
.player-row.top1{border-color:rgba(255,122,41,0.45);background:linear-gradient(90deg,rgba(255,122,41,0.09),var(--panel-2) 55%);}
.player-left{display:flex;align-items:center;gap:14px;}
.rank-chip{
  font-family:'Teko',sans-serif;font-size:20px;font-weight:600;color:var(--text-mute);min-width:30px;text-align:center;
}
.rank-chip.medal{color:var(--gold);}
.avatar{
  width:34px;height:34px;border-radius:8px;background:var(--void-2);object-fit:cover;
  border:1px solid var(--line-soft);
}
.player-row.top1 .avatar{border-color:var(--fire);box-shadow:0 0 12px rgba(255,122,41,0.4);}
.player-name{font-size:13.5px;font-weight:700;color:#fff;}
.player-points{font-size:12.5px;color:var(--gold);font-weight:700;font-family:'JetBrains Mono',monospace;}

/* ===== MODES GRID ===== */
.section-eyebrow{font-size:10.5px;font-weight:700;color:var(--fire);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.section-heading{font-family:'Cinzel',serif;font-size:19px;font-weight:600;color:#fff;margin-bottom:22px;letter-spacing:.4px;}
.modes-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:44px;}
.mode-card{
  padding:24px 14px;display:flex;flex-direction:column;align-items:center;gap:13px;
  cursor:pointer;transition:.28s;text-align:center;
}
.mode-card:hover{transform:translateY(-4px);border-color:rgba(142,201,255,0.4);}
.mode-card:hover .mode-icon{transform:scale(1.08);filter:drop-shadow(0 0 10px rgba(255,122,41,.5));}
.mode-icon{width:38px;height:38px;transition:.3s;}
.mode-name{font-size:11.5px;font-weight:800;color:var(--text);letter-spacing:1px;}

/* ===== STATS ===== */
.stats-section{text-align:center;margin:44px 0;padding:40px 24px;}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;max-width:760px;margin:26px auto 0;}
.stat-box{background:var(--panel-2);border:1px solid var(--line-soft);border-radius:13px;padding:22px 14px;}
.stat-box h2{font-family:'Teko',sans-serif;font-size:40px;font-weight:700;
  background:linear-gradient(90deg,var(--gold),var(--fire));-webkit-background-clip:text;background-clip:text;color:transparent;
  margin-bottom:4px;}
.stat-box p{font-size:11.5px;color:var(--text-dim);font-weight:600;letter-spacing:.3px;}

/* ===== PROCESS TIMELINE ===== */
.flow-section{padding:38px 26px;margin:44px 0;text-align:center;}
.timeline{max-width:640px;margin:30px auto 0;text-align:left;position:relative;}
.timeline::before{
  content:"";position:absolute;left:19px;top:6px;bottom:6px;width:2px;
  background:linear-gradient(var(--gold), var(--fire) 60%, transparent);
}
.tl-step{display:flex;gap:20px;padding-bottom:26px;position:relative;}
.tl-step:last-child{padding-bottom:0;}
.tl-num{
  width:40px;height:40px;min-width:40px;border-radius:50%;
  background:var(--panel-2);border:1px solid var(--line-soft);
  display:flex;align-items:center;justify-content:center;
  font-family:'Teko',sans-serif;font-size:19px;font-weight:600;color:var(--gold);
  position:relative;z-index:1;
}
.tl-step.active .tl-num{background:linear-gradient(145deg,var(--gold),var(--fire));color:#1a0d04;box-shadow:0 0 16px rgba(255,122,41,.5);}
.tl-name{font-size:15.5px;font-weight:800;color:#fff;margin-bottom:5px;}
.tl-desc{font-size:12.5px;color:var(--text-dim);line-height:1.6;max-width:480px;}

/* ===== FAQ ===== */
.faq-section{margin-top:44px;}
.faq-item{
  background:var(--panel);border:1px solid var(--line-soft);border-radius:13px;
  margin-bottom:11px;overflow:hidden;cursor:pointer;transition:.2s;
}
.faq-item:hover{border-color:rgba(142,201,255,0.3);}
.faq-q{padding:18px 22px;display:flex;justify-content:space-between;align-items:center;font-size:13.5px;font-weight:700;color:#fff;gap:14px;}
.faq-q .arrow{transition:.3s;color:var(--fire);min-width:14px;}
.faq-item.active .arrow{transform:rotate(45deg);}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease, padding .35s ease;padding:0 22px;font-size:12.5px;color:var(--text-dim);line-height:1.7;}
.faq-item.active .faq-a{max-height:220px;padding:0 22px 20px;}

/* ===== FOOTER ===== */
footer{margin-top:60px;padding:40px 0 34px;border-top:1px solid var(--line-soft);display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;}
.footer-brand p{font-size:12.5px;color:var(--text-dim);line-height:1.7;margin-top:12px;max-width:320px;}
.footer-col h4{font-size:12.5px;font-weight:800;color:#fff;margin-bottom:15px;letter-spacing:1px;text-transform:uppercase;}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:11px;}
.footer-col ul a{color:var(--text-dim);text-decoration:none;font-size:12.5px;cursor:pointer;transition:.2s;}
.footer-col ul a:hover{color:var(--fire);}
.footer-bottom{margin-top:30px;padding-top:20px;border-top:1px solid var(--line-soft);font-size:11.5px;color:var(--text-mute);text-align:center;grid-column:1/-1;}

/* ===== RANKING VIEW ===== */
.rk-header{margin-bottom:24px;}
.rk-title{font-family:'Cinzel',serif;font-size:26px;font-weight:700;color:#fff;letter-spacing:1px;}
.rk-sub{font-size:13px;color:var(--text-dim);margin-top:6px;}
.rk-tabs{display:flex;gap:10px;overflow-x:auto;padding-bottom:14px;border-bottom:1px solid var(--line-soft);margin-bottom:22px;scrollbar-width:thin;}
.rk-tab{
  display:flex;align-items:center;gap:8px;background:var(--panel-2);border:1px solid var(--line-soft);
  padding:9px 16px;border-radius:10px;cursor:pointer;opacity:.65;transition:.2s;white-space:nowrap;font-size:11.5px;font-weight:700;color:#fff;
}
.rk-tab.active,.rk-tab:hover{opacity:1;border-color:var(--fire);background:rgba(255,122,41,0.08);}
.rk-view-card{padding:26px;margin-bottom:30px;}
.rk-table-wrap{width:100%;overflow-x:auto;}
.rk-table{width:100%;border-collapse:collapse;min-width:680px;}
.rk-table th{text-align:left;font-size:11px;font-weight:700;color:var(--text-mute);padding:12px 12px;border-bottom:1px solid var(--line-soft);letter-spacing:1px;text-transform:uppercase;}
.rk-table td{padding:14px 12px;border-bottom:1px solid var(--line-soft);font-size:13.5px;vertical-align:middle;}
.rk-table tr:hover td{background:rgba(255,122,41,0.03);}
.tiers-wrap{display:flex;flex-wrap:wrap;gap:6px;max-width:420px;}
.tier-chip{
  display:flex;align-items:center;gap:5px;background:var(--panel-2);border:1px solid var(--line-soft);
  border-radius:7px;padding:5px 10px;font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:700;color:#7fd4ff;
}
.tier-chip.match{color:var(--gold);border-color:rgba(247,200,115,0.35);background:rgba(247,200,115,0.06);}
.empty-state{padding:50px 10px;text-align:center;color:var(--text-mute);font-size:13px;}

@media(max-width:860px){
  .modes-grid{grid-template-columns:repeat(2,1fr);}
  .stats-grid{grid-template-columns:1fr;}
  footer{grid-template-columns:1fr;gap:26px;}
}
@media(max-width:600px){
  .nav-links a:not(.cta){display:none;}
  .hero-word{letter-spacing:5px;}
  .flame-ladder{height:130px;}
}
@media(prefers-reduced-motion:reduce){
  .ember,.hero-glow,.flame-bar.t1,.lb-dot,.sigil-mark.ambient .sigil-flame,.sigil-mark.ambient .sigil-core{animation:none !important;}
  .reveal{transition:none;}
}
</style>
</head>
<body class="loading">

<!-- ============ CUSTOM CURSOR ============ -->
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>

<!-- ============ SHARED SIGIL SYMBOL ============ -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <linearGradient id="tickGradT5" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bfe9ff"/><stop offset="1" stop-color="#5eb8dd"/></linearGradient>
    <linearGradient id="tickGradT4" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe9ad"/><stop offset="1" stop-color="#e8b95a"/></linearGradient>
    <linearGradient id="tickGradT3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffcf7a"/><stop offset="1" stop-color="#f0982e"/></linearGradient>
    <linearGradient id="tickGradT2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffb15e"/><stop offset="1" stop-color="#ff7a29"/></linearGradient>
    <linearGradient id="tickGradT1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#ff4519"/></linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#c98f3e"/><stop offset="1" stop-color="#ff7a29"/></linearGradient>
    <linearGradient id="flameGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#7a1608"/><stop offset=".55" stop-color="#ff7a29"/><stop offset="1" stop-color="#f7c873"/>
    </linearGradient>
    <radialGradient id="coreGrad" cx="0.5" cy="0.4" r="0.65">
      <stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#8ec9ff"/><stop offset="1" stop-color="#3f6fa8" stop-opacity="0"/>
    </radialGradient>

    <g id="sigil-wing">
      <path class="sigil-feather" d="M0,0 C20,-13 46,-13 72,-2 C50,1 30,4 12,10 C7,6 3,3 0,0 Z" fill="url(#wingGrad)" opacity="0.55" transform="rotate(-30)"/>
      <path class="sigil-feather" d="M0,0 C22,-10 50,-8 80,0 C56,3 34,6 15,11 C8,7 3,3 0,0 Z" fill="url(#wingGrad)" opacity="0.7" transform="rotate(-14)"/>
      <path class="sigil-feather" d="M0,0 C24,-6 54,-2 86,4 C60,6 36,8 16,12 C9,8 4,4 0,0 Z" fill="url(#wingGrad)" opacity="0.85" transform="rotate(2)"/>
      <path class="sigil-feather" d="M0,0 C22,-2 50,4 78,12 C54,10 32,10 14,13 C7,9 3,4 0,0 Z" fill="var(--fire)" opacity="0.9" transform="rotate(18)"/>
      <path class="sigil-feather" d="M0,0 C18,2 40,10 62,20 C42,14 24,13 10,14 C5,10 2,5 0,0 Z" fill="var(--fire-hot)" opacity="0.95" transform="rotate(34)"/>
    </g>

    <symbol id="sigil" viewBox="0 0 200 200">
      <g class="sigil-ticks">
        <line class="sigil-tick" x1="100" y1="16" x2="100" y2="27" stroke="url(#tickGradT5)" stroke-width="2" stroke-linecap="round" transform="rotate(-75 100 90)"/>
        <line class="sigil-tick" x1="100" y1="15" x2="100" y2="27" stroke="url(#tickGradT5)" stroke-width="2.3" stroke-linecap="round" transform="rotate(-58.3 100 90)"/>
        <line class="sigil-tick" x1="100" y1="14" x2="100" y2="27" stroke="url(#tickGradT4)" stroke-width="2.6" stroke-linecap="round" transform="rotate(-41.6 100 90)"/>
        <line class="sigil-tick" x1="100" y1="13" x2="100" y2="27" stroke="url(#tickGradT4)" stroke-width="2.9" stroke-linecap="round" transform="rotate(-24.9 100 90)"/>
        <line class="sigil-tick" x1="100" y1="12" x2="100" y2="27" stroke="url(#tickGradT3)" stroke-width="3.2" stroke-linecap="round" transform="rotate(-8.2 100 90)"/>
        <line class="sigil-tick" x1="100" y1="12" x2="100" y2="27" stroke="url(#tickGradT3)" stroke-width="3.2" stroke-linecap="round" transform="rotate(8.4 100 90)"/>
        <line class="sigil-tick" x1="100" y1="13" x2="100" y2="27" stroke="url(#tickGradT2)" stroke-width="2.9" stroke-linecap="round" transform="rotate(25.1 100 90)"/>
        <line class="sigil-tick" x1="100" y1="14" x2="100" y2="27" stroke="url(#tickGradT2)" stroke-width="2.6" stroke-linecap="round" transform="rotate(41.8 100 90)"/>
        <line class="sigil-tick" x1="100" y1="15" x2="100" y2="27" stroke="url(#tickGradT1)" stroke-width="2.3" stroke-linecap="round" transform="rotate(58.5 100 90)"/>
        <line class="sigil-tick" x1="100" y1="16" x2="100" y2="27" stroke="url(#tickGradT1)" stroke-width="2" stroke-linecap="round" transform="rotate(75 100 90)"/>
      </g>
      <use class="wing-r" href="#sigil-wing" transform="translate(100,150)"/>
      <use class="wing-l" href="#sigil-wing" transform="translate(100,150) scale(-1,1)"/>
      <path class="sigil-flame" d="M100,58 C82,90 74,112 100,144 C126,112 118,90 100,58 Z" fill="url(#flameGrad)"/>
      <path class="sigil-core" d="M100,96 C90,112 88,124 100,138 C112,124 110,112 100,96 Z" fill="url(#coreGrad)" opacity="0.92"/>
    </symbol>
  </defs>
</svg>

<!-- ============ IGNITION LOADER ============ -->
<div id="loader">
  <svg class="sigil-mark" viewBox="0 0 200 200" id="loader-sigil"><use href="#sigil"/></svg>
  <div id="loader-word">ANGELTIER</div>
  <div id="loader-bar-wrap"><div id="loader-bar"></div></div>
  <div id="loader-status" class="mono">ĐANG THẮP LỬA · 0%</div>
</div>

<div class="ember-field" id="ember-field"></div>

<header>
  <div class="container">
    <a class="logo" onclick="switchView('home')">
      <svg class="sigil-mark ambient" viewBox="0 0 200 200"><use href="#sigil"/></svg>
      <span class="logo-text">ANGELTIER</span>
    </a>
    <ul class="nav-links">
      <li><a onclick="switchView('home')">Trang chủ</a></li>
      <li><a onclick="openRanking('Overall')">Bảng Xếp Hạng</a></li>
      <li><a href="https://discord.gg/vnlist" target="_blank" class="cta">⚡ Discord</a></li>
    </ul>
  </div>
</header>

<div class="container">

  <div id="home-view" class="view-section active">

    <section class="hero">
      <div class="hero-glow"></div>
      <div class="hero-tag">🔥 Cộng Đồng Minecraft PvP Việt Nam</div>
      <div class="hero-sigil-wrap">
        <svg class="sigil-mark ambient" viewBox="0 0 200 200"><use href="#sigil"/></svg>
      </div>
      <div class="hero-word">ANGELTIER</div>
      <div class="hero-sub">Trial by fire · Ranked by skill</div>
      <p class="lead">Gặp gỡ những chiến binh PvP hàng đầu Việt Nam. Bước qua ngọn lửa thử thách, để lại dấu ấn của mình trên Bảng Xếp Hạng Tier — nơi mỗi cấp bậc là một ngọn lửa bạn tự tay thắp lên.</p>
      <div class="hero-btns">
        <a onclick="openRanking('Overall')" class="btn btn-fire">🏆 Xem Bảng Xếp Hạng</a>
        <a href="https://discord.gg/vnlist" target="_blank" class="btn btn-ghost">⚡ Tham gia Test ngay</a>
      </div>
    </section>

    <div class="wing-divider reveal">
      <svg width="90" height="18" viewBox="0 0 90 18"><path d="M0 9 Q 20 -4 40 9" stroke="url(#wg1)" stroke-width="1.4" fill="none"/><defs><linearGradient id="wg1" x1="0" x2="1"><stop offset="0" stop-color="#f7c873" stop-opacity="0"/><stop offset="1" stop-color="#f7c873" stop-opacity=".8"/></linearGradient></defs></svg>
      <div class="wing-orb"></div>
      <svg width="90" height="18" viewBox="0 0 90 18"><path d="M90 9 Q 70 -4 50 9" stroke="url(#wg2)" stroke-width="1.4" fill="none"/><defs><linearGradient id="wg2" x1="1" x2="0"><stop offset="0" stop-color="#f7c873" stop-opacity="0"/><stop offset="1" stop-color="#f7c873" stop-opacity=".8"/></linearGradient></defs></svg>
    </div>

    <div class="card tier-card reveal">
      <div class="tier-top">
        <div>
          <div class="tier-eyebrow">Hệ thống Tier</div>
          <div class="tier-title">Ngọn lửa càng cao, đẳng cấp càng lớn</div>
        </div>
        <div class="tier-badge">10 CẤP BẬC</div>
      </div>
      <div class="flame-ladder" id="flame-ladder">
        <div class="flame-col"><div class="flame-bar t5" style="height:22px"></div><span class="flame-label">LT5</span></div>
        <div class="flame-col"><div class="flame-bar t5" style="height:30px"></div><span class="flame-label">HT5</span></div>
        <div class="flame-col"><div class="flame-bar t4" style="height:44px"></div><span class="flame-label">LT4</span></div>
        <div class="flame-col"><div class="flame-bar t4" style="height:52px"></div><span class="flame-label">HT4</span></div>
        <div class="flame-col"><div class="flame-bar t3" style="height:66px"></div><span class="flame-label">LT3</span></div>
        <div class="flame-col"><div class="flame-bar t3" style="height:84px"></div><span class="flame-label">HT3</span></div>
        <div class="flame-col"><div class="flame-bar t2" style="height:106px"></div><span class="flame-label">LT2</span></div>
        <div class="flame-col"><div class="flame-bar t2" style="height:124px"></div><span class="flame-label">HT2</span></div>
        <div class="flame-col hi"><div class="flame-bar t1" style="height:146px"></div><span class="flame-label">LT1</span></div>
        <div class="flame-col hi"><div class="flame-bar t1" style="height:164px"></div><span class="flame-label">HT1</span></div>
      </div>
      <div class="tier-desc">Mỗi Mode có Tier riêng biệt — điểm số cộng dồn vào tổng điểm Overall. Tier càng cao, ngọn lửa trên biểu đồ càng bùng cháy dữ dội. Vành hào quang của AngelTier mang đúng 10 nấc lửa này.</div>
    </div>

    <div class="card lb-box reveal">
      <div class="lb-header">
        <div>
          <div class="lb-live"><span class="lb-dot"></span>LIVE LEADERBOARD</div>
          <div class="lb-title">Top Players</div>
        </div>
        <div class="lb-filter" onclick="openRanking('Overall')">Overall ▾</div>
      </div>
      <div id="home-top-players"></div>
    </div>

    <div class="section-eyebrow reveal">Xếp hạng theo Mode</div>
    <div class="section-heading reveal">Modes Leaderboard</div>
    <div class="modes-grid reveal" id="modes-grid"></div>

    <div class="card stats-section reveal">
      <div class="section-eyebrow" style="margin-bottom:6px;">Những con số nổi bật</div>
      <div class="section-heading" style="margin-bottom:0;">Thống kê hệ thống</div>
      <div class="stats-grid">
        <div class="stat-box"><h2>1.800+</h2><p>Người chơi đã được Test</p></div>
        <div class="stat-box"><h2>5.200+</h2><p>Bài Test đã hoàn thành</p></div>
        <div class="stat-box"><h2>9</h2><p>Modes đang xếp hạng</p></div>
      </div>
    </div>

    <div class="card flow-section reveal">
      <div class="tier-eyebrow">Quy trình Test</div>
      <div class="section-heading" style="margin-bottom:0;">Từ tân binh đến huyền thoại</div>
      <div class="timeline">
        <div class="tl-step active">
          <div class="tl-num">1</div>
          <div><div class="tl-name">Tham gia Discord</div><div class="tl-desc">Tham gia Discord để nhận hỗ trợ hệ thống, cập nhật thông báo và giao lưu cùng cộng đồng AngelTier.</div></div>
        </div>
        <div class="tl-step">
          <div class="tl-num">2</div>
          <div><div class="tl-name">Đăng ký lịch Test</div><div class="tl-desc">Chọn Mode bạn muốn Test và đăng ký lịch phù hợp với thời gian rảnh của bạn.</div></div>
        </div>
        <div class="tl-step">
          <div class="tl-num">3</div>
          <div><div class="tl-name">Chờ đến lượt</div><div class="tl-desc">Hàng đợi được xử lý theo thứ tự đăng ký — Tester sẽ liên hệ khi đến lượt bạn.</div></div>
        </div>
        <div class="tl-step">
          <div class="tl-num">4</div>
          <div><div class="tl-name">Thi đấu trực tiếp</div><div class="tl-desc">Đối đầu trực tiếp với Tester trong các trận đấu thực tế để thể hiện trình độ thật sự.</div></div>
        </div>
        <div class="tl-step">
          <div class="tl-num">5</div>
          <div><div class="tl-name">Nhận kết quả & Tier</div><div class="tl-desc">Tester đánh giá và trao Tier chính xác dựa trên kỹ năng thể hiện trong trận đấu.</div></div>
        </div>
        <div class="tl-step">
          <div class="tl-num">6</div>
          <div><div class="tl-name">Leo hạng</div><div class="tl-desc">Tier của bạn được cộng điểm và xuất hiện ngay trên Bảng Xếp Hạng AngelTier.</div></div>
        </div>
      </div>
    </div>

    <div class="faq-section reveal">
      <div class="section-heading" style="text-align:center;">Những điều cần biết về AngelTier</div>
      <div class="faq-item active" onclick="toggleFaq(this)">
        <div class="faq-q">AngelTier hoạt động như thế nào? <span class="arrow">+</span></div>
        <div class="faq-a">AngelTier sử dụng hệ thống Tester chuyên nghiệp dành cho Minecraft PvP. Người chơi đăng ký, được Tester đánh giá trực tiếp qua các trận đấu thực tế và nhận Tier chính xác dựa trên kỹ năng.</div>
      </div>
      <div class="faq-item" onclick="toggleFaq(this)">
        <div class="faq-q">Làm sao để đăng ký Test? <span class="arrow">+</span></div>
        <div class="faq-a">Tham gia Discord của cộng đồng, vào kênh đăng ký Test, chọn Mode và khung giờ phù hợp. Tester sẽ nhắn tin xác nhận khi đến lượt bạn.</div>
      </div>
      <div class="faq-item" onclick="toggleFaq(this)">
        <div class="faq-q">Tier được đánh giá dựa trên tiêu chí gì? <span class="arrow">+</span></div>
        <div class="faq-a">Tester đánh giá dựa trên kỹ năng combat, khả năng ra quyết định, phản xạ và tư duy chiến thuật trong từng Mode cụ thể — không chỉ dựa vào thắng thua.</div>
      </div>
      <div class="faq-item" onclick="toggleFaq(this)">
        <div class="faq-q">Bao lâu thì có thể Test lại để lên Tier? <span class="arrow">+</span></div>
        <div class="faq-a">Thời gian chờ giữa hai lần Test cùng một Mode do quy định của cộng đồng đặt ra — thường được thông báo cụ thể trong Discord.</div>
      </div>
    </div>

    <footer>
      <div class="footer-brand">
        <a class="logo" onclick="switchView('home')">
          <svg class="sigil-mark ambient" viewBox="0 0 200 200" style="width:30px;height:30px;"><use href="#sigil"/></svg>
          <span class="logo-text">ANGELTIER</span>
        </a>
        <p>AngelTier là nền tảng đánh giá và xếp hạng Minecraft PvP hàng đầu tại Việt Nam — nơi kỹ năng được tôi luyện qua lửa.</p>
      </div>
      <div class="footer-col">
        <h4>Điều hướng</h4>
        <ul>
          <li><a onclick="switchView('home')">Trang chủ</a></li>
          <li><a onclick="openRanking('Overall')">Bảng Xếp Hạng</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Liên kết nhanh</h4>
        <ul><li><a href="https://discord.gg/vnlist" target="_blank">Discord AngelTier</a></li></ul>
      </div>
      <div class="footer-bottom">© AngelTier · Cộng đồng Minecraft PvP Việt Nam</div>
    </footer>
  </div>

  <div id="ranking-view" class="view-section">
    <div class="card rk-view-card">
      <div class="rk-header">
        <div class="rk-title">Bảng Xếp Hạng</div>
        <div class="rk-sub">Dữ liệu trực tiếp từ hệ thống Angel Bot.</div>
      </div>
      <div class="rk-tabs" id="ranking-tabs-bar"></div>
      <div class="rk-table-wrap">
        <table class="rk-table">
          <thead>
            <tr><th style="width:60px;">#</th><th style="width:220px;">Player</th><th style="width:100px;">Điểm</th><th>Tiers chi tiết</th></tr>
          </thead>
          <tbody id="ranking-table-body"></tbody>
        </table>
      </div>
    </div>
  </div>

</div>

<script>
let allPlayersData = [];
const REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const TIER_POINTS = {LT5:10,HT5:15,LT4:20,HT4:25,LT3:30,HT3:40,LT2:50,HT2:60,LT1:70,HT1:80};
function tierPoints(tier){ return TIER_POINTS[String(tier||'').trim().toUpperCase()] || 0; }

const modeList = [
  { id:"Overall", name:"OVERALL" },
  { id:"Sword", name:"SWORD" },
  { id:"Nethpot", name:"NETHPOT" },
  { id:"Pot", name:"POT" },
  { id:"Smp", name:"SMP" },
  { id:"Uhc", name:"UHC" },
  { id:"Axe", name:"AXE" },
  { id:"Vanilla", name:"VANILLA" },
  { id:"Mace", name:"MACE" }
];

const modeIcons = {
  Sword: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-sword" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7c873"/><stop offset="1" stop-color="#ff7a29"/></linearGradient></defs><path d="M14 3l7 7-2 2-7-7 2-2z" fill="url(#g-sword)"/><path d="M13.2 6.8L4 16l-1 4 4-1 9.2-9.2-3-3z" fill="url(#g-sword)" opacity="0.85"/><path d="M3 21l2.5-2.5" stroke="#f5efe4" stroke-width="1.4" stroke-linecap="round"/></svg>',
  Nethpot: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-neth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a29"/><stop offset="1" stop-color="#ff4519"/></linearGradient></defs><path d="M10 2h4v3h-4z" fill="#f7c873"/><path d="M8 6h8l1.5 5.5a6.5 6.5 0 1 1-11 0L8 6z" fill="url(#g-neth)"/><circle cx="12" cy="15" r="2.2" fill="#fff2df" opacity="0.85"/></svg>',
  Pot: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-pot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffcf7a"/><stop offset="1" stop-color="#f0982e"/></linearGradient></defs><path d="M10 2h4v3h-4z" fill="#f7c873"/><path d="M8 6h8l1.5 5.5a6.5 6.5 0 1 1-11 0L8 6z" fill="url(#g-pot)"/><rect x="10.4" y="13" width="3.2" height="4.2" rx="1.4" fill="#fff2df" opacity="0.85"/></svg>',
  Smp: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-smp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7c873"/><stop offset="1" stop-color="#d89a3f"/></linearGradient></defs><path d="M4 9l8-5 8 5-8 5-8-5z" fill="url(#g-smp)"/><path d="M4 9v6l8 5 8-5V9" stroke="#f7c873" stroke-width="1.3" fill="none" opacity="0.6"/><path d="M4 9l8 5 8-5" stroke="#1a0d04" stroke-width="0.6" fill="none" opacity="0.3"/></svg>',
  Uhc: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-uhc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9ad"/><stop offset="1" stop-color="#e8b95a"/></linearGradient></defs><path d="M12 8c-3.5 0-6 2.7-6 6.2C6 18 8.7 21 12 21s6-3 6-6.8C18 10.7 15.5 8 12 8z" fill="url(#g-uhc)"/><path d="M12 8c0-2 1-3.3 2.4-4.2-.2 1.6-1 2.6-1 2.6s1.6-.4 2.6-2c.3 2.2-1 3.9-2.4 4.6" fill="#8fce6a"/></svg>',
  Axe: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-axe" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7c873"/><stop offset="1" stop-color="#ff7a29"/></linearGradient></defs><path d="M13 3l-8 8 3 3 8-8-3-3z" fill="url(#g-axe)"/><path d="M14.2 4.2c2.2-.6 4.6-.2 6 1.2s1.8 3.8 1.2 6c-2.6-.2-4.4-1-5.8-2.4s-2.2-3.2-2.4-4.8" fill="url(#g-axe)" opacity="0.85"/><path d="M8 10L3 21" stroke="#f5efe4" stroke-width="1.4" stroke-linecap="round"/></svg>',
  Vanilla: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-van" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e4da"/><stop offset="1" stop-color="#a99cae"/></linearGradient></defs><path d="M12 3c4 0 7 2.4 7 6.2V13c0 4-3 7-7 7s-7-3-7-7V9.2C5 5.4 8 3 12 3z" fill="url(#g-van)"/><rect x="7.5" y="10" width="9" height="2.4" fill="#1a0d04" opacity="0.55"/></svg>',
  Mace: '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g-mace" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7c873"/><stop offset="1" stop-color="#ff4519"/></linearGradient></defs><circle cx="16.5" cy="7.5" r="4.3" fill="url(#g-mace)"/><circle cx="16.5" cy="7.5" r="1.6" fill="#1a0d04" opacity="0.4"/><path d="M13.6 10.4L4 20" stroke="#c9c2b4" stroke-width="1.8" stroke-linecap="round"/></svg>'
};

async function fetchBotData(){
  try{
    let response = await fetch('/api/leaderboard');
    allPlayersData = await response.json();
    renderHomeTopPlayers();
  }catch(error){
    console.error("Lỗi tải dữ liệu từ Angel Bot:", error);
    document.getElementById('home-top-players').innerHTML = '<div class="empty-state">Không thể tải dữ liệu từ Angel Bot lúc này.</div>';
  }
}

function renderHomeTopPlayers(){
  let container = document.getElementById('home-top-players');
  container.innerHTML = '';
  if(!allPlayersData.length){ container.innerHTML = '<div class="empty-state">Chưa có người chơi nào được xếp hạng.</div>'; return; }
  let top3 = allPlayersData.slice(0,3);
  top3.forEach((p,index) => {
    let medal = index===0 ? "🥇" : (index===1 ? "🥈" : "🥉");
    container.innerHTML += `
      <div class="player-row ${index===0?'top1':''}">
        <div class="player-left">
          <span class="rank-chip medal">#${index+1} ${medal}</span>
          <img src="${p.avatar}" class="avatar" alt="" onerror="this.style.visibility='hidden'">
          <span class="player-name">${p.name}</span>
        </div>
        <span class="player-points">${p.points} pts</span>
      </div>`;
  });
}

function renderModesGrid(){
  let grid = document.getElementById('modes-grid');
  grid.innerHTML = '';
  modeList.filter(m => m.id !== 'Overall').forEach(m => {
    grid.innerHTML += `
      <div class="card mode-card" onclick="openRanking('${m.id}')">
        <div class="mode-icon">${modeIcons[m.id] || ''}</div>
        <span class="mode-name">${m.name}</span>
      </div>`;
  });
}

function switchView(viewName){
  document.getElementById('home-view').classList.remove('active');
  document.getElementById('ranking-view').classList.remove('active');
  if(viewName==='home') document.getElementById('home-view').classList.add('active');
  else if(viewName==='ranking') document.getElementById('ranking-view').classList.add('active');
  window.scrollTo(0,0);
}

function openRanking(selectedMode){
  switchView('ranking');
  let bar = document.getElementById('ranking-tabs-bar');
  bar.innerHTML = '';
  modeList.forEach(m => {
    let isActive = m.id===selectedMode ? 'active' : '';
    bar.innerHTML += `<div class="rk-tab ${isActive}" onclick="openRanking('${m.id}')"><span>${m.name}</span></div>`;
  });

  let tbody = document.getElementById('ranking-table-body');
  tbody.innerHTML = '';

  let rows;
  if(selectedMode === 'Overall'){
    rows = allPlayersData.map(p => ({...p, displayPoints: p.points, focusMode: null}));
  } else {
    rows = allPlayersData
      .filter(p => p.tiers && p.tiers[selectedMode])
      .map(p => ({...p, displayPoints: tierPoints(p.tiers[selectedMode]), focusMode: selectedMode}))
      .sort((a,b) => b.displayPoints - a.displayPoints);
  }

  if(!rows.length){
    tbody.innerHTML = `<tr><td colspan="4"><div class="empty-state">Chưa có người chơi nào có Tier ở Mode này.</div></td></tr>`;
    return;
  }

  rows.forEach((p, index) => {
    let rankDisplay = String(index+1);
    if(index===0) rankDisplay = "1 🥇"; else if(index===1) rankDisplay = "2 🥈"; else if(index===2) rankDisplay = "3 🥉";

    let tiersHTML = '';
    if(p.tiers){
      for(let [m,t] of Object.entries(p.tiers)){
        let match = p.focusMode && m === p.focusMode ? 'match' : '';
        tiersHTML += `<div class="tier-chip ${match}">${m}: ${t}</div>`;
      }
    }

    tbody.innerHTML += `
      <tr>
        <td style="font-weight:700;color:var(--text-dim);">${rankDisplay}</td>
        <td>
          <div class="player-left">
            <img src="${p.avatar}" class="avatar" alt="" onerror="this.style.visibility='hidden'">
            <span class="player-name">${p.name}</span>
          </div>
        </td>
        <td style="font-weight:700;color:var(--gold);font-family:'JetBrains Mono',monospace;">${p.displayPoints}</td>
        <td><div class="tiers-wrap">${tiersHTML}</div></td>
      </tr>`;
  });
}

function toggleFaq(element){
  document.querySelectorAll('.faq-item').forEach(el => { if(el!==element) el.classList.remove('active'); });
  element.classList.toggle('active');
}

// ember particles
function buildEmbers(){
  const field = document.getElementById('ember-field');
  const count = 20;
  for(let i=0;i<count;i++){
    const e = document.createElement('div');
    e.className = 'ember' + (i % 6 === 0 ? ' spark' : '');
    const size = 2 + Math.random()*3.5;
    const left = Math.random()*100;
    const delay = Math.random()*9;
    const duration = 6 + Math.random()*6;
    const drift = (Math.random()*40-20).toFixed(0)+'px';
    e.style.width = size+'px';
    e.style.height = size+'px';
    e.style.left = left+'%';
    e.style.setProperty('--drift', drift);
    e.style.animationDelay = delay+'s';
    e.style.animationDuration = duration+'s';
    field.appendChild(e);
  }
}

// scroll reveal
function setupReveal(){
  const els = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, {threshold:0.15});
  els.forEach(el => io.observe(el));

  const ladder = document.getElementById('flame-ladder');
  const io2 = new IntersectionObserver((entries) => {
    entries.forEach(entry => { if(entry.isIntersecting){ ladder.classList.add('in'); io2.unobserve(ladder); } });
  }, {threshold:0.2});
  io2.observe(ladder);
}

/* ================= CUSTOM CURSOR ENGINE ================= */
function setupCursor(){
  const isFine = window.matchMedia('(pointer: fine)').matches;
  if(!isFine) return;
  document.body.classList.add('has-fine-pointer');

  const dot = document.getElementById('cursor-dot');
  const ring = document.getElementById('cursor-ring');
  let mx=-100,my=-100, rx=-100, ry=-100;
  let lastSpark = 0;

  document.addEventListener('mousemove', (e) => {
    mx = e.clientX; my = e.clientY;
    dot.style.transform = `translate3d(${mx-3}px, ${my-3}px, 0)`;

    const now = performance.now();
    if(!REDUCED_MOTION && now - lastSpark > 55){
      const dx = mx-rx, dy = my-ry;
      if(Math.hypot(dx,dy) > 14){
        lastSpark = now;
        const s = document.createElement('div');
        s.className = 'cursor-spark';
        s.style.left = (mx-2)+'px';
        s.style.top = (my-2)+'px';
        document.body.appendChild(s);
        setTimeout(()=>s.remove(), 720);
      }
    }
  });

  document.addEventListener('mousedown', ()=> ring.classList.add('click'));
  document.addEventListener('mouseup', ()=> ring.classList.remove('click'));
  document.addEventListener('mouseleave', ()=>{ dot.style.opacity=0; ring.style.opacity=0; });
  document.addEventListener('mouseenter', ()=>{ dot.style.opacity=1; ring.style.opacity=1; });

  function raf(){
    rx += (mx-rx)*0.18;
    ry += (my-ry)*0.18;
    ring.style.transform = `translate3d(${rx}px, ${ry}px, 0)`;
    requestAnimationFrame(raf);
  }
  raf();

  const hoverables = 'a, button, .player-row, .mode-card, .faq-item, .rk-tab, .lb-filter, .logo';
  document.addEventListener('mouseover', (e) => {
    if(e.target.closest(hoverables)){ ring.classList.add('hover'); dot.classList.add('hover'); }
  });
  document.addEventListener('mouseout', (e) => {
    if(e.target.closest(hoverables)){ ring.classList.remove('hover'); dot.classList.remove('hover'); }
  });
}

/* ================= IGNITION LOADER ENGINE ================= */
function runLoader(){
  const loader = document.getElementById('loader');
  const bar = document.getElementById('loader-bar');
  const status = document.getElementById('loader-status');
  const seen = sessionStorage.getItem('angeltier_intro_seen');

  const finish = () => {
    loader.classList.add('exit');
    document.body.classList.remove('loading');
    setTimeout(()=> loader.remove(), 750);
  };

  if(seen || REDUCED_MOTION){
    document.body.classList.remove('loading');
    loader.style.transition = 'none';
    loader.remove();
    return;
  }

  sessionStorage.setItem('angeltier_intro_seen','1');
  let pct = 0;
  const totalTime = 1650;
  const stepTime = 40;
  const steps = totalTime/stepTime;
  let step = 0;
  const timer = setInterval(()=>{
    step++;
    pct = Math.min(100, Math.round((step/steps)*100 + Math.random()*3));
    bar.style.width = pct+'%';
    status.textContent = (pct<100 ? 'ĐANG THẮP LỬA · ' : 'SẴN SÀNG · ') + Math.min(pct,100) + '%';
    if(step>=steps || pct>=100){
      clearInterval(timer);
      bar.style.width='100%';
      status.textContent='SẴN SÀNG · 100%';
      setTimeout(finish, 380);
    }
  }, stepTime);
}

window.onload = function(){
  buildEmbers();
  renderModesGrid();
  setupReveal();
  setupCursor();
  fetchBotData();
  runLoader();
};
</script>

</body>
</html>
"""


if __name__ == '__main__':
    print("🚀 Server AngelTier (giao diện + API) đang chạy tại http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
