import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
from query import MAIN_QUERY

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=3600, show_spinner=False, persist=True)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    #rows = [dict(row) for row in rows_raw]
    local_df = rows_raw.to_dataframe()

    return local_df

df = run_query(MAIN_QUERY)



st.title("Hackathon Google - Promos Data")

dynamic_filters = DynamicFilters(df=df, filters=['category_name','retailer_name', 'store_name', 'full_date', 'product_name', 'ean_sku_code', 'is_promo_price', 'is_other_promo'])

dynamic_filters.display_filters(location='sidebar')

dynamic_filters.display_df()

def filter_chart(dataset : pd.DataFrame ) -> pd.DataFrame:
    dataset['num_promos'] = dataset['product_other_promotions'].apply(lambda x: len(x))
    filter_products = st.multiselect('Select products to filter graphics', dataset['product_name'].unique())

    if filter_products:
        dataset = dataset[dataset['product_name'].isin(filter_products)]
    return dataset

#filtered = filter_chart(df)

# st.write('Promo prices by product')

# st.line_chart(filter_chart(df), x="full_date", y="product_promo_price", color="product_name")

# st.write('Other promos by product')

# st.line_chart(filtered, x="full_date", y="num_promos", color="product_name")
