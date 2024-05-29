import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#fucntion to load Gemini Pro Vision 
model = genai.GenerativeModel('gemini-1.5-flash-latest')


prompt=f"""Consider you're professional and
 you have the ability to tell the Mitigation strategy for the emission of a company.
 I need  top 10 mitigation strategy only which will be applicable for the particular(Precise) company under the given budget limit. 
 It should be in single lined.The output shouldn't contains any * symbols and # symbols
 """
def get_gemini_response(user_input ,prompt):
    response=model.generate_content([user_input,prompt])
    return response.text


def process_entries(result):
    
    return result

# Streamlit app
st.title("Company Information Form")

company_name = st.text_input("Company Name")
industry_name = st.text_input("Industry Name")

scope1_options = ["Manufacturing emission", "fugitive emissions", "vehicles emission", "warehouses","Gas combustion( natural gas, diesel, gasoline)","Mobile combustion (ethanol, bio-diesel)", "stationary combustion (Bio-mass)","Process Emissions(chemical/metal prodcution)","Emissions from on-site generation","Logistics", "Dealer", "Suppliers","Biogenic Emissions(biomass combustion,land-use changes,organic waste decomposition)"]
scope2_options = ["Manufacturing Emission", "Transportation Emission"]
scope3_options = ["Solar Emission"]

scope1_selected = st.multiselect("Scope 1", scope1_options)
scope2_selected = st.multiselect("Scope 2", scope2_options)
scope3_selected = st.multiselect("Scope 3", scope3_options)

budget = st.text_input("Budget")

def user_input_generator(company_name, industry_name, scope1_emission, scope2_emission,scope3_emission, budget):
    txt = f"""My company name is {company_name} and we are in the {industry_name} industry. We have scope 1 emissions such as {', '.join(scope1_emission)}.
        Scope 2 emissions include {', '.join(scope2_emission)} and Scope3 emissions include {', '.join(scope3_emission)} the budget is ${budget} million.
        """ 
    return txt

def calculate_height(text, line_height=20):
    lines = max(1, len(text.split('\n')))
    return lines * line_height

def cleaned_text(text):
    cleaned_text = text.replace('#', '').replace('*', '')
    return cleaned_text

if st.button("Submit"):
    user_input = user_input_generator(company_name,industry_name,scope1_selected,scope2_selected,scope3_selected,budget)
    result = get_gemini_response(user_input ,prompt)
    cleaned_result=cleaned_text(result)
    hei=calculate_height(cleaned_result)
    st.text_area("Output:-", cleaned_result, height=hei+hei)

