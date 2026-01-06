#!/usr/bin/env python3
"""
Web Scraper for federicocalo.dev
Extracts portfolio data including certifications, experience, education, and skills.
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FedericoCaloScraper:
    """Scraper for Federico Calò's portfolio website."""

    def __init__(self, base_url: str = "https://federicocalo.dev"):
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

    def extract_certifications(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract certification information."""
        certifications = []

        # Look for certification cards/sections
        cert_sections = soup.find_all(['div', 'article'], class_=lambda x: x and 'cert' in x.lower())

        for cert in cert_sections:
            cert_data = {
                'title': None,
                'organization': None,
                'date': None,
                'image_url': None
            }

            # Extract title
            title_elem = cert.find(['h3', 'h4', 'h5'])
            if title_elem:
                cert_data['title'] = title_elem.get_text(strip=True)

            # Extract organization
            org_elem = cert.find(class_=lambda x: x and any(word in str(x).lower() for word in ['org', 'issuer', 'provider']))
            if org_elem:
                cert_data['organization'] = org_elem.get_text(strip=True)

            # Extract date
            date_elem = cert.find(['time', 'span'], class_=lambda x: x and 'date' in str(x).lower())
            if date_elem:
                cert_data['date'] = date_elem.get_text(strip=True)

            # Extract image
            img_elem = cert.find('img')
            if img_elem and img_elem.get('src'):
                cert_data['image_url'] = img_elem['src']

            if cert_data['title']:
                certifications.append(cert_data)

        logger.info(f"Found {len(certifications)} certifications")
        return certifications

    def extract_experience(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract professional experience."""
        experiences = []

        # Look for experience/work sections
        exp_sections = soup.find_all(['div', 'article'], class_=lambda x: x and any(
            word in str(x).lower() for word in ['experience', 'work', 'job', 'role']
        ))

        for exp in exp_sections:
            exp_data = {
                'title': None,
                'company': None,
                'period': None,
                'description': None
            }

            # Extract title/role
            title_elem = exp.find(['h3', 'h4', 'h5'])
            if title_elem:
                exp_data['title'] = title_elem.get_text(strip=True)

            # Extract company
            company_elem = exp.find(class_=lambda x: x and 'company' in str(x).lower())
            if company_elem:
                exp_data['company'] = company_elem.get_text(strip=True)

            # Extract period
            period_elem = exp.find(['time', 'span'], class_=lambda x: x and any(
                word in str(x).lower() for word in ['date', 'period', 'year']
            ))
            if period_elem:
                exp_data['period'] = period_elem.get_text(strip=True)

            # Extract description
            desc_elem = exp.find(['p', 'div'], class_=lambda x: x and 'desc' in str(x).lower())
            if desc_elem:
                exp_data['description'] = desc_elem.get_text(strip=True)

            if exp_data['title']:
                experiences.append(exp_data)

        logger.info(f"Found {len(experiences)} work experiences")
        return experiences

    def extract_education(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract education information."""
        education = []

        # Look for education sections
        edu_sections = soup.find_all(['div', 'article'], class_=lambda x: x and any(
            word in str(x).lower() for word in ['education', 'degree', 'school']
        ))

        for edu in edu_sections:
            edu_data = {
                'degree': None,
                'institution': None,
                'year': None,
                'description': None
            }

            # Extract degree
            degree_elem = edu.find(['h3', 'h4', 'h5'])
            if degree_elem:
                edu_data['degree'] = degree_elem.get_text(strip=True)

            # Extract institution
            inst_elem = edu.find(class_=lambda x: x and any(
                word in str(x).lower() for word in ['school', 'university', 'institution']
            ))
            if inst_elem:
                edu_data['institution'] = inst_elem.get_text(strip=True)

            # Extract year
            year_elem = edu.find(['time', 'span'], class_=lambda x: x and 'year' in str(x).lower())
            if year_elem:
                edu_data['year'] = year_elem.get_text(strip=True)

            if edu_data['degree']:
                education.append(edu_data)

        logger.info(f"Found {len(education)} education entries")
        return education

    def extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills and technologies."""
        skills = []

        # Look for skills sections
        skills_section = soup.find(['div', 'section'], class_=lambda x: x and 'skill' in str(x).lower())

        if skills_section:
            # Extract individual skill items
            skill_items = skills_section.find_all(['li', 'span', 'div'], class_=lambda x: x and any(
                word in str(x).lower() for word in ['skill', 'tech', 'tag']
            ))

            for item in skill_items:
                skill_text = item.get_text(strip=True)
                if skill_text and len(skill_text) < 50:  # Filter out long descriptions
                    skills.append(skill_text)

        logger.info(f"Found {len(skills)} skills")
        return list(set(skills))  # Remove duplicates

    def extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information and social links."""
        contact = {
            'email': None,
            'github': None,
            'linkedin': None,
            'twitter': None,
            'other_links': []
        }

        # Find all links
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']

            if 'mailto:' in href:
                contact['email'] = href.replace('mailto:', '')
            elif 'github.com' in href:
                contact['github'] = href
            elif 'linkedin.com' in href:
                contact['linkedin'] = href
            elif 'twitter.com' in href or 'x.com' in href:
                contact['twitter'] = href
            elif href.startswith('http') and 'federicocalo.dev' not in href:
                contact['other_links'].append(href)

        logger.info("Extracted contact information")
        return contact

    def extract_about(self, soup: BeautifulSoup) -> str:
        """Extract about/bio section."""
        about_section = soup.find(['section', 'div'], class_=lambda x: x and 'about' in str(x).lower())

        if about_section:
            paragraphs = about_section.find_all('p')
            about_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            logger.info("Extracted about section")
            return about_text

        return ""

    def scrape_all(self) -> Dict:
        """Scrape all data from the portfolio."""
        logger.info("Starting scraping process...")

        soup = self.fetch_page(self.base_url)
        if not soup:
            logger.error("Failed to fetch homepage")
            return {}

        data = {
            'url': self.base_url,
            'scraped_at': datetime.now().isoformat(),
            'about': self.extract_about(soup),
            'certifications': self.extract_certifications(soup),
            'experience': self.extract_experience(soup),
            'education': self.extract_education(soup),
            'skills': self.extract_skills(soup),
            'contact': self.extract_contact_info(soup)
        }

        logger.info("Scraping completed successfully")
        return data

    def save_to_json(self, data: Dict, filename: str = "federicocalo_data.json"):
        """Save scraped data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to file: {e}")


def main():
    """Main execution function."""
    scraper = FedericoCaloScraper()

    # Scrape all data
    data = scraper.scrape_all()

    # Save to JSON
    scraper.save_to_json(data)

    # Print summary
    print("\n" + "="*50)
    print("SCRAPING SUMMARY")
    print("="*50)
    print(f"Certifications found: {len(data.get('certifications', []))}")
    print(f"Work experiences found: {len(data.get('experience', []))}")
    print(f"Education entries found: {len(data.get('education', []))}")
    print(f"Skills found: {len(data.get('skills', []))}")
    print(f"Email: {data.get('contact', {}).get('email', 'Not found')}")
    print(f"GitHub: {data.get('contact', {}).get('github', 'Not found')}")
    print(f"LinkedIn: {data.get('contact', {}).get('linkedin', 'Not found')}")
    print("="*50)
    print(f"\nData saved to federicocalo_data.json")


if __name__ == "__main__":
    main()
