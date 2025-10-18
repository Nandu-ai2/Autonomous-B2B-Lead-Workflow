
from .base import BaseAgent
class ResponseTrackerAgent(BaseAgent):
    def run(self, inputs):
        campaign_id = inputs.get('campaign_id')
        self.log('Tracking (mock) for campaign', campaign_id)
        responses = []
        responses.append({'email':'pat0@testco.com','action':'opened'})
        responses.append({'email':'pat3@testco.com','action':'replied','text':'Interested, send more info'})
        return {'responses': responses}
