import datetime

metadata = dict(
    name='Rhode Island and Providence Plantations',
    abbreviation='ri',
    legislature_name='Rhode Island General Assembly',
    upper_chamber_name='Senate',
    lower_chamber_name='House of Representatives',
    upper_chamber_title='Senator',
    lower_chamber_title='Representative',
    upper_chamber_term=2,
    lower_chamber_term=2,
    terms=[{'name': '2011',
            'start_year': 2011,
            'start_date': datetime.date(2011, 1, 4),
            'end_year': 2011,
            'sessions': ['2011']},
            ],
    session_details={'2011': {'start_date': datetime.date(2011, 1, 4),
                              'type': 'primary'},
                    },
)

def session_list():
    from billy.scrape.utils import url_xpath
    return url_xpath( 'http://status.rilin.state.ri.us/bill_history.aspx?mode=previous',
        "//select[@name='ctl00$rilinContent$cbYear']/option/text()" )
