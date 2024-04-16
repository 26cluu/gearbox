import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from ISLP import load_data
from ISLP.models import (ModelSpec as MS, summarize, poly)
import math

st.title("Car Price Model Predictor")


@st.cache_data
def get_df():
   df = pd.read_csv("car_prices.csv", on_bad_lines = "warn")
   df = df.drop(['model', 'vin', 'trim', 'state', 'interior', 'seller', 'mmr', 'saledate'], axis=1)
   df = df.dropna(subset = ["year", "condition", "odometer", "sellingprice", "make", "transmission", "body", "color"])

   make_dummies = pd.get_dummies(df['make'], prefix_sep='_', prefix='make')
   transmission_dummies = pd.get_dummies(df['transmission'], prefix_sep='_', prefix='transmission')
   body_dummies = pd.get_dummies(df['body'], prefix_sep='_', prefix='body')
   color_dummies = pd.get_dummies(df['color'], prefix_sep='_', prefix='color')

   df = pd.concat([df, make_dummies, transmission_dummies, body_dummies, color_dummies], axis=1)

   features = ['year', 'condition', 'odometer'] + list(make_dummies.columns) + list(transmission_dummies.columns) + list(body_dummies.columns) + list(color_dummies.columns)
   spec = MS(features).fit(df)

   x = spec.transform(df)
   y = df['sellingprice']

   model1 = sm.OLS(y, x).fit()

   return df, spec, model1


def predict(df, spec, model, year, maker, body, transmission, condition, mileage, color):
   column_names = df.columns
   df_new = pd.DataFrame(columns = column_names)
   df_new = df_new.drop(['sellingprice'], axis=1)
   zeros_list = [0] * 160

   df_new.loc[0] = [year, maker, body, transmission, condition, mileage, color] + zeros_list
   df_new.loc[0, ('make_' + maker)] = 1
   df_new.loc[0, ('color_' + color)] = 1
   df_new.loc[0, ('body_' + body)] = 1
   df_new.loc[0, ('transmission_' + transmission)] = 1
   
   new_X = spec.transform(df_new)
   return model.get_prediction(new_X).predicted_mean

df, spec, model = get_df()


with st.form("my_form"):
    year = st.slider("What year was the car produced?", 1960, 2024, 2000)
    maker = st.selectbox(
        "Who's the maker of the car?",
        ('Kia', 'BMW', 'Volvo', 'Nissan', 'Chevrolet', 'Audi', 'Ford',
       'Cadillac', 'Acura', 'Lexus', 'Hyundai', 'Buick', 'Infiniti',
       'Jeep', 'Mercedes-Benz', 'Mitsubishi', 'Mazda', 'MINI',
       'Land Rover', 'Lincoln', 'Jaguar', 'Volkswagen', 'Toyota',
       'Subaru', 'Scion', 'Porsche', 'Dodge', 'FIAT', 'Chrysler',
       'Ferrari', 'Honda', 'GMC', 'Ram', 'smart', 'Bentley', 'Pontiac',
       'Saturn', 'Maserati', 'Mercury', 'HUMMER', 'Saab', 'Suzuki',
       'Oldsmobile', 'Rolls-Royce', 'Isuzu', 'Plymouth', 'Tesla',
       'Aston Martin', 'Geo', 'Fisker', 'Daewoo', 'Lamborghini', 'Lotus')
    )

    body_type = st.selectbox(
        "What's the style of the car?",
        ('SUV', 'Sedan', 'Convertible', 'Coupe', 'Wagon', 'Hatchback',
       'Crew Cab', 'G Coupe', 'G Sedan', 'Elantra Coupe', 'Genesis Coupe',
       'Minivan', 'Van', 'Double Cab', 'CrewMax Cab', 'Access Cab',
       'King Cab', 'CTS Coupe', 'SuperCrew', 'E-Series Van',
       'Extended Cab', 'SuperCab', 'G Convertible', 'Koup', 'Regular Cab',
       'Quad Cab', 'CTS-V Coupe', 'sedan', 'G37 Convertible', 'Club Cab',
       'Xtracab', 'Q60 Convertible', 'CTS Wagon', 'G37 Coupe', 'Mega Cab',
       'Cab Plus 4', 'Q60 Coupe', 'Beetle Convertible', 'TSX Sport Wagon',
       'Promaster Cargo Van', 'Cab Plus', 'GranTurismo Convertible',
       'CTS-V Wagon', 'Ram Van', 'convertible', 'minivan', 'Transit Van',
       'van', 'regular-cab', 'suv', 'g sedan', 'g coupe', 'hatchback',
       'king cab', 'supercrew', 'g convertible', 'coupe', 'crew cab',
       'wagon', 'e-series van', 'regular cab', 'quad cab',
       'g37 convertible', 'supercab', 'extended cab', 'crewmax cab',
       'double cab', 'genesis coupe', 'access cab', 'mega cab', 'xtracab',
       'beetle convertible', 'cts coupe', 'koup', 'club cab',
       'elantra coupe', 'q60 coupe', 'cts-v coupe', 'transit van',
       'granturismo convertible', 'tsx sport wagon',
       'promaster cargo van', 'q60 convertible', 'cab plus 4',
       'cts wagon')
    )

    transmission = st.radio("Is it an automatic or manual?", ['automatic', 'manual'])

    condition = st.slider("On a scale of 1-5, what condition is the car in?", 0.0, 5.0, 3.0, 0.5)

    mileage = st.slider("How is the mileage looking like?", 0, 200000, 50000, 500)

    color = st.selectbox("Just for fun, what color is the car?", ('white', 'gray', 'black', 'red', 'silver', 'brown', 'beige',
       'blue', 'purple', 'burgundy', 'gold', 'yellow', 'green',
       'charcoal', 'orange', 'off-white', 'turquoise', 'pink', 'lime'))
    st.caption('*ps. color does matter*')


    button = st.form_submit_button("predict")

    if button:
      prediction = predict(df, spec, model, year, maker, body_type, transmission, condition, mileage, color)
      num = round(prediction[0])
      text = "Range: " + str(max(num - 1000, 0)) + " - " + str(num+1000)
      st.subheader(f':{color}[{text}]')
      st.text("Prediced Price: ~$" + str(num))
      





