
from .base import BaseAgent
class OutreachContentAgent(BaseAgent):
    def run(self, inputs):
        leads = inputs.get('ranked_leads') or []
        persona = inputs.get('persona','SDR'); tone = inputs.get('tone','friendly')
        self.log('Generating content persona=', persona, 'tone=', tone)
        messages = []
        for l in leads:
            body = f"Hi {l.get('contact')},\n\nQuick note — I saw {l.get('company')} uses {', '.join(l.get('technologies',[]))}. We've helped similar teams shorten analysis time. 15 mins?\n\nBest, SDR Team"
            messages.append({'lead': l.get('contact'), 'email': l.get('email'), 'email_body': body})
        return {'messages': messages}
