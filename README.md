# Lumina Travel — Proactive AI Trip Concierge

[![Watch Travel Concierge Walkthrough](https://cdn.loom.com/sessions/thumbnails/7ef79d0ab08240db95e4abafe165b8e2-with-play.gif)](https://www.loom.com/share/7ef79d0ab08240db95e4abafe165b8e2)

Lumina Travel is a proactive, end-to-end AI Trip Concierge designed to plan, research, and book travels while keeping humans in the loop for financial security. It is built with the **Google Antigravity SDK** and powered by **Gemini 3.5 Flash**.

It handles the entire travel lifecycle: researching weather and cultural highlights, finding accommodations, and conducting safe checkouts for bookings with explicit confirmation check-gates.

---

## 🚀 Key Features

* **Authoritative Destination Research**: Leverages weather conditions, local norms (etiquette rules), transit guides, and major cultural events to ground travel tips.
* **Smart Lodging Finder**: Discovers, filters, and ranks premium accommodations based on rating, location, pricing, and refund policies.
* **Safe Booking Check-Gates**: Intercepts financial transactions, requiring explicit in-chat user confirmation (`yes` / `confirm`) before calling the execution tool.
* **Active Travel Suitcase**: Tracks and lists active reservations and bookings in real-time in a dedicated sidebar widget.
* **Self-Contained Fallbacks**: Dynamically designs itineraries and lodging options for any tourist destination globally, keeping the user journey completely fluid.
* **Premium User Interface**: Features a custom glassmorphic dark-mode console with live streaming, reasoning disclosure drawers, and interactive testing chips.

---

## 📁 Repository Structure

```
lumina_travel/
├── app.py                  # FastAPI Application and streaming chat endpoints
├── agent.py                # Antigravity Agent and persona instructions
├── tools.py                # Weather, cultural database, search, and checkout booking tools
├── pyproject.toml          # Dependency declarative definitions
├── start-lumina-travel     # Background launch helper on port 8002
├── stop-lumina-travel      # Teardown helper script
└── static/                 # Beautiful Glassmorphic UI & stylesheets
```

---

## 🛠️ Local Quickstart

### Prerequisites
Make sure you have `uv` installed (Python package manager). If not, install it with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Configure Secrets
Create a `.env` file in the workspace root or this directory with your Gemini API key:
```bash
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Start the Server
Run the launch helper to start the service on port `8002` in the background:
```bash
chmod +x start-lumina-travel stop-lumina-travel
./start-lumina-travel
```

### 3. Open the Interface
Navigate to:
👉 **[http://localhost:8002](http://localhost:8002)**

### 4. Stop the Server
When you are done, clean up all background services with:
```bash
./stop-lumina-travel
```

---

## 🔒 Financial Safety Containment
This concierge is audited against prompt injection and hijacking attacks using `test_security.py` in the workspace root. It safely contains:
* **Booking Hijacking**: Will never execute booking tools or trigger billing cards unless the user explicitly typing approval in the conversation.
* **Behavioral Hijacks**: Rejects prompts ordering illegal transit evasion/ticket sneaking tips, steering travelers to legal options instead.
