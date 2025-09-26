# SwagTrackr  

## Problem Statement  
The Operations team at VandyHacks has to manage a large number of physical items (t-shirts, stickers, swag). Tracking inventory manually is inefficient and often leads to errors — shirts being over-counted, stickers running out unexpectedly, or swag deliveries delayed. There is no simple system to:  
- Track current inventory.  
- Log check-outs when items are handed out to participants.  
- Generate real-time reports for organizers.  

----------------------

## Proposed Solution: SwagTrackr  
SwagTrackr is a **minimal inventory management app** designed specifically for hackathon operations. It provides organizers with a simple interface (CLI or web) to:  
- Maintain an up-to-date inventory of items.  
- Record check-outs when items are distributed.  
- Generate real-time inventory reports so organizers know what’s left.  

This app keeps things lightweight but still solves the core need: **tracking items quickly and accurately** during the event.  

----------------------

## Core Features Implemented  
1. **Inventory CRUD (Create, Read, Update, Delete)**  
   - Add new swag items (e.g., “T-shirt L”, “Sticker Pack”).  
   - Update quantities when shipments arrive.  
   - Delete items if no longer tracked.  
   - List all current items with quantities.  

2. **Check-Out Tracking**  
   - Deduct items when they’re handed out.  
   - Optionally record who received them (for accountability).  
   - Prevent negative stock (alerts if stock is too low).  

----------------------

## Screenshots / Example Output  
### CLI Example:  
```bash
$ python swagtrackr.py add "T-shirt L" 200
Added 200 of T-shirt L.

$ python swagtrackr.py checkout "T-shirt L" 3
Checked out 3 of T-shirt L. Remaining: 197

$ python swagtrackr.py list
Inventory:
- T-shirt L: 197
- Stickers: 150
```

----------------------

##Tech Stack & Tools  
This project is designed to be **minimal yet structured**.  

### Languages & Usage  
- **Python**  → Core backend logic & CLI interface.  
- **SQLite**  → Lightweight database to persist inventory across runs.  
- **Click (Python library)** → Clean CLI commands (`add`, `checkout`, `list`).  

----------------------

##Thought Process  
- **Why Python + SQLite?**  
  They’re lightweight, easy to set up, and don’t require external dependencies. Perfect for hackathon-scale software.  
- **Why a CLI first?**  
  It ensures organizers can run it anywhere (laptop, server, etc.) without setup overhead.  
- **Scalability:** If VandyHacks grows, we can extend into a web dashboard, connect APIs, and track delivery statuses.  

----------------------

## How to Run  
1. Clone repo:  
   ```bash
   git clone https://github.com/your-username/swagtrackr.git
   cd swagtrackr
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run commands:  
   ```bash
   python swagtrackr.py add "Stickers" 150
   python swagtrackr.py list
   python swagtrackr.py checkout "Stickers" 10
   ```  

----------------------

##Comments on the Project  
This was a fun challenge because it shows how even small tools can have a big impact in real hackathon logistics.  
Future ideas I considered:  
- Integrating QR code scanning for quick item check-out.  
- Adding a web dashboard with role-based access (volunteers vs. organizers).  
- Visual analytics of swag distribution.  
