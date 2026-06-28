#!/usr/bin/env python3
"""
Fix unrendered template variables in location/service pages.

These pages have literal '+ seo_desc +', '+ canonical +', '+ seo_title +'
instead of actual values. This script extracts the correct values from
the page title and folder structure, then replaces the broken tags.
"""

import re
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent  # Site root (parent of scripts/)
DOMAIN = "https://www.beautybyyulis.com"

# Service name mapping (folder prefix -> display name)
SERVICE_NAMES = {
    'knotless-braids': 'Knotless Braids',
    'box-braids': 'Box Braids',
    'feed-in-cornrows': 'Feed-in Cornrows',
    'goddess-braids': 'Goddess Braids',
    'braids-and-twists': 'Braids & Twists',
    'bridal-styling': 'Bridal Styling',
}

# Location name mapping
LOCATION_NAMES = {
    'miami': 'Miami',
    'cutler-bay': 'Cutler Bay',
    'doral-fl': 'Doral, FL',
    'homestead-fl': 'Homestead, FL',
    'kendall-fl': 'Kendall, FL',
    'coral-gables-fl': 'Coral Gables, FL',
    'palmetto-bay': 'Palmetto Bay',
    'pinecrest-fl': 'Pinecrest, FL',
}


def parse_folder(folder_name):
    """Parse folder name into service and location."""
    # Try each service prefix
    for prefix, display in SERVICE_NAMES.items():
        if folder_name.startswith(prefix + '-'):
            location_slug = folder_name[len(prefix) + 1:]
            location = LOCATION_NAMES.get(location_slug, location_slug.replace('-', ' ').title())
            return display, location, location_slug
    return None, None, None


def fix_page(page_path):
    """Fix template variables in a single page."""
    content = page_path.read_text()

    # Extract folder name from path
    folder_name = page_path.parent.name

    service, location, location_slug = parse_folder(folder_name)
    if not service:
        print(f"  ⚠️  Unknown service in folder: {folder_name}")
        return False

    # Build proper values
    page_title = f"{service} in {location} | Beauty By Yulis"
    canonical = f"{DOMAIN}/{folder_name}/"
    seo_desc = f"Professional {service.lower()} in {location} by Yulis. Book your appointment for lightweight, comfortable braiding styles in South Miami."

    # Check if already fixed
    if '+ seo_desc +' not in content:
        return False

    # Replace broken template variables
    # Fix meta description
    content = re.sub(
        r'<meta name="description" content= \+ seo_desc \+ >',
        f'<meta name="description" content="{seo_desc}">',
        content
    )

    # Fix canonical
    content = re.sub(
        r'<link rel="canonical" href= \+ canonical \+ >',
        f'<link rel="canonical" href="{canonical}">',
        content
    )

    # Fix hreflang en
    content = re.sub(
        r'<link rel="alternate" hreflang="en" href= \+ canonical \+ >',
        f'<link rel="alternate" hreflang="en" href="{canonical}">',
        content
    )

    # Fix hreflang x-default
    content = re.sub(
        r'<link rel="alternate" hreflang="x-default" href= \+ canonical \+ >',
        f'<link rel="alternate" hreflang="x-default" href="{canonical}">',
        content
    )

    # Fix OG title
    content = re.sub(
        r'<meta property="og:title" content= \+ seo_title \+ >',
        f'<meta property="og:title" content="{page_title}">',
        content
    )

    # Fix OG description
    content = re.sub(
        r'<meta property="og:description" content= \+ seo_desc \+ >',
        f'<meta property="og:description" content="{seo_desc}">',
        content
    )

    # Fix OG URL
    content = re.sub(
        r'<meta property="og:url" content= \+ canonical \+ >',
        f'<meta property="og:url" content="{canonical}">',
        content
    )

    # Fix Twitter title
    content = re.sub(
        r'<meta name="twitter:title" content= \+ seo_title \+ >',
        f'<meta name="twitter:title" content="{page_title}">',
        content
    )

    # Fix Twitter description
    content = re.sub(
        r'<meta name="twitter:description" content= \+ seo_desc \+ >',
        f'<meta name="twitter:description" content="{seo_desc}">',
        content
    )

    page_path.write_text(content)
    return True


def main():
    broken = []
    fixed = 0

    for html_file in sorted(SITE_DIR.glob('*/index.html')):
        content = html_file.read_text()
        if '+ seo_desc +' in content:
            broken.append(html_file)

    print(f"Found {len(broken)} pages with unrendered template variables\n")

    for page_path in broken:
        if fix_page(page_path):
            fixed += 1
            print(f"  ✅ {page_path.parent.name}/")
        else:
            print(f"  ⚠️  {page_path.parent.name}/ (skipped)")

    print(f"\n✅ Fixed {fixed}/{len(broken)} pages")


if __name__ == '__main__':
    main()
