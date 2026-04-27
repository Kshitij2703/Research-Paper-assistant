from groq import Groq
import re

class CitationManager:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def extract_citations(self, text):
        # Try to find references section
        references_section = self._extract_references_section(text)
        
        if references_section:
            prompt = f"""Extract all citations from this references section. 
For each citation, provide:
- Authors (last name, first initial)
- Year
- Title
- Journal/Conference/Source

References section:
{references_section[:8000]}

Format each citation as:
[N] Author(s), Year, Title, Source"""
        else:
            # Fallback to searching entire text
            prompt = f"""Find and extract all academic citations/references from this paper.
Look for patterns like:
- Author et al. (Year)
- [Number] Author, Year, Title
- References section

Text: {text[:10000]}

Format each citation as:
[N] Author(s), Year, Title, Source"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def _extract_references_section(self, text):
        """Extract the references/bibliography section from paper"""
        # Common reference section headers
        patterns = [
            r'(?i)\n\s*references\s*\n',
            r'(?i)\n\s*bibliography\s*\n',
            r'(?i)\n\s*works cited\s*\n',
            r'(?i)\n\s*literature cited\s*\n'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                # Extract from this point to end (or next major section)
                start = match.end()
                # Try to find where references end (appendix, acknowledgments, etc.)
                end_patterns = [
                    r'(?i)\n\s*appendix',
                    r'(?i)\n\s*acknowledgments?',
                    r'(?i)\n\s*supplementary'
                ]
                end = len(text)
                for end_pattern in end_patterns:
                    end_match = re.search(end_pattern, text[start:])
                    if end_match:
                        end = start + end_match.start()
                        break
                return text[start:end]
        
        return None
    
    def generate_citation(self, paper_info, style="APA"):
        prompt = f"""Generate a {style} citation for this paper:

{paper_info}

Return only the formatted citation."""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_bibliography(self, citations_list):
        prompt = f"""Create a formatted bibliography from these citations:

{citations_list}

Return a properly formatted bibliography."""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
