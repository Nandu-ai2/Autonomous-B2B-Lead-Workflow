
from .base import BaseAgent
import uuid
class OutreachExecutorAgent(BaseAgent):
    def run(self, inputs):
        messages = inputs.get('messages') or []
        self.log('Executing outreach (mock)', len(messages))
        sent = []
        campaign_id = str(uuid.uuid4())
        for m in messages:
            sent.append({'to': m.get('email'), 'status': 'mock_sent', 'message_id': str(uuid.uuid4())})
        return {'sent_status': sent, 'campaign_id': campaign_id}
