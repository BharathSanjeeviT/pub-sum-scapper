from flask import jsonify 
from bs4 import BeautifulSoup
from browser import Playwright
from utils import GS_URL, PARSER, CATEGORIES
from html_scrapper import get_author_details, get_coauths, get_auth_pubs, get_pub_details, get_year_cits

def fetch_author_gs_html(author_id: str) -> str:
    browser = Playwright()
    page = browser.create_page_with_context()

    author_url = f'{GS_URL}/citations?user={author_id}'
    page.goto(author_url)

    load_more_button = page.locator('#gsc_bpf_more')
    while load_more_button.is_enabled():
        load_more_button.click()
        # page.wait_for_timeout(1000)

    content = page.content()
    browser.close_browser()
    return content

def fetch_author_pub(author_pub_url):
    browser = Playwright()
    page = browser.create_page_with_context()

    pub_html_content = []
    for pub_url in author_pub_url:
        page.goto(f'{GS_URL}/{pub_url}')
        pub_html_content.append(page.content())

    browser.close_browser()
    return pub_html_content

# main function 
def get_author_gs(author_id: str):
    try:
        html_content = fetch_author_gs_html(author_id)
        soup = BeautifulSoup(html_content, PARSER)

        author_pub = dict()
        get_author_details(soup, author_pub)
        author_pub['co_authors'] = get_coauths(soup)
        author_pub['year-cits'] = get_year_cits(soup)
        author_pub_url = get_auth_pubs(soup)

        pub_html_content = fetch_author_pub(author_pub_url)
        publications = get_publications(pub_html_content)

        return jsonify({
            'status': 200, 
            **author_pub,
            'publications': publications
        })

    except Exception as err:
        return jsonify({ 'status': 400, 'err': err })

def get_publications(pub_html_content):
    publications = dict()
    for pub in pub_html_content:
        pub_soup = BeautifulSoup(pub, PARSER)
        pub_obj = get_pub_details(pub_soup)
        for category, keys in CATEGORIES.items():
            if all(key in pub_obj for key in keys):  
                if category not in publications:
                    publications[category] = []
                publications[category].append(pub_obj)
    return publications

