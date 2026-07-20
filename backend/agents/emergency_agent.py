import pandas as pd
from backend.utils.helper import get_llm


class EmergencyAgent:

    def __init__(self):
        self.data = pd.read_csv("database/seed/disasters.csv")
        self.llm = get_llm()

    def get_response(self, disaster, user_query):

        disaster = disaster.lower()

        for _, row in self.data.iterrows():

            if row["Disaster"].lower() == disaster:

                prompt = f"""
You are an Emergency Response Assistant.

Disaster:
{row['Disaster']}

Emergency Instructions:
{row['Emergency']}

User Question:
{user_query}

Instructions:
- Give immediate emergency guidance.
- Keep the answer calm and practical.
- Use the emergency instructions provided.
- Keep it under 150 words.
"""

                response = self.llm.invoke(prompt)

                return response.content

        return "Sorry, I don't have emergency information for that disaster."