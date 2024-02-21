from website import create_app
from flask import Flask, render_template, request
from website import create_app as create_streamlit_app
import numpy as np
import pandas as pd

app = Flask(__name__)

# try:
#     city_data = pd.read_pickle('./website/city.pkl')
#     print(city_data.keys())
#     places_data = pd.read_pickle('places.pkl')
#     similarity_data = pd.read_pickle('similarity.pkl')
# except Exception as e:
#     print("Error loading pickled files:", e)
#     city_data = {}
#     places_data = {}


# @app.route('/recommend', methods=['POST'])
# def recommend():
#     user_input = request.form.get('city_input')
#     index = np.where(city_data['City'] == user_input)[0][0]
#     similar_cities = sorted(list(enumerate(similarity_data[index])), key=lambda x: x[1], reverse=True)[1:6]
  
#     data = []

#     for i in similar_cities:
#         city_name = city_data.iloc[i[0]]['City']
#         city_desc = city_data.iloc[i[0]]['City_desc']
#         ideal_duration = city_data.iloc[i[0]]['Ideal_duration']
#         ratings = city_data.iloc[i[0]]['Ratings']

#         # Get recommended places for the current city
#         recommended_places = places_data[places_data['City'] == city_name].sort_values(by='Ratings', ascending=False).head(5)
#         place_data = []
#         for _, place in recommended_places.iterrows():
#             place_data.append((place['Place'], place['Place_desc'], place['Ratings'], place['Distance']))

#         data.append((city_name, city_desc, ideal_duration, ratings, place_data))

#     return render_template('recommend.html', data=data)

st_app = create_streamlit_app()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)