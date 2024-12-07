from bs4 import BeautifulSoup
from author import Author
from utils import GS_URL, PARSER 
from html_scrapper import get_author_details, get_coauths, get_auth_pubs, get_pub_details, get_year_cits

# main function 
def get_author_gs(author_info, author: Author, page):
    try:
        html_content = fetch_author_gs_html(author_info['gs_id'], page)
        soup = BeautifulSoup(html_content, PARSER)

        # ADD AUTHOR DETAILS
        author.add_all(get_author_details(soup))
        author.add('co_authors', get_coauths(soup))
        author.add('year_cits', get_year_cits(soup))

        # ADD PUBLICATIONS
        author_pub_url = get_auth_pubs(soup)
        pub_html_content = fetch_author_pub(author_pub_url, page)
        author.add_pub(get_publications(pub_html_content))

    except Exception as err:
        return ({ 'status': 400, 'err': err })


def fetch_author_pub(author_pub_url, page):
    pub_html_content = []
    for pub_url in author_pub_url:
        page.goto(f'{GS_URL}/{pub_url}')
        pub_html_content.append({
            "url" : pub_url,
            "content" : page.content()
        })

    return pub_html_content

def get_publications(pub_html_content):
    publications = []
    for pub in pub_html_content:
        pub_soup = BeautifulSoup(pub['content'], PARSER)
        pub_obj = get_pub_details(pub_soup)
        pub_obj['URL'] = f"{GS_URL}/{pub['url']}"
        publications.append(pub_obj)
    return publications

def fetch_author_gs_html(author_id, page) -> str:
    author_url = f'{GS_URL}/citations?user={author_id}'
    page.goto(author_url)

    load_more_button = page.locator('#gsc_bpf_more')
    while load_more_button.is_enabled():
        load_more_button.click()
        # page.wait_for_timeout(1000)

    content = page.content()
    return content

# TODO GETTING PUB INDEX
def find_publication_index(pub_name):
    print(pub_name)
    return "" 
