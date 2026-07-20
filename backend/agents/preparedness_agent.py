import pandas as pd
from backend.utils.helper import get_llm


class PreparednessAgent:

    def __init__(self):
        self.data = pd.read_csv("database/seed/disasters.csv")
        self.llm = get_llm()

    def get_response(self, disaster, user_query):

        disaster = disaster.lower()

        for _, row in self.data.iterrows():

            if row["Disaster"].lower() == disaster:

                prompt = f"""
You are an expert Disaster Preparedness Assistant.

Disaster: {row['Disaster']}

Preparedness Information:
{row['Preparedness']}

User Question:
{user_query}

Instructions:
- Answer naturally.
- Use the preparedness information provided.
- Add practical advice if appropriate.
- Keep the answer under 150 words.
"""

                response = self.llm.invoke(prompt)

                return response.content

        return "Sorry, I don't have preparedness information for that disaster."