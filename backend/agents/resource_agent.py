import pandas as pd


class ResourceAgent:

    def __init__(self):
        self.hospitals = pd.read_csv("database/seed/hospitals.csv")
        self.shelters = pd.read_csv("database/seed/shelters.csv")
        self.contacts = pd.read_csv("database/seed/emergency_contacts.csv")

    def get_resources(self, user_query):

        query = user_query.lower()

        result = ""

        # --------------------
        # Hospitals
        # --------------------

        if any(word in query for word in ["hospital","doctor","clinic","medical"]):

            result += "🏥 Hospitals\n\n"

            filtered = self.hospitals

            print("User Query:", query)
            for location in self.hospitals["Location"].unique():
                print("Checking location:", location)
                if location.lower() in query:
                    print("Matched:", location)
                    filtered = self.hospitals[
                        self.hospitals["Location"].str.lower() == location.lower()
                    ]

            if filtered.empty:
                result += "No hospitals found.\n"

            else:

                for _, row in filtered.iterrows():

                    result += (
                        f"**{row['Hospital']}**\n\n"
                        f"📍 {row['Location']}\n\n"
                        f"📞 {row['Phone']}\n\n"
                    )

            return result

        # --------------------
        # Shelters
        # --------------------

        if any(word in query for word in ["shelter","camp","relief camp","evacuation"]):

            result += "🏠 Shelters\n\n"

            filtered = self.shelters

            for location in self.shelters["Location"].unique():

                if location.lower() in query:
                    filtered = self.shelters[
                        self.shelters["Location"].str.lower() == location.lower()
                    ]

            if filtered.empty:
                result += "No shelters found.\n"

            else:

                for _, row in filtered.iterrows():

                    result += (
                        f"**{row['Shelter']}**\n\n"
                        f"📍 {row['Location']}\n\n"
                        f"👥 Capacity: {row['Capacity']}\n\n"
                    )

            return result

        # --------------------
        # Emergency Contacts
        # --------------------

        if (
            "contact" in query
            or "helpline" in query
            or "emergency number" in query
            or "emergency contact" in query
        ):

            result += "☎ Emergency Contacts\n\n"

            for _, row in self.contacts.iterrows():

                result += (
                    f"**{row['Service']}** : {row['Number']}\n\n"
                )

            return result

        return "Please ask for hospitals, shelters, or emergency contacts."