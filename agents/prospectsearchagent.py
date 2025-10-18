
from .base import BaseAgent
class ProspectSearchAgent(BaseAgent):
    def run(self, inputs):
        icp = inputs.get('icp', {})
        signals = inputs.get('signals', [])
        self.log('ProspectSearch: ICP=', icp, 'signals=', signals)
        leads = []
        for i in range(4):
            leads.append({
                'company': f'TestCo-{i}',
                'contact_name': f'Pat Prospect{i}',
                'email': f'pat{i}@testco.com',
                'linkedin': f'https://linkedin.com/in/pat-prospect{i}',
                'signal': signals[i%len(signals)] if signals else 'none'
            })
        return {'leads': leads}
