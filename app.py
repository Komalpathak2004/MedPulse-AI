from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from PIL import Image

app = Flask(__name__)

# Load the medicine data and similarity matrix
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(medicine):
    try:
        medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
        distances = similarity[medicine_index]
        medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_medicines = []
        for i in medicines_list:
            recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
        return recommended_medicines
    except IndexError:
        return ["No recommendations available"]

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        medicine_name = request.form.get('medicine')
        recommendations = recommend(medicine_name)
    return render_template('index.html', medicines=medicines['Drug_Name'].values, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
