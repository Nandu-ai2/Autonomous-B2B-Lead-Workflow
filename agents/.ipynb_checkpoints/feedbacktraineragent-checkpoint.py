
from .base import BaseAgent
class FeedbackTrainerAgent(BaseAgent):
    def run(self, inputs):
        responses = inputs.get('responses') or []
        cfg = inputs.get('current_config') or {}
        self.log('FeedbackTrainer analyzing', len(responses), 'responses')
        replies = [r for r in responses if r.get('action') == 'replied']
        open_rate = len([r for r in responses if r.get('action') == 'opened']) / max(1, len(responses))
        recs = []
        if len(replies)/max(1,len(responses)) < 0.2:
            recs.append({'action':'subject_test','suggestion':'A/B test benefit-led subject lines'})
        if open_rate < 0.3:
            recs.append({'action':'send_time','suggestion':'Try 9-11am ET'})
        self.log('Recommendations', recs)
        return {'recommendations': recs}
