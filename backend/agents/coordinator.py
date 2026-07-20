from backend.utils.helper import get_llm


class CoordinatorAgent:

    def __init__(self):
        self.llm = get_llm()

    def decide_agent(self, user_query):

        prompt = f"""
You are an intelligent routing agent.

Choose ONLY ONE of these:

preparedness
emergency
information
resource

Rules

Questions about:

• preparing
• prevention
• before disaster

→ preparedness

Questions about:

• help
• rescue
• current disaster
• immediate action

→ emergency

Questions about:

• hospital
• shelter
• emergency number
• contact
• helpline

→ resource

Questions about:

• what is
• explain
• causes
• why

→ information

Return ONLY ONE WORD.

User:

{user_query}
"""

        response = self.llm.invoke(prompt)

        return response.content.strip().lower()