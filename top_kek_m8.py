import pandas as pd
import streamlit as st
from streamlit_extras.image_in_tables import table_with_images
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.title("Interacting with Processed CSVs - Images, PDF Reports, etc")

st.write(
    """Interact with Processed Books, quickly filter and view images for PoV usage.
    """
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df

uploaded_file = st.file_uploader("Choose a Processed Book)", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    ecr_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_exterior_condition_rating', 'cape_exterior_condition_rating_image_url']
    loc_factors_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_parcel_distance_to_coastline', 'cape_parcel_distance_to_highway','cape_parcel_distance_to_lake', 'cape_parcel_distance_to_powerline', 'cape_parcel_distance_to_railway', 'cape_parcel_distance_to_river']
    pool_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_pool_condition_rating','cape_pool_presence','cape_pool_structure_type', 'cape_pool_condition_rating_image_url']
    acc_struct_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_accessory_structure_count','cape_accessory_structure_roof_condition_rating']
    roof_list= ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_roof_condition_rating', 'cape_roof_condition_rating_date', 'cape_roof_condition_rating_image_url']
    tree_overhang_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_tree_overhang', 'cape_tree_overhang_image_url']
    yard_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_yard_debris_coverage_pct', 'cape_yard_debris_coverage_sqft', 'cape_yard_debris_coverage_pct_image_url']
    summary_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude','Address', 'City', 'State', 'Zip','cape_property_condition_report_url', 'cape_exterior_condition_rating','cape_roof_condition_rating','cape_roof_condition_rating_date','cape_roof_condition_rating_image_url','cape_accessory_structure_count','cape_accessory_structure_roof_condition_rating','cape_tree_overhang','cape_yard_debris_coverage_pct', 'cape_yard_debris_coverage_sqft','cape_roof_solar_panel', 'cape_liquidity_score']



    pool_df = df[pool_list].copy()
    pool_df.rename(columns = {'cape_pool_condition_rating_image_url':'url'}, inplace = True)

    roof_df = df[roof_list].copy()
    roof_df.rename(columns = {'cape_roof_condition_rating_image_url':'url'}, inplace = True)

    tree_overhang_df = df[tree_overhang_list].copy()
    tree_overhang_df.rename(columns = {'cape_tree_overhang_image_url':'url'}, inplace = True)

    yard_df = df[yard_list].copy()
    yard_df.rename(columns = {'cape_yard_debris_coverage_pct_image_url':'url'}, inplace = True)

    propertysummary_df = df[summary_list].copy()
    propertysummary_df.rename(columns = {'cape_roof_condition_rating_image_url':'url'}, inplace = True)

    location_factors_df = df[loc_factors_list].copy()
    ecr_df = df[ecr_list].copy()
    ecr_df.rename(columns = {'cape_exterior_condition_rating_image_url':'url'}, inplace = True)
    df_options = {"Roof Stuff": roof_df, "Tree Overhang Stuff": tree_overhang_df, "Yard Stuff": yard_df, "Pool Stuff": pool_df, "Property Summary": propertysummary_df, "Location Factors": location_factors_df, "ECR": ecr_df, "EVERYTHING": df}
    option = st.selectbox(
    'Pick a set of attributes',
    list(df_options.keys()))
    chosen_df = df_options[option]

    st.write('You selected:', option)

    st.dataframe(filter_dataframe(chosen_df))

    all_imgs = chosen_df['url'].to_list()

    n = st.number_input('Number of Images to Display', min_value=1, max_value=len(all_imgs), value=1)

    n_images = all_imgs[:n]
    for n in n_images:
        st.image(n, width=400)