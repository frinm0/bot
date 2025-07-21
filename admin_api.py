from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

def log_transaction(entry):
    try:
        with open("transactions.json", "r") as f:
            logs = json.load(f)
    except:
        logs = []
    logs.append(entry)
    with open("transactions.json", "w") as f:
        json.dump(logs, f, indent=2)

@app.post("/api/withdraw")
async def withdraw(req: Request):
    body = await req.json()
    user_id = str(body["user_id"])
    amount = int(body["amount"])
    to_user = str(body.get("to_user", user_id))

    data = load_data()
    balance = data["users"].get(user_id, {}).get("balance", 0)
    casino_balance = data.get("casino_balance", 0)

    if amount <= 0 or balance < amount:
        return {"status": "error", "message": "Недостаточно средств на балансе"}
    if casino_balance < amount:
        return {"status": "error", "message": "Недостаточно резерва казино"}

    data["users"][user_id]["balance"] -= amount
    data["casino_balance"] -= amount
    save_data(data)

    txid = str(uuid.uuid4())
    log_transaction({
        "type": "withdraw",
        "user_id": user_id,
        "amount": amount,
        "to_user": to_user,
        "txid": txid,
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"status": "ok", "txid": txid}

@app.post("/api/deposit")
async def deposit(req: Request):
    body = await req.json()
    user_id = str(body["6844038711"])
    amount = int(body["amount"])

    data = load_data()
    if user_id not in data["users"]:
        data["users"][user_id] = {"balance": 0}
    data["users"][user_id]["balance"] += amount
    data["casino_balance"] = data.get("casino_balance", 0) + amount
    save_data(data)

    txid = str(uuid.uuid4())
    log_transaction({
        "type": "deposit",
        "user_id": user_id,
        "amount": amount,
        "txid": txid,
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"status": "ok", "txid": txid}

@app.get("/api/stats/daily")
async def get_daily_stats(range: int = 30):
    try:
        with open("transactions.json", "r") as f:
            txs = json.load(f)
    except:
        return {"dates": [], "deposits": [], "withdrawals": []}

    today = datetime.utcnow().date()
    stats = {}
    for tx in txs:
        day = datetime.fromisoformat(tx["timestamp"]).date()
        if (today - day).days > range:
            continue
        key = str(day)
        if key not in stats:
            stats[key] = {"deposits": 0, "withdrawals": 0}
        if tx["type"] == "deposit":
            stats[key]["deposits"] += tx["amount"]
        elif tx["type"] == "withdraw":
            stats[key]["withdrawals"] += tx["amount"]

    sorted_keys = sorted(stats.keys())
    return {
        "dates": sorted_keys,
        "deposits": [stats[k]["deposits"] for k in sorted_keys],
        "withdrawals": [stats[k]["withdrawals"] for k in sorted_keys]
    }
