
from .base import BaseAgent
class DataEnrichmentAgent(BaseAgent):
    def run(self, inputs):
        leads = inputs.get('leads') or []
        self.log('Enriching', len(leads), 'leads')
        enriched = []
        for l in leads:
            enriched.append({
                'company': l.get('company'),
                'contact': l.get('contact_name'),
                'role': 'VP Sales' if '1' in l.get('company') else 'Head of Sales',
                'technologies': ['aws','segment'] if '2' in l.get('company') else ['gcp','stripe']
            })
        return {'enriched_leads': enriched}
