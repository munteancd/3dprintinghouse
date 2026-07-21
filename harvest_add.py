"""Cauta modele dupa keyword-uri NOI si le ADAUGA in modele_vandabile.csv (dedup pe url).

Spre deosebire de harvest.py (care rescrie tot catalogul), asta pastreaza randurile
existente — inclusiv cele adaugate manual (ex: modelele de pe Thangs). Util cand vrei
sa imbogatesti o categorie fara sa reconstruiesti totul.

    python harvest_add.py earrings "gem earrings" pendant bracelet
    python harvest_add.py --min-dl 100 --pages 6 earrings ring

Dupa rulare: python build_site.py  (regenereaza site.html + coduri.csv)
"""
import argparse
import csv
from pathlib import Path

from harvest import harvest_makerworld, harvest_printables, trademark_risk

FIELDS = ["site", "license", "title", "author", "downloads",
          "trademark_risk", "keyword", "url", "img"]


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).parent
    ap.add_argument("keywords", nargs="+", help="keyword-uri de cautat (in ghilimele daca au spatii)")
    ap.add_argument("--pages", type=int, default=5, help="pagini per keyword per site")
    ap.add_argument("--min-dl", type=int, default=150, help="minim descarcari")
    ap.add_argument("--csv", default=str(here / "modele_vandabile.csv"))
    args = ap.parse_args()

    path = Path(args.csv)
    existing, seen = [], set()
    if path.exists():
        with path.open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                existing.append(r)
                seen.add(r["url"])
    print(f"Catalog existent: {len(existing)} modele.")

    added = []
    for i, kw in enumerate(args.keywords, 1):
        print(f"[{i}/{len(args.keywords)}] {kw}")
        for row in harvest_makerworld(kw, args.pages, args.min_dl) + \
                   harvest_printables(kw, args.pages, args.min_dl):
            if row["url"] in seen:
                continue
            seen.add(row["url"])
            row["trademark_risk"] = "DA" if trademark_risk(row["title"]) else ""
            added.append(row)

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(existing + added)

    risky = sum(1 for r in added if r["trademark_risk"])
    print(f"\nAdaugate {len(added)} modele noi ({risky} cu risc trademark, ignorate la build). "
          f"Total acum: {len(existing) + len(added)}.")
    print("Ruleaza acum: python build_site.py")


if __name__ == "__main__":
    main()
