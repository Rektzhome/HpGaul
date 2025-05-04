# Hi, I'm Muh Amin Arsyad — a code artisan from Indonesia!  

[![GitHub followers](https://img.shields.io/github/followers/Rektzhome?label=Follow&style=social)](https://github.com/Rektzhome)  
[![LinkedIn](https://img.shields.io/badge/-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourprofile)  
[![Personal Website](https://img.shields.io/badge/-Website-black?style=flat-square&logo=github)](https://github.com/Rektzhome)

---

### About Me
- 🧠 Focused on backend development & data scraping  
- ⚒️ Building: [`HpGaul`](https://github.com/Rektzhome/HpGaul) — a Node.js-powered smartphone scraper  
- 🧩 Loves efficient code, hates dummy data  
- 🕹️ Current Stack: Node.js, Express, Puppeteer, MongoDB  
- ☕ Fuel: Kopi dan deadline mendadak  

---

### Featured Project
#### [`HpGaul`](https://github.com/Rektzhome/HpGaul)
Scrapes smartphone data like a ninja—accurate, silent, and no dummy data allowed.

![Status](https://img.shields.io/badge/status-maintained-brightgreen)
![Tech](https://img.shields.io/badge/node.js-checked-blue)
![Data](https://img.shields.io/badge/dummy%20data-nope-red)

---

### GitHub Stats

![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=Rektzhome&layout=


# GSMArena Phone Scraper Web App (Redesigned)

This is a simple Flask web application that allows users to search for phone specifications on GSMArena.com. This version features a redesigned user interface using Tailwind CSS (via Play CDN) and vanilla JavaScript, incorporating features like dark mode, cards for results, and a modal for detailed views.

## Structure

- `src/main.py`: The main Flask application file. It defines routes and runs the app.
- `src/scraper.py`: Contains the Python script using Playwright to scrape GSMArena.
- `src/routes/gsmarena.py`: Defines the Flask blueprint and API endpoint (`/api/gsmarena/search`) that triggers the scraper.
- `src/static/index.html`: The frontend HTML page with the redesigned UI (Tailwind CSS via CDN), search form, card display, modal, dark mode toggle, and JavaScript to interact with the API.
- `requirements.txt`: Lists the Python dependencies required to run the application.
- `venv/`: Python virtual environment (not included in zip).

## How to Run Locally

1.  **Navigate to the project directory:**
    ```bash
    cd gsmarena_web_app
    ```
2.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
3.  **Install Python dependencies (if not already installed):**
    ```bash
    pip install -r requirements.txt
    # You might also need to install Playwright browsers if running for the first time:
    playwright install --with-deps chromium
    ```
4.  **Run the Flask application:**
    ```bash
    python src/main.py
    ```
5.  Open your web browser and go to `http://127.0.0.1:5002` (or the port specified in `main.py`).

**Note:**
- The frontend uses Tailwind CSS via the Play CDN, so an internet connection is required for the styles to load.
- The scraping process can take some time depending on the GSMArena website's response time.

