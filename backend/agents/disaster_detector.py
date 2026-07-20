from backend.utils.helper import get_llm


class DisasterDetector:

    def __init__(self):
        self.llm = get_llm()

    def detect_disaster(self, user_query):

        prompt = f"""
You are a disaster classifier.

Identify the disaster mentioned or strongly implied in the user's query.

Choose ONLY from:

Flood
Earthquake
Cyclone
Fire
Tsunami
Landslide
Heatwave

Examples:

Heavy rain, water entering houses -> Flood

Ground shaking -> Earthquake

Strong winds and storm -> Cyclone

Huge sea waves -> Tsunami

Very high temperature -> Heatwave

If unsure return ONLY:

Unknown

Return ONLY ONE WORD.

User Query:

{user_query}
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()