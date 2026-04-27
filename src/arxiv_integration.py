import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time

class ArxivIntegration:
    def __init__(self):
        self.base_url = "https://export.arxiv.org/api/query?"
        
    def search_papers(self, query, max_results=5):
        params = {
            'search_query': query,
            'start': 0,
            'max_results': max_results
        }
        url = self.base_url + urllib.parse.urlencode(params)
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ResearchAssistant/1.0'})
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=15) as response:
                        if response.status == 429:
                            time.sleep(3 * (attempt + 1))
                            continue
                        data = response.read().decode('utf-8')
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(3)
            
            root = ET.fromstring(data)
            papers = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                paper = {
                    'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                    'authors': [author.find('{http://www.w3.org/2005/Atom}name').text 
                               for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                    'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                    'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                    'pdf_url': entry.find('{http://www.w3.org/2005/Atom}id').text.replace('abs', 'pdf') + '.pdf'
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            return f"Error searching arXiv: {str(e)}"
    
    def get_paper_by_id(self, arxiv_id):
        return self.search_papers(f"id:{arxiv_id}", max_results=1)
    
    def search_by_category(self, category, max_results=5):
        return self.search_papers(f"cat:{category}", max_results=max_results)
