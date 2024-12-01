from flask import jsonify 
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_author_gs_html(author_id: str) -> str:
    url = f'https://scholar.google.com/citations?user={author_id}'
    user_agent = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.set_extra_http_headers({'User-Agent': user_agent})
        page.goto(url)

        while True:
            try:
                load_more_button = page.locator('#gsc_bpf_more')
                if load_more_button.is_enabled():
                    load_more_button.click()
                    page.wait_for_timeout(1000)
                else:
                    break
            except Exception:
                break

        content = page.content()

        browser.close()
        return content

def get_author_gs(author_id: str):
    try:
        html_content = fetch_author_gs_html(author_id)
        soup = BeautifulSoup(html_content, 'html.parser')
        author_pub = dict()

        auth_name_html = soup.find(id='gsc_prf_in')
        if auth_name_html:
            author_pub['name'] = auth_name_html.get_text()

        author_deatils_html = soup.find(id='gsc_rsb_st').find('tbody').find_all('tr')
        author_pub['cits'] = author_deatils_html[0].find(class_='gsc_rsb_std').get_text()
        author_pub['h'] = author_deatils_html[1].find(class_='gsc_rsb_std').get_text()

        co_auths = []
        co_auths_list = soup.find(class_='gsc_rsb_a')
        for co_auth in co_auths_list.find_all('li'):
            co_auths.append(co_auth.find('a').get_text())
        author_pub['co_authors'] = co_auths

        publications = []
        pub_table_html = soup.find(id='gsc_a_t')
        if pub_table_html:
            pub_tbody_html = pub_table_html.find('tbody')
            if pub_tbody_html:
                for trow in pub_tbody_html.find_all('tr'):
                    pub_details = dict()
                    pub_details = dict()
                    tdata = trow.find_all('td')
                    pub_details['title'] = tdata[0].find('a').get_text()
                    more_info = tdata[0].find_all('div')
                    pub_details['co_auhtors'] = more_info[0].get_text()
                    pub_details['desc'] = more_info[1].get_text()
                    pub_details['cits'] = tdata[1].get_text()
                    pub_details['year'] = tdata[2].get_text()
                    publications.append(pub_details)
                author_pub["pubs"] = publications
        return jsonify({
            'status': 200, 
            'author_pub': author_pub
        })
    except Exception as err:
        return jsonify({ 'status': 400, 'err': err })

