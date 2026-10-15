# MensaPy

A lightweight Python client and CLI tool for fetching daily meal plans and automated quick-liking for **Studierendenwerk Thüringen** cafeterias and canteens (Mensen).

Designed by students of the Friedrich-Schiller-Universität Jena.

---

## Features

* **Multi-Mensa Support**: Full coverage for all Studierendenwerk Thüringen locations across Jena, Erfurt, Ilmenau, Gera, Eisenach, Nordhausen, Schmalkalden, and Weimar.
* **Detailed Meal Scraping**: Extracts full meal titles, pricing, components, allergens, additives, and CO₂ equivalent data.
* **Automated Likes**: Like your favorite meals programmatically via the backend endpoint.
* **Mass-Liking Rate Limiter**: Use `mass_like` to bump meal likes up to a target number safely at configurable time intervals.
* **Interactive CLI**: Menu-driven terminal script to select cafeterias, inspect dishes, and automate vote generation.

---

## 📁 Project Structure

```text
mensapy/
├── client.py    # MensaSession class for network requests & HTML parsing
├── mensa.py     # Mensa IntEnum mapping and Meal dataclass definitions
├── utils.py     # Utility functions (mass_like generator)
└── main.py      # Interactive CLI application
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/mensapy.git
   cd mensapy
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   `mensapy` requires `requests` and `beautifulsoup4` which can be found in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### 1. Interactive CLI (`main.py`)

Run the main script to interactively view and like dishes:

```bash
python main.py
```

## 📍 Supported Locations

| City | Supported Mensen & Cafeterias |
| :--- | :--- |
| **Jena** | Ernst-Abbe-Platz, Carl-Zeiss-Promenade, Philosophenweg, Uni Hauptgebäude, Moritz-von-Rohr-Straße, Cafeteria Carl-Zeiss-Straße |
| **Erfurt** | Nordhäuser Straße, Altonaer Straße, Cafeteria Schlüterstraße, Cafeteria Leipziger Straße |
| **Ilmenau** | Mensa Ehrenberg, Cafeteria Mensa Ehrenberg, Cafeteria Nanoteria, Cafeteria Röntgenbau |
| **Gera** | Mensa Weg der Freundschaft |
| **Eisenach** | Mensa Am Wartenberg |
| **Nordhausen** | Mensa Weinberg-Hof |
| **Schmalkalden** | Mensa Blechhammer |
| **Weimar** | Mensa am Park, Cafeteria am Horn, Cafeteria Mensa am Park |
