import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from fish.models import TrainingSample


def train_lda_from_db():

    samples = TrainingSample.objects.select_related("fish", "food")

    if not samples.exists():
        raise ValueError("No training samples found in database.")

    fish_names = []
    water_types = []
    farm_types = []
    farm_sizes = []
    temperatures = []
    food_names = []

    for s in samples:
        fish_names.append(s.fish.common_name)
        water_types.append(s.water_type)
        farm_types.append(s.farm_type)
        farm_sizes.append(s.farm_size)
        temperatures.append(s.water_temperature)
        food_names.append(s.food.food_name)

    fish_enc = LabelEncoder()
    water_enc = LabelEncoder()
    farm_enc = LabelEncoder()
    food_enc = LabelEncoder()

    fish_encoded = fish_enc.fit_transform(fish_names)
    water_encoded = water_enc.fit_transform(water_types)
    farm_encoded = farm_enc.fit_transform(farm_types)
    food_encoded = food_enc.fit_transform(food_names)

    X = np.column_stack((
        fish_encoded,
        water_encoded,
        farm_encoded,
        farm_sizes,
        temperatures
    ))

    y = food_encoded

    lda = LinearDiscriminantAnalysis()
    lda.fit(X, y)

    return lda, fish_enc, water_enc, farm_enc, food_enc

def predict_food(fish_name, water_type, farm_type, farm_size, temperature):

    lda, fish_enc, water_enc, farm_enc, food_enc = train_lda_from_db()

    try:
        fish_val = fish_enc.transform([fish_name])[0]
    except:
        fish_val = 0

    try:
        water_val = water_enc.transform([water_type])[0]
    except:
        water_val = 0

    try:
        farm_val = farm_enc.transform([farm_type])[0]
    except:
        farm_val = 0

    input_vector = np.array([[fish_val, water_val, farm_val, farm_size, temperature]])

    predicted_class = lda.predict(input_vector)[0]
    probabilities = lda.predict_proba(input_vector)[0]

    confidence = float(np.max(probabilities)) * 100
    predicted_food = food_enc.inverse_transform([predicted_class])[0]

    return predicted_food, round(confidence, 2)