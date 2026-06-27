#!/usr/bin/env python3
"""
Generate sitemap.xml for beautybyyulis.com with all pages and hreflang alternates.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime

SITE_DIR = Path(__file__).parent.parent
DOMAIN = "https://www.beautybyyulis.com"

# Pages that have Spanish translations
TRANSLATED_PAGES = {
    '/': '/es/',
    '/services/': '/es/services/',
    '/locations/': '/es/locations/',
    '/contact/': '/es/contact/',
    '/about/': '/es/about/',
    '/blog/': '/es/blog/',
    '/photos/': '/es/photos/',
    '/blog/now-open-cutler-bay/': '/es/blog/ahora-abierto-cutler-bay/',
}

# Service/location pages (no Spanish translation yet)
SERVICE_PAGES = [
    '/box-braids-cutler-bay/',
    '/box-braids-doral-fl/',
    '/box-braids-homestead-fl/',
    '/box-braids-kendall-fl/',
    '/box-braids-miami/',
    '/braids-and-twists-cutler-bay/',
    '/braids-and-twists-homestead-fl/',
    '/braids-and-twists-miami/',
    '/bridal-styling-cutler-bay/',
    '/bridal-styling-homestead-fl/',
    '/bridal-styling-miami/',
    '/feed-in-cornrows-cutler-bay/',
    '/feed-in-cornrows-homestead-fl/',
    '/feed-in-cornrows-kendall-fl/',
    '/feed-in-cornrows-miami/',
    '/goddess-braids-cutler-bay/',
    '/goddess-braids-homestead-fl/',
    '/goddess-braids-kendall-fl/',
    '/goddess-braids-miami/',
    '/knotless-braids-coral-gables-fl/',
    '/knotless-braids-cutler-bay/',
    '/knotless-braids-doral-fl/',
    '/knotless-braids-homestead-fl/',
    '/knotless-braids-kendall-fl/',
    '/knotless-braids-miami/',
    '/knotless-braids-palmetto-bay/',
    '/knotless-braids-pinecrest-fl/',
]

# Priority mapping
PRIORITY = {
    '/': 1.0,
    '/es/': 0.9,
    '/services/': 0.9,
    '/es/services/': 0.8,
    '/locations/': 0.9,
    '/es/locations/': 0.8,
    '/contact/': 0.8,
    '/es/contact/': 0.7,
    '/about/': 0.7,
    '/es/about/': 0.6,
    '/blog/': 0.6,
    '/es/blog/': 0.5,
    '/photos/': 0.9,
    '/es/photos/': 0.8,
    '/blog/now-open-cutler-bay/': 0.9,
    '/es/blog/ahora-abierto-cutler-bay/': 0.8,
}

# Images for specific pages
IMAGES = {
    '/': [
        ('https://www.beautybyyulis.com/assets/images/hero-braids-miami.png',
         'Luxury Miami braiding by Beauty by Yulis',
         'Luxury hair braiding and protective styles by Yulis in South Miami and the Florida Keys.'),
    ],
    '/blog/now-open-cutler-bay/': [
        ('https://www.beautybyyulis.com/assets/images/yulis-and-friends-boho-braids.jpg',
         'Boho braids by Yulis in Cutler Bay, FL',
         'Local portfolio photo of boho braids and protective styling by Yulis for Cutler Bay clients.'),
    ],
    '/photos/': [
        ('https://www.beautybyyulis.com/assets/images/yulis-and-friends-boho-braids.jpg',
         'Boho braid finish by Yulis in Cutler Bay',
         'Portfolio photo of long boho braids by Yulis for Cutler Bay and South Miami clients.'),
        ('https://www.beautybyyulis.com/assets/images/beautiful-young-lady-long-braids.jpg',
         'Long protective braids by Yulis',
         'Clean long protective braid style by Yulis at BeautyByYulis.'),
        ('https://www.beautybyyulis.com/assets/images/guy-scalp-braid-cool-pattern.jpg',
         "Men's scalp braid pattern by Yulis",
         'Detailed scalp braid pattern and precise parts by Yulis in Cutler Bay.'),
        ('https://www.beautybyyulis.com/assets/images/child-head-braid-cool-pattern.jpg',
         'Kids braid design by Yulis',
         'Child-friendly scalp braid design with clean parts and gentle tension.'),
    ],
    '/es/photos/': [
        ('https://www.beautybyyulis.com/assets/images/yulis-and-friends-boho-braids.jpg',
         'Fotos de trenzas boho por Yulis en Cutler Bay',
         'Portafolio de trenzas boho y estilos protectores por Yulis para clientas de Cutler Bay.'),
    ],
}


def get_lastmod(path):
    """Get last modified date from file or use today's date."""
    file_path = SITE_DIR / path.strip('/') / 'index.html'
    if file_path.exists():
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    return datetime.now().strftime('%Y-%m-%d')


def generate_sitemap():
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml_ns = 'http://www.w3.org/1999/xhtml'
    image_ns = 'http://www.google.com/schemas/sitemap-image/1.1'

    root = ET.Element('{%s}urlset' % ns, {
        'xmlns': ns,
        'xmlns:xhtml': xhtml_ns,
        'xmlns:image': image_ns,
    })

    # Collect all pages
    all_pages = list(TRANSLATED_PAGES.keys()) + SERVICE_PAGES

    for path in all_pages:
        loc = f'{DOMAIN}{path}'
        url_elem = ET.SubElement(root, 'url')

        ET.SubElement(url_elem, 'loc').text = loc
        ET.SubElement(url_elem, 'lastmod').text = get_lastmod(path)
        ET.SubElement(url_elem, 'changefreq').text = 'weekly' if '/blog' in path else 'monthly'
        ET.SubElement(url_elem, 'priority').text = str(PRIORITY.get(path, 0.7))

        # Add hreflang alternates for translated pages
        if path in TRANSLATED_PAGES:
            es_path = TRANSLATED_PAGES[path]
            ET.SubElement(url_elem, f'{{{xhtml_ns}}}link', {
                'rel': 'alternate',
                'hreflang': 'es',
                'href': f'{DOMAIN}{es_path}',
            })
        elif path.startswith('/es/'):
            # Find English counterpart
            en_path = None
            for en, es in TRANSLATED_PAGES.items():
                if es == path:
                    en_path = en
                    break
            if en_path:
                ET.SubElement(url_elem, f'{{{xhtml_ns}}}link', {
                    'rel': 'alternate',
                    'hreflang': 'en',
                    'href': f'{DOMAIN}{en_path}',
                })

        # Add images
        if path in IMAGES:
            for img_url, img_title, img_caption in IMAGES[path]:
                img_elem = ET.SubElement(url_elem, f'{{{image_ns}}}image')
                ET.SubElement(img_elem, f'{{{image_ns}}}loc').text = img_url
                ET.SubElement(img_elem, f'{{{image_ns}}}title').text = img_title
                ET.SubElement(img_elem, f'{{{image_ns}}}caption').text = img_caption

    # Pretty print
    xml_str = minidom.parseString(ET.tostring(root, encoding='unicode')).toprettyxml(indent='  ')

    # Remove extra XML declaration
    lines = xml_str.split('\n')
    lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_str = '\n'.join(lines)

    # Write to file
    sitemap_path = SITE_DIR / 'sitemap.xml'
    sitemap_path.write_text(xml_str)
    print(f'Sitemap generated: {sitemap_path}')
    print(f'Total URLs: {len(all_pages)}')


if __name__ == '__main__':
    generate_sitemap()
