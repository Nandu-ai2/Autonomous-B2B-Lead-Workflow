
from .base import BaseAgent
class ScoringAgent(BaseAgent):
    def run(self, inputs):
        leads = inputs.get('enriched_leads') or []
        scoring = inputs.get('scoring_criteria') or self.step.get('inputs',{}).get('scoring_criteria',{})
        self.log('Scoring with criteria', scoring)
        ranked = []
        for l in leads:
            score = 0
            techs = l.get('technologies',[])
            if 'aws' in techs: score += 15
            if 'stripe' in techs: score += 5
            if 'VP' in l.get('role',''): score += 10
            ranked.append({**l, 'score': score})
        ranked.sort(key=lambda x: x['score'], reverse=True)
        return {'ranked_leads': ranked}
