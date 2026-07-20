import pandas as pd
from backend.utils.helper import get_llm


class InformationAgent:

    def __init__(self):
        self.data = pd.read_csv("database/seed/disasters.csv")
        self.llm = get_llm()

    def get_response(self, disaster, user_query):

        disaster = disaster.lower()

        for _, row in self.data.iterrows():

            if row["Disaster"].lower() == disaster:

                prompt = f"""
You are a Disaster Information Assistant.

Disaster:
{row['Disaster']}

Description:
{row['Description']}

User Question:
{user_query}

Instructions:
- Explain clearly in simple language.
- Use the disaster description.
- Add useful facts if appropriate.
- Keep the answer under 150 words.
"""

                response = self.llm.invoke(prompt)

                return response.content

        return "Sorry, I don't have information about that disaster."