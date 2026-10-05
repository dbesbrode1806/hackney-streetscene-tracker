import datetime
import json


def main():
  data = {
      "last_updated": datetime.date.today().strftime("%d %B %Y"),
      "projects": [
          {
              "name": "Amhurst Road & Pembury Circus Transformation",
              "status": "Live Works",
              "location": (
                  "Amhurst Road, Mare Street & Pembury Circus Junction"
              ),
              "consultation": "Concluded",
              "schedule": "Feb 2025 – Mid/Late 2026",
              "works": (
                  "Major redesign of Pembury Circus junction, bus access"
                  " restrictions on Amhurst Rd/Mare St, high-street"
                  " repaving."
              ),
          },
          {
              "name": "Nile Street Public Realm Improvements",
              "status": "Live Works",
              "location": (
                  "Nile Street (Provost St to Britannia St), Hoxton West"
              ),
              "consultation": "Closed Sep 2025",
              "schedule": "Jan 2026 – Autumn 2026",
              "works": (
                  "Raised pedestrian footways, continuous pavement"
                  " installation across Provost St junction, tree planting."
              ),
          },
      ],
  }

  with open("projects.json", "w") as f:
    json.dump(data, f, indent=2)

  print("Successfully updated projects.json!")


if __name__ == "__main__":
  main()
