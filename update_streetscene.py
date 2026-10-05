import datetime
import json
import re
import requests
from bs4 import BeautifulSoup

# --- Scraping Endpoints ---
CITIZEN_SPACE_URL = (
    "https://consultation.hackney.gov.uk/consultation_finder/?st=open"
)
HACKNEY_TRAFFIC_ORDERS_URL = "https://www.hackney.gov.uk/parking-streets-and-transport/penalty-charge-notices/active-traffic-orders"


def fetch_citizen_space_consultations():
  """Scrapes all currently open consultations from Citizen Space."""
  consultations = []
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

  try:
    response = requests.get(CITIZEN_SPACE_URL, headers=headers, timeout=10)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")
      items = soup.find_all(
          "li", class_=re.compile("consultation-item|item", re.I)
      )

      for item in items:
        title_elem = item.find("a")
        date_elem = item.find(class_=re.compile("date|close", re.I))

        if title_elem:
          title = title_elem.get_text(strip=True)
          link = title_elem.get("href", "")
          if not link.startswith("http"):
            link = "https://consultation.hackney.gov.uk" + link

          closing_date = (
              date_elem.get_text(strip=True)
              if date_elem
              else "Open for feedback"
          )

          # Only capture transport / streetscene related consultations
          keywords = [
              "street",
              "road",
              "traffic",
              "school",
              "liveable",
              "cycle",
              "pedestrian",
              "parking",
              "ltn",
              "bus",
          ]
          if any(kw in title.lower() for kw in keywords):
            consultations.append({
                "name": title,
                "status": "Live Consultation",
                "location": "Borough-wide / Specified Location",
                "consultation": f"Open until: {closing_date}",
                "schedule": "In Consultation Phase",
                "works": f'Public consultation active. <a href="{link}" target="_blank">View on Citizen Space</a>',
            })
  except Exception as e:
    print(f"Error scraping Citizen Space: {e}")

  return consultations


def get_core_streetscene_projects():
  """Returns the base inventory of major ongoing physical works & upcoming schemes."""
  return [
      {
          "name": "Amhurst Road & Pembury Circus Transformation",
          "status": "Live Works",
          "location": (
              "Amhurst Road, Mare Street & Pembury Circus Junction, Hackney"
              " Central"
          ),
          "consultation": "Concluded (Feb 2024)",
          "schedule": "Feb 2025 – Mid/Late 2026",
          "works": (
              "Major junction safety redesign, bus access restrictions, high"
              " street urban realm repaving."
          ),
      },
      {
          "name": "Nile Street Public Realm Improvements",
          "status": "Live Works",
          "location": "Nile Street (Provost St to Britannia St), Hoxton West",
          "consultation": "Closed Sep 2025",
          "schedule": "Jan 2026 – Autumn 2026",
          "works": (
              "Raised pedestrian footways, continuous pavement installation"
              " across Provost St junction, tree planting."
          ),
      },
      {
          "name": "Bradstock Road & Cassland Road Junction Scheme",
          "status": "Live Works",
          "location": "Bradstock Road & Cassland Road, South Hackney",
          "consultation": "Concluded",
          "schedule": "March 2026 – Late 2026",
          "works": (
              "Parallel walking/cycling crossing over Cassland Road, footway"
              " widening, motor vehicle access restrictions."
          ),
      },
      {
          "name": "Chatsworth Road Liveable Neighbourhood",
          "status": "Live Works",
          "location": "Chatsworth Road corridor, Brooksby’s Walk & side streets",
          "consultation": "Concluded",
          "schedule": "Late 2025 – Late 2026",
          "works": (
              "Phased roll-out of central Chatsworth Road bus gate, traffic"
              " filter installations (modal filters)."
          ),
      },
      {
          "name": "Connecting Hoxton (Liveable Neighbourhood)",
          "status": "Upcoming Works",
          "location": (
              "Hoxton St, Stanway St, Purcell Gardens, Regan Way, Ivy St"
          ),
          "consultation": "Concluded Sep 2025",
          "schedule": "Late 2026 – 2027",
          "works": (
              "Public realm design finalized; upcoming physical delivery of bus"
              " gate on Hoxton St, footway improvements, public garden"
              " upgrades."
          ),
      },
      {
          "name": "School Streets Infrastructure Expansion",
          "status": "Live & Rolling",
          "location": (
              "Selected schools borough-wide (e.g. Cecilia Rd / Downs Park Rd)"
          ),
          "consultation": "Location-specific",
          "schedule": "Rolling rollout through 2026",
          "works": (
              "Installation of physical ANPR camera posts, operational street"
              " signage, and timed access barriers."
          ),
      },
  ]


def main():
  print("Starting daily Streetscene data scrape...")

  # 1. Scrape live open consultations from Citizen Space
  active_consultations = fetch_citizen_space_consultations()

  # 2. Fetch standard physical works inventory
  core_projects = get_core_streetscene_projects()

  # 3. Combine both lists (live consultations placed at the top)
  all_projects = active_consultations + core_projects

  # 4. Construct final structured JSON container
  data = {
      "last_updated": datetime.date.today().strftime("%d %B %Y"),
      "total_items": len(all_projects),
      "projects": all_projects,
  }

  # 5. Write out to projects.json
  with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

  print(
      f"Successfully output {len(all_projects)} items to projects.json at"
      f" {datetime.date.today()}."
  )


if __name__ == "__main__":
  main()
