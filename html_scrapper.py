def get_author_details(soup):
    author_pub = dict()
    auth_name_html = soup.find(id='gsc_prf_in')
    if auth_name_html:
        author_pub['name'] = auth_name_html.get_text()
    author_deatils_html = soup.find(id='gsc_rsb_st')
    if author_deatils_html:
        if(author_deatils_html.find('tbody')):
            author_deatils_html = author_deatils_html.find('tbody').find_all('tr')
            if author_deatils_html: 
                author_pub['citations'] = author_deatils_html[0].find(class_='gsc_rsb_std').get_text()
                author_pub['h-ind'] = author_deatils_html[1].find(class_='gsc_rsb_std').get_text()
                author_pub['i10-ind'] = author_deatils_html[2].find(class_='gsc_rsb_std').get_text()
        return author_pub

def get_coauths(soup):
    co_auths = []
    co_auths_list = soup.find(class_='gsc_rsb_a')
    if co_auths_list:
        for co_auth in co_auths_list.find_all('li'):
            co_auths.append(co_auth.find('a').get_text())
    return co_auths

def get_year_cits(soup):
    year_wise_cits = dict()
    year_wise_cits_html = soup.find(class_='gsc_md_hist_b')
    if year_wise_cits_html:
        years = year_wise_cits_html.find_all(class_='gsc_g_t')
        cits = year_wise_cits_html.find_all(class_='gsc_g_al')
        for i in range(len(years)):
            year_wise_cits[years[i].get_text()] = cits[i].get_text()
    return year_wise_cits


def get_auth_pubs(soup):
    publicatons_url = []
    pub_table_html = soup.find(id='gsc_a_t')
    if pub_table_html:
        pub_tbody_html = pub_table_html.find('tbody')
        if pub_tbody_html:
            for trow in pub_tbody_html.find_all('tr'):
                tdata = trow.find_all('td')
                publicatons_url.append(tdata[0].find('a').get('href'))
    return publicatons_url

def get_pub_details(soup):
    pub_details = dict() 
    pub_details['Title'] = soup.find(class_ = 'gsc_oci_title_link').get_text()
    pub_table = soup.find(id='gsc_oci_table')
    if pub_table: 
        pub_table_tr = pub_table.find_all(class_='gs_scl')
        for pub_table_td in pub_table_tr:
            key = pub_table_td.find(class_='gsc_oci_field').get_text()
            if key == 'Total citations':
                pub_details[key] = pub_table_td.find('a').get_text().split(' ')[2]
            elif key == 'Scholar articles': continue 
            else: pub_details[key] = pub_table_td.find(class_='gsc_oci_value').get_text()
    return pub_details
