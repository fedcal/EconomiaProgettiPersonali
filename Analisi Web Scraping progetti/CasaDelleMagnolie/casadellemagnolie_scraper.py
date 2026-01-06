#!/usr/bin/env python3
"""
Web Scraper for casadellemagnolie.com
Extracts vacation rental property information including amenities, location, and features.
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CasaDelleMagnolieScraper:
    """Scraper for Casa delle Magnolie vacation rental website."""

    def __init__(self, base_url: str = "https://casadellemagnolie.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage."""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_property_info(self, soup: BeautifulSoup) -> Dict:
        """Extract basic property information."""
        property_info = {
            'name': None,
            'tagline': None,
            'location': None,
            'capacity': None,
            'description': None
        }

        # Extract property name
        title_elem = soup.find(['h1', 'h2'], class_=lambda x: x and any(
            word in str(x).lower() for word in ['title', 'name', 'property']
        ))
        if not title_elem:
            title_elem = soup.find('h1')

        if title_elem:
            property_info['name'] = title_elem.get_text(strip=True)

        # Extract tagline/slogan
        tagline_elem = soup.find(['p', 'div', 'span'], class_=lambda x: x and any(
            word in str(x).lower() for word in ['tagline', 'slogan', 'subtitle']
        ))
        if tagline_elem:
            property_info['tagline'] = tagline_elem.get_text(strip=True)

        # Extract location
        location_elem = soup.find(string=re.compile(r'Gallipoli|Baia Verde|Salento', re.IGNORECASE))
        if location_elem:
            property_info['location'] = location_elem.strip()

        # Extract capacity (beds/guests)
        capacity_elem = soup.find(string=re.compile(r'\d+\s*(bed|posto|guest)', re.IGNORECASE))
        if capacity_elem:
            capacity_match = re.search(r'(\d+)\s*(bed|posto|guest)', capacity_elem, re.IGNORECASE)
            if capacity_match:
                property_info['capacity'] = capacity_match.group(1) + ' ' + capacity_match.group(2)

        # Extract description
        desc_elem = soup.find(['p', 'div'], class_=lambda x: x and 'desc' in str(x).lower())
        if desc_elem:
            property_info['description'] = desc_elem.get_text(strip=True)

        logger.info("Extracted property information")
        return property_info

    def extract_amenities(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract property amenities and features."""
        amenities = []

        # Look for feature/amenity cards or lists
        amenity_sections = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(
            word in str(x).lower() for word in ['feature', 'amenity', 'card', 'service']
        ))

        for amenity in amenity_sections:
            amenity_data = {
                'name': None,
                'description': None,
                'icon': None
            }

            # Extract amenity name
            name_elem = amenity.find(['h3', 'h4', 'h5', 'strong', 'b'])
            if name_elem:
                amenity_data['name'] = name_elem.get_text(strip=True)

            # Extract description
            desc_elem = amenity.find(['p', 'span'])
            if desc_elem:
                amenity_data['description'] = desc_elem.get_text(strip=True)

            # Extract icon if present
            icon_elem = amenity.find(['i', 'svg', 'img'])
            if icon_elem:
                if icon_elem.name == 'img' and icon_elem.get('src'):
                    amenity_data['icon'] = icon_elem['src']
                elif icon_elem.get('class'):
                    amenity_data['icon'] = ' '.join(icon_elem['class'])

            if amenity_data['name']:
                amenities.append(amenity_data)

        # Also look for common amenities in text
        common_amenities = [
            'aria condizionata', 'air conditioning', 'parcheggio', 'parking',
            'cucina', 'kitchen', 'wifi', 'ascensore', 'elevator', 'beach',
            'spiaggia', 'mare', 'sea'
        ]

        text_content = soup.get_text().lower()
        for amenity in common_amenities:
            if amenity.lower() in text_content:
                if not any(a['name'] and amenity.lower() in a['name'].lower() for a in amenities):
                    amenities.append({
                        'name': amenity.title(),
                        'description': None,
                        'icon': None
                    })

        logger.info(f"Found {len(amenities)} amenities")
        return amenities

    def extract_distances(self, soup: BeautifulSoup) -> Dict:
        """Extract distances to points of interest."""
        distances = {}

        # Look for distance information (especially beach distance)
        text_content = soup.get_text()

        # Search for beach distance
        beach_pattern = re.compile(r'(\d+)\s*(m|metri|meters?).*?(spiaggia|beach)', re.IGNORECASE)
        beach_match = beach_pattern.search(text_content)
        if beach_match:
            distances['beach'] = f"{beach_match.group(1)} {beach_match.group(2)}"

        # Search for other distance patterns
        distance_pattern = re.compile(r'(\d+)\s*(km|m|metri|meters?)\s*(da|from|to)\s+([a-zA-Z\s]+)', re.IGNORECASE)
        for match in distance_pattern.finditer(text_content):
            distance_value = f"{match.group(1)} {match.group(2)}"
            place_name = match.group(4).strip()
            if len(place_name) < 30:  # Filter out long matches
                distances[place_name.lower()] = distance_value

        logger.info(f"Found {len(distances)} distance references")
        return distances

    def extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information."""
        contact = {
            'phone': None,
            'email': None,
            'website': self.base_url,
            'social_links': []
        }

        # Find all links
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']

            if 'mailto:' in href:
                contact['email'] = href.replace('mailto:', '')
            elif 'tel:' in href:
                contact['phone'] = href.replace('tel:', '').replace(' ', '')
            elif any(social in href for social in ['facebook', 'instagram', 'twitter', 'whatsapp']):
                contact['social_links'].append(href)

        # Search for phone numbers in text
        if not contact['phone']:
            phone_pattern = re.compile(r'\+?\d{2,3}[-.\s]?\d{3,4}[-.\s]?\d{4,}')
            phone_match = phone_pattern.search(soup.get_text())
            if phone_match:
                contact['phone'] = phone_match.group(0)

        # Search for email in text
        if not contact['email']:
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            email_match = email_pattern.search(soup.get_text())
            if email_match:
                contact['email'] = email_match.group(0)

        logger.info("Extracted contact information")
        return contact

    def extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract property images."""
        images = []

        # Find all images
        img_elements = soup.find_all('img', src=True)

        for img in img_elements:
            src = img['src']

            # Convert relative URLs to absolute
            if src.startswith('/'):
                src = self.base_url + src
            elif not src.startswith('http'):
                src = self.base_url + '/' + src

            # Filter out icons and small images
            if not any(x in src.lower() for x in ['icon', 'logo', 'favicon']):
                images.append({
                    'url': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })

        logger.info(f"Found {len(images)} images")
        return images

    def extract_navigation(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract navigation menu items and available pages."""
        nav_items = []

        # Find navigation menu
        nav = soup.find(['nav', 'header'])
        if nav:
            nav_links = nav.find_all('a', href=True)

            for link in nav_links:
                nav_item = {
                    'text': link.get_text(strip=True),
                    'url': link['href']
                }

                # Convert relative URLs to absolute
                if nav_item['url'].startswith('/'):
                    nav_item['url'] = self.base_url + nav_item['url']
                elif not nav_item['url'].startswith('http'):
                    nav_item['url'] = self.base_url + '/' + nav_item['url']

                if nav_item['text']:
                    nav_items.append(nav_item)

        logger.info(f"Found {len(nav_items)} navigation items")
        return nav_items

    def extract_languages(self, soup: BeautifulSoup) -> List[str]:
        """Extract available language options."""
        languages = []

        # Look for language switcher
        lang_elements = soup.find_all(['a', 'button'], class_=lambda x: x and 'lang' in str(x).lower())

        for elem in lang_elements:
            lang_text = elem.get_text(strip=True)
            lang_code = elem.get('href', '') or elem.get('data-lang', '')

            if lang_text:
                languages.append({
                    'name': lang_text,
                    'code': lang_code
                })

        # Look for hreflang attributes
        hreflang_links = soup.find_all('link', {'rel': 'alternate', 'hreflang': True})
        for link in hreflang_links:
            lang_code = link['hreflang']
            if lang_code not in [l.get('code') for l in languages]:
                languages.append({
                    'name': lang_code.upper(),
                    'code': lang_code
                })

        logger.info(f"Found {len(languages)} languages")
        return languages

    def scrape_all(self) -> Dict:
        """Scrape all data from the website."""
        logger.info("Starting scraping process...")

        soup = self.fetch_page(self.base_url)
        if not soup:
            logger.error("Failed to fetch homepage")
            return {}

        data = {
            'url': self.base_url,
            'scraped_at': datetime.now().isoformat(),
            'property': self.extract_property_info(soup),
            'amenities': self.extract_amenities(soup),
            'distances': self.extract_distances(soup),
            'contact': self.extract_contact_info(soup),
            'images': self.extract_images(soup),
            'navigation': self.extract_navigation(soup),
            'languages': self.extract_languages(soup)
        }

        logger.info("Scraping completed successfully")
        return data

    def save_to_json(self, data: Dict, filename: str = "casadellemagnolie_data.json"):
        """Save scraped data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to file: {e}")


def main():
    """Main execution function."""
    scraper = CasaDelleMagnolieScraper()

    # Scrape all data
    data = scraper.scrape_all()

    # Save to JSON
    scraper.save_to_json(data)

    # Print summary
    print("\n" + "="*50)
    print("SCRAPING SUMMARY - CASA DELLE MAGNOLIE")
    print("="*50)
    print(f"Property name: {data.get('property', {}).get('name', 'Not found')}")
    print(f"Location: {data.get('property', {}).get('location', 'Not found')}")
    print(f"Capacity: {data.get('property', {}).get('capacity', 'Not found')}")
    print(f"Amenities found: {len(data.get('amenities', []))}")
    print(f"Images found: {len(data.get('images', []))}")
    print(f"Distances tracked: {len(data.get('distances', {}))}")

    if data.get('distances', {}).get('beach'):
        print(f"Beach distance: {data['distances']['beach']}")

    print(f"Email: {data.get('contact', {}).get('email', 'Not found')}")
    print(f"Phone: {data.get('contact', {}).get('phone', 'Not found')}")
    print(f"Languages available: {len(data.get('languages', []))}")
    print(f"Navigation pages: {len(data.get('navigation', []))}")
    print("="*50)
    print(f"\nData saved to casadellemagnolie_data.json")


if __name__ == "__main__":
    main()
