import os


import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = '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'

destination_template = PromptTemplate(
    input_variables=[
        'destination',  # User's desired destination
        'interests',  # List of user's interests (e.g., history, nature, food)
        'budget',  # User's budget for the trip
        'start_date',  # User's preferred start date (formatted as YYYY-MM-DD)
        'end_date',  # User's preferred end date (formatted as YYYY-MM-DD)
        'num_people',  # Number of people traveling
        'current_day',  # Day currently generating itinerary for (starts at 1)
    ],
    template="""
      **Based on the user's input:**

      * Destination: {destination}
      * Interests: {interests}
      * Budget: {budget}
      * Start date: {start_date}
      * End date: {end_date}
      * Number of people: {num_people}
      * Current day: {current_day}

      **Leveraging insights from travel experts and considering UN SDGs, generate a detailed itinerary for Day {current_day} of this trip, incorporating the following:**

      * **Places to visit:**
        * Suggest engaging activities and locations aligned with user interests and UN SDGs, considering travel time, logistics, and budget constraints.
        * Provide brief descriptions with historical/cultural significance (where applicable).
        * Recommend estimated times for each activity to ensure a balanced and fulfilling experience.
      * **Accommodation:**
        * Suggest hotels or lodging options that suit the budget, preferences, and proximity to planned activities.
        * Include estimated costs for accommodation.
      * **Transportation:**
        * Recommend suitable modes of transportation between locations, considering cost, time, convenience, and budget.
        * Provide estimated costs for transportation.
      * **Restaurants:**
        * Suggest budget-friendly restaurants aligned with user preferences and local cuisine.
        * Include estimated costs for meals.

      **Remember to prioritize affordability, cultural immersion, and sustainability throughout the itinerary.**

      **Please provide a clear and concise itinerary for Day {current_day}, addressing all aspects of the day.**

      Provide this output in table format with column time, name, location, activity, estimated price in indian rupees, time to reach from previous location in hours.
    """,
)

# Memory
memory = ConversationBufferMemory(input_key="destination", memory_key='conversation_history')

# LLM
llm = OpenAI(temperature=0.5)
itinerary_chain = LLMChain(
    llm=llm,
    prompt=destination_template,
    memory=memory,
    output_key='itinerary',
    verbose=True
)

def generate_itinerary():
    """
    Collects user input, generates an itinerary for each day, and presents it to the user.
    """

    with st.form("itinerary_form"):
        destination = st.text_input("Enter your desired destination:")
        interests = st.multiselect("Select your interests:", ["History", "Nature", "Food", "Adventure", "Relaxation"])
        budget = st.number_input("Enter your budget for this trip:")
        start_date = st.date_input("Enter your preferred start date:")
        end_date = st.date_input("Enter your preferred end date:")
        num_people = st.number_input("How many people are traveling?")

        submit_button = st.form_submit_button("Generate Itinerary")

        if submit_button:
            user_input = {
                # Extract and format user input values
                'destination': destination,
                'interests': interests,
                'budget': budget,
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                'num_people': num_people,
                'current_day': 1  # Start with Day 1
            }

            # Initialize variables for day generation
            current_day = 1
            itinerary = ""

            while current_day <= (end_date - start_date).days + 1:
                # Update the 'current_day' key in user_input for each iteration
                user_input['current_day'] = current_day

                # Generate itinerary for the current day using the LLM chain
                daily_itinerary = itinerary_chain.run(user_input)

                # Append the daily itinerary to the main itinerary
                itinerary += f"\n**Day {current_day} Itinerary:**\n{daily_itinerary}"

                # Add next button/logic here

                current_day += 1  # Go to next day

            # Present the complete itinerary to the user
                # Generate itinerary using the LLM chain
            # itinerary = itinerary_chain.run(user_input)
            # Present the itinerary to the user
            st.write("**Your personalized itinerary:**")
            st.write(itinerary)  # directly write the itinerary
if __name__ == '__main__':
    st.title('Travel Itinerary Planner')
    # generate_itinerary_button = st.button("Generate Itinerary")
    # if generate_itinerary_button:
    itinerary = generate_itinerary()  # Capture the returned value
    if itinerary:
        st.write(itinerary)
        # print(itinerary)  # Debugging step to check the type and content of 'itinerary'
        # st.json(itinerary['itinerary'])  # Display the itinerary
# st.write("Saving Streamlit app as HTML file...")
# st.write("Please wait, this may take a moment.")
# st.write("(You can close this window after the HTML file is saved.)")

with open("streamlit_app.html", "w") as f:
    f.write("<html>\n<body>\n")
    f.write("<iframe src='http://localhost:8501/' width='100%' height='600px'></iframe>\n")
    f.write("</body>\n</html>\n")
        
        
        
       