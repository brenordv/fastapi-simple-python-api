import xml.etree.ElementTree as ET
import re

from raccoontools.generators.misc_generators import infinite_iterator
from raccoontools.shared.requests_with_retry import get

_rss_url_toronto = "https://www.cbc.ca/webfeed/rss/rss-canada-toronto"
_rss_url_technology = "https://www.cbc.ca/webfeed/rss/rss-technology"
_rss_url_canada = "https://www.cbc.ca/webfeed/rss/rss-canada"
_rss_url_top_stories = "https://www.cbc.ca/webfeed/rss/rss-topstories"
_urls = [
    _rss_url_toronto,
    _rss_url_technology,
    _rss_url_canada,
    _rss_url_top_stories
]

def _get_feed_from_cbc(url: str):
    response = get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
    })

    if response.status_code == 200:
        return response.text

    return None


def _get_next_next_url() -> str:
    yield infinite_iterator(_urls)


def _parse_cbc_rss(xml_content):
    """
    Parses an RSS XML feed from CBC.ca and extracts channel and item information.

    Parameters:
        xml_content (str): A string containing the RSS XML content.

    Returns:
        dict: A dictionary containing channel information and a list of items.
    """
    # Register namespaces
    namespaces = {'cbc': 'https://www.cbc.ca/rss/cbc'}

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Extract channel information
    channel = root.find('channel')
    channel_info = {
        'title': channel.findtext('title'),
        'description': channel.findtext('description'),
        'link': channel.findtext('link'),
        'lastBuildDate': channel.findtext('lastBuildDate'),
        'image': {
            'title': channel.find('image/title').text if channel.find('image/title') is not None else None,
            'url': channel.find('image/url').text if channel.find('image/url') is not None else None,
            'link': channel.find('image/link').text if channel.find('image/link') is not None else None,
        }
    }

    # Extract items
    items = []
    for item in channel.findall('item'):
        # Extract cbc attributes
        cbc_type = item.attrib.get('{https://www.cbc.ca/rss/cbc}type')
        cbc_deptid = item.attrib.get('{https://www.cbc.ca/rss/cbc}deptid')
        cbc_syndicate = item.attrib.get('{https://www.cbc.ca/rss/cbc}syndicate')

        # Extract standard item elements
        item_info = {
            'title': item.findtext('title'),
            'link': item.findtext('link'),
            'description': item.findtext('description'),
            'pubDate': item.findtext('pubDate'),
            'category': item.findtext('category'),
            'guid': item.findtext('guid'),
            'cbc_type': cbc_type,
            'cbc_deptid': cbc_deptid,
            'cbc_syndicate': cbc_syndicate,
        }

        # Extract optional cbc:authorName element
        author_elem = item.find('cbc:authorName', namespaces)
        if author_elem is not None:
            item_info['authorName'] = author_elem.text

        items.append(item_info)

    return {'channel': channel_info, 'items': items}


def _extract_img_src_and_text(html):
    # Regex pattern to extract the img src
    img_src_pattern = r"<img\s+[^>]*src=['\"]([^'\"]+)['\"]"
    # Regex pattern to extract the text content of the <p> tag
    text_pattern = r"<p>(.*?)</p>"

    # Extract the image src
    img_src_match = re.search(img_src_pattern, html)
    img_src = img_src_match.group(1) if img_src_match else None

    # Extract the text content
    text_match = re.search(text_pattern, html)
    text_content = text_match.group(1) if text_match else None

    return img_src, text_content


def fetch_news_article():
    results = []
    processed = {
        "copyright": "For personal use only! Look at the sources for whoever owns the news.",
        "sources": []
    }
    for url in _urls:
        x = _get_feed_from_cbc(url)
        news = _parse_cbc_rss(x)
        results.append(news)
        processed["sources"].append(url)

        for item in news["items"]:
            img_src, text_content = _extract_img_src_and_text(item["description"])

            item_category = item.get("category", "unknown")
            if item_category.strip() == "":
                item_category = "unknown"

            if item_category not in processed:
                processed[item_category] = []

            processed[item_category].append({
                "title": item["title"],
                "link": item["link"],
                "description_raw": item["description"],
                "description": text_content,
                "img_src": img_src,
                "pubDate": item["pubDate"],
                "category": item_category,
                "type": item.get("cbc_type", "unknown"),
            })

    return processed
