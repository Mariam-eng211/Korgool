# 🛡️ Korgool (Коргоол)
**Silent SMS Crisis Response Infrastructure for Kyrgyzstan**

## The Problem
In Kyrgyzstan, women facing domestic violence often cannot use existing reporting apps. Abusers frequently monitor smartphones, check call logs, and control mobile data access. Furthermore, women in rural areas or with disabilities may not have access to smartphones or internet.

## The Solution
Korgool is a **zero-trace, offline-first SMS reporting system**. 
- **No App:** The victim just sends an SMS from any $20 Nokia.
- **No Internet:** SMS works on 2G. The NGO's backend runs on a local laptop.
- **No Trace:** She texts a secret pre-registered codeword (e.g., `РОМАШКА`). The abuser thinks it's a typo.
- **30-Minute Vault:** If she requests a callback (`ПОЗВОНИ`), her number is held in a temporary vault for 30 minutes, allowing the operator to call her from a safe line. It is then permanently deleted.

## How it Works
1. **Codeword Path:** Pre-registered women text their secret word. The system instantly displays her name, exact address, and safe contacts to the NGO operator.
2. **Callback Path:** Anonymous women text for help with "ПОЗВОНИ" (Call Me). The operator calls them back securely.
3. **Anonymous Path:** If she stays fully anonymous, the system logs the severity and district for statistical advocacy and patrol mapping.

## Tech Stack (Offline-First)
- **Backend:** Python (Flask)
- **Database:** SQLite (WAL mode enabled for high concurrency)
- **Frontend:** Vanilla JS, HTML, CSS (Light/Dark mode)
- **SMS Gateway Ready:** Integrates via HTTP POST (`/sms/receive`) with any Android SMS Gateway or local telecom provider.

## Running Locally
1. `pip install flask`
2. `python app.py`
3. Open `http://localhost:5000`
4. Use the built-in SMS Simulator to test the triage engine.

*Note: For actual deployment, any Android phone running an SMS Gateway app can point its webhook to `/sms/receive`.*

## Why Open Source?
We built this as public infrastructure. Any crisis center in Kyrgyzstan can download this code, put it on a $50 laptop, and start saving lives tomorrow. We believe safety should not be proprietary.