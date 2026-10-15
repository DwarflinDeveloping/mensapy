import re
import traceback
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from mensa import Meal

HOSTNAME = 'https://www.stw-thueringen.de'
LOADSPEISEPLAN_URL = '/xhr/loadspeiseplan.html'
QUICKLIKE_URL = 'xhr/quicklike.html'

cookies = {
    'filterkennz': '[]',
    'filterkennzAllow': 'true',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:154.0) Gecko/20100101 Firefox/154.0',
    'Accept': '*/*',
    'Accept-Language': 'de,en-US;q=0.9,en;q=0.8',
    'Origin': 'https://www.stw-thueringen.de',
    'Referer': 'https://www.stw-thueringen.de/mensen/',
}


class MensaSession(requests.Session):
    def __init__(self, hostname: Optional[str] = None, loadspeiseplan_url: Optional[str] = None,
                 quicklike_url: Optional[str] = None):
        super().__init__()

        self.hostname = hostname or HOSTNAME
        self.loadspeiseplan_url = urljoin(self.hostname, loadspeiseplan_url or LOADSPEISEPLAN_URL)
        self.quicklike_url = urljoin(self.hostname, quicklike_url or QUICKLIKE_URL)

        self.cookies.update(cookies)
        self.headers.update(headers)

    def like_meal(self, meal: Meal) -> int:
        """Likes a meal."""

        cookies = dict(self.cookies) | ({'selectedMensa': str(meal.rscid)})

        data = {
            'essenname': meal.name,
            'rscid': meal.rscid,
            'proddat': meal.proddat,
            'gebinde': meal.gebinde,
            'symbols': meal.symbols,
            'context': '',
        }

        response = requests.post(self.quicklike_url, cookies=cookies, data=data)
        return int(response.text)

    def load_speiseplan(self, mensa_id: int, date: Optional[str] = None) -> list[Meal]:
        """Loads the speiseplan and returns a list of meals."""

        if date is None:
            date = datetime.now().strftime("%d.%m.%Y")

        cookies = dict(self.cookies) | ({'selectedMensa': str(mensa_id)})
        data = {'resources_id': mensa_id, 'date': date}

        response = self.post(self.loadspeiseplan_url, cookies=cookies, data=data)

        bs = BeautifulSoup(response.text, 'html.parser')
        meal_divs = bs.find_all(class_="rowMealInner")
        return [self._parse_meal(meal_div) for meal_div in meal_divs]

    def _parse_meal(self, meal_div) -> Meal:
        """Some AI code to parse the HTML. Seems to be working well"""

        # Pflichtfelder & Basis-Metadaten
        name_elem = meal_div.find(class_="mealText")
        name = name_elem.get_text(strip=True) if name_elem else ""

        # rscid (int)
        rscid = 0
        rscid_elem = meal_div.find(class_="meal-rscid")
        if rscid_elem:
            try:
                rscid = int(rscid_elem.get_text(strip=True))
            except ValueError:
                pass

        # proddat (str)
        proddat_elem = meal_div.find(class_="meal-proddat")
        proddat = proddat_elem.get_text(strip=True) if proddat_elem else ""

        # gebinde (int)
        gebinde = 0
        gebinde_elem = meal_div.find(class_="meal-gebinde")
        if gebinde_elem:
            try:
                gebinde = int(gebinde_elem.get_text(strip=True))
            except ValueError:
                pass

        # symbols (str)
        symbols_elem = meal_div.find(class_="meal-symbols")
        symbols = symbols_elem.get_text(strip=True) if symbols_elem else ""

        # Zusatzstoffe (Optional[str])
        zusatzstoffe = None
        try:
            z_elem = meal_div.find(class_="zusatzstoffe")
            if z_elem:
                z_text = z_elem.get_text(strip=True)
                if "Zusatzstoffe:" in z_text:
                    parsed_z = z_text.replace("Zusatzstoffe:", "").strip()
                    zusatzstoffe = parsed_z if parsed_z else None
                else:
                    zusatzstoffe = z_text if z_text else None
        except (ValueError, TypeError):
            print("Error fetching zusatzstoffe")
            traceback.print_exc()

        # Allergene (Optional[list[str]])
        allergene = None
        try:
            a_elem = meal_div.find(class_="allergene")
            if a_elem:
                a_text = a_elem.get_text(strip=True)
                if "Allergene:" in a_text:
                    a_raw = a_text.replace("Allergene:", "").strip()
                    if a_raw:
                        allergene = [a.strip() for a in a_raw.split(",")]
        except (ValueError, TypeError):
            print("Error fetching allergene")
            traceback.print_exc()

        # Komponenten (Optional[list[str]])
        komponenten = None
        try:
            k_elem = meal_div.find(class_="komponenten")
            if k_elem:
                for br in k_elem.find_all("br"):
                    br.replace_with("\n")
                k_text = k_elem.get_text()
                extracted_k = []
                for line in k_text.split("\n"):
                    cleaned_line = line.strip().lstrip("•").strip()
                    if cleaned_line:
                        extracted_k.append(cleaned_line)
                if extracted_k:
                    komponenten = extracted_k
        except (ValueError, TypeError):
            print("Error fetching komponenten")
            traceback.print_exc()

        # Tooltips & CO2 (Optional[list[str]], Optional[int])
        tooltip = None
        co2_equivalent = None
        try:
            container_elems = meal_div.find_all(class_="tooltip-container")
            extracted_tooltips = []
            for container in container_elems:
                img_elem = container.find("img")
                if img_elem and img_elem.has_attr("alt"):
                    alt_text = img_elem["alt"].strip()
                    if "CO2" in alt_text or "CO₂" in alt_text or "Äquivalent" in alt_text:
                        match = re.search(r"(\d+)", alt_text)
                        if match:
                            co2_equivalent = int(match.group(1))
                        continue

                    if alt_text and alt_text not in extracted_tooltips:
                        extracted_tooltips.append(alt_text)

                span_elem = container.find(class_="tooltip")
                if span_elem:
                    span_text = span_elem.get_text(strip=True)
                    if "Die CO" not in span_text and span_text not in extracted_tooltips:
                        extracted_tooltips.append(span_text)

            if extracted_tooltips:
                tooltip = extracted_tooltips
        except (ValueError, TypeError):
            print("Error fetching tooltips")
            traceback.print_exc()

        # Preise (Optional[float])
        price_student = price_bedienstet = price_gast = None
        try:
            p_elem = meal_div.find(class_="mealPreise")
            if p_elem:
                p_text = p_elem.get_text(strip=True).replace("€", "").strip()
                parts = p_text.split("/")
                if len(parts) == 3:
                    def parse_price(part):
                        match = re.search(r"(\d+[\.,]\d+)", part)
                        if match:
                            return float(match.group(1).replace(",", "."))
                        raise ValueError(f"Could not find price in: {part}")

                    price_student = parse_price(parts[0])
                    price_bedienstet = parse_price(parts[1])
                    price_gast = parse_price(parts[2])
        except (ValueError, TypeError):
            print("Error fetching mealPreise")
            traceback.print_exc()

        # Extract likes count (Optional[int])
        likes = None
        try:
            quicklike_elem = meal_div.find(class_="quicklike")
            if quicklike_elem:
                likes_elem = quicklike_elem.find(class_="fa-stack-1x")
                if likes_elem:
                    likes_text = likes_elem.get_text(strip=True)
                    if likes_text:
                        likes = int(likes_text)
        except (ValueError, TypeError):
            print("Error fetching likes")
            traceback.print_exc()

        return Meal(
            name=name,
            gebinde=gebinde,
            rscid=rscid,
            proddat=proddat,
            symbols=symbols,
            likes=likes,
            zusatzstoffe=zusatzstoffe,
            allergene=allergene,
            komponenten=komponenten,
            tooltip=tooltip,
            co2_equivalent=co2_equivalent,
            price_student=price_student,
            price_bedienstet=price_bedienstet,
            price_gast=price_gast,
        )
