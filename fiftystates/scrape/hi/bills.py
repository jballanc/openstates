from fiftystates.scrape import ScrapeError, NoDataForYear
from fiftystates.scrape.votes import Vote
from fiftystates.scrape.bills import BillScraper, Bill

import lxml.html
import re, contextlib
import datetime as dt



class HIBillScraper(BillScraper):
    state = 'hi'
    
    @contextlib.contextmanager
    def lxml_context(self, url, sep=None, sep_after=True):
        try:
            body = self.urlopen(url)
        except:
            body = self.urlopen("http://www.google.com")
        
        if sep != None: 
            if sep_after == True:
                before, itself, body = body.rpartition(sep)
            else:
                body, itself, after = body.rpartition(sep)    
        
        elem = lxml.html.fromstring(body)
        
        try:
            yield elem
        except:
            raise
    

    def scrape(self, chamber, year):
        session = "%s-%d" % (year, int(year) + 1)

        if int(year) >= 2009:
            self.scrape_session_2009(chamber, session)
        else:
            self.scrape_session_old(chamber, session)

    def scrape_session_2009(self, chamber, session):
        if chamber == "upper":
            url = "http://www.capitol.hawaii.gov/session2009/lists/RptIntroSB.aspx"
            type = "HB"
        else:
            url = "http://www.capitol.hawaii.gov/session2009/lists/RptIntroSB.aspx"
            type = "SB"
            
        with self.lxml_context(url) as page:
            for element, attribute, link, pos in page.iterlinks():         
                if re.search("billtype=" + type + "&billnumber=[0-9]+", link) != None:
                    bill_page_url = "http://www.capitol.hawaii.gov/session2009/lists/" + link
                    with self.lxml_context(bill_page_url) as bill_page:
                        splitted_link = link.split("=")
                        bill_number = splitted_link[-1]
                        bill_id = bill_page.cssselect('a[class="headerlink"]')
                        bill_id = bill_id[0]
                        bill_id = bill_id.text_content()
                        bill_title = bill_page.cssselect('td[style="color:Black"]')
                        bill_title = bill_title[0]
                        bill_title = bill_title.text_content()
                        bill = Bill(session, chamber, bill_id, bill_title)
                        bill.add_source(bill_page_url)
                        
                        actions_table_list = bill_page.cssselect('table[rules="all"]')
                        actions_table = actions_table_list[0]
                        action_elements = actions_table.cssselect('tr')
                        for ae in action_elements:
                            action_element_parts = ae.cssselect('td')
                            action_date = action_element_parts[0]
                            actor_house = action_element_parts[1]
                            action_text = action_element_parts[2]
                            
                            match = re.search("committee(\(s\))? on [A-Z]{3}((/|-)[A-Z]{3})?", action_text)
                            
                            if(match != None):
                                print match.group(0)
                            elif(actor_house == 'D'):
                                pass
                            elif (actor_house == 'S'):
                                pass
                            else:
                                pass
                                                           
                            #bill.add_action(actor, action_text, dt.datetime.strptime(action_date, '%m/%d/%Y'))
                        
                        versions_page_url = "http://www.capitol.hawaii.gov/session2009/getstatus.asp?query=" \
                         + type + bill_number + "&showtext=on&currpage=1"
                         
                        with self.lxml_context(versions_page_url) as versions_page:
                            versions_elements = versions_page.cssselect('span[class="searchtitle"]')
                            for ve in versions_elements:
                                element_text = ve.text_content()
                                bill_version_url = "http://www.capitol.hawaii.gov/session2009/Bills/" + element_text
                                version_name = element_text.rstrip("_.HTM")
                                bill.add_version(version_name, bill_version_url)
                            
            

    def scrape_session_old(self, chamber, session):
        pass