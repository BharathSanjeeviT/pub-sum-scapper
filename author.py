from typing import List, Dict, Union, Optional

class Author:
    ALL_KEYS: Dict[str, List[str]] = {
        "JOURNAL": [ "Title", "Authors", "Publication Date", "Journal", "Volume", "Issue", "Pages", "Publisher", "Total Citations", "Year", "URL", "Index" ],
        "CONFERENCE": [ "Title", "Authors", "Publication Date", "Conference", "Volume", "Issue", "Pages", "Total Citations", "Year", "URL", "Index" ],
        "BOOK": [ "Title", "Authors", "Publication Date", "Book", "Volume", "Pages", "Publisher", "Isbn", "Total Citations", "Year", "URL" ],
        "PREPRINT": [ "Title", "Authors", "Publication Date", "Preprint", "Arxiv", "Biorxiv", "Ssrn", "Total Citations", "Year", "URL" ],
        "THESIS": ["Title", "Thesis", "Dissertation", "University", "Total Citations", "Year", "URL"],
        "PATENT": [ "Title", "Inventors", "Publication Date", "Patent Office", "Patent Number", "Application Number", "Total Citations", "Year", "URL" ],
        "REPORT": ["Title", "Report", "Technical Report", "Total Citations", "Year", "URL"],
        "OTHER": ["Title", "Authors", "Publication Date", "Source", "Report Number", "Total Citations", "Year", "URL"]
    }
    REQ_KEYS: Dict[str, List[str]] = {
        "JOURNAL": ["Journal", "Volume", "Issue"],
        "CONFERENCE": ["Conference", "Proceedings", "Symposium"],
        "BOOK": ["Book", "Publisher", "Isbn"],
        "PREPRINT": ["Preprint", "Arxiv", "Biorxiv", "Ssrn"],
        "THESIS": ["Thesis", "Dissertation", "University"],
        "PATENT": ["Patent"],
        "REPORT": ["Report", "Technical Report"]
    }

    def __init__(self):
        self.name: Optional[str] = None
        self.citations: Optional[int] = None
        self.h_index: Optional[int] = None
        self.i10_index: Optional[int] = None
        self.co_authors: List[str] = []
        self.year_cits: Dict[int, int] = {}
        self.publications: Dict[str, List[Dict[str, Union[str, int, None]]]] = {
            "JOURNAL": [],
            "CONFERENCE": [],
            "BOOK": [],
            "PREPRINT": [],
            "THESIS": [],
            "PATENT": [],
            "REPORT": []
        }

    def add_pub(self, pubs):
        for pub in pubs:
            for category, keys in self.REQ_KEYS.items():
                if all(key in pub for key in keys):  
                    self.publications[category].append(pub)
                    for key in self.ALL_KEYS[category]:
                        if key not in pub:
                            pub[key] = None
                    if 'Total Citations' not in pub:
                        pub['Total Citations'] = 0
                    if 'Year' not in pub:
                        pub['Year'] = 0
                    if 'Index' not in pub:
                        # GET INDEX
                        pub['Index'] = None
                    break

    def add(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value

    def add_all(self, data):
        for key, value in data.items():
            self.add(key, value)

    def as_obj(self):
        return {
            'name': self.name,
            'citations': self.citations,
            'h-index': self.h_index,
            'i10-index': self.i10_index,
            'co-authors': self.co_authors,
            'year-wise-citations': self.year_cits,
            'publications': self.publications
        }
