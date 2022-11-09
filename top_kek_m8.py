import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
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
addr_field = st.text_input("Name for 'Address' Field?", value="Address")
uploaded_file = st.file_uploader("Choose a Processed Book", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    #ecr_list = ['cape_exterior_condition_rating','cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}','cape_exterior_condition_rating_image_url','cape_roof_condition_rating_date']
    #loc_factors_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}','cape_parcel_distance_to_coastline', 'cape_parcel_distance_to_highway','cape_parcel_distance_to_lake', 'cape_parcel_distance_to_powerline', 'cape_parcel_distance_to_railway', 'cape_parcel_distance_to_river','cape_roof_condition_rating_date']
    #pool_list = ['cape_pool_condition_rating','cape_pool_presence','cape_pool_structure_type','cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}', 'cape_pool_condition_rating_image_url','cape_roof_condition_rating_date']
    #acc_struct_list = ['cape_accessory_structure_count','cape_accessory_structure_roof_condition_rating','cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}','cape_roof_condition_rating_date']
    #roof_list= ['cape_roof_condition_rating', 'cape_roof_condition_rating_date','cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}', 'cape_roof_condition_rating_image_url']
    #tree_overhang_list = ['cape_tree_overhang','cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}','cape_tree_overhang_image_url','cape_roof_condition_rating_date']
    #yard_list = ['cape_yard_debris_coverage_pct', 'cape_yard_debris_coverage_sqft', 'cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}','cape_yard_debris_coverage_pct_image_url','cape_roof_condition_rating_date']
    #summary_list = ['cape_response_status','cape_primary_structure_latitude', 'cape_primary_structure_longitude',f'{addr_field}','cape_property_condition_report_url', 'cape_exterior_condition_rating','cape_roof_condition_rating','cape_roof_condition_rating_date','cape_roof_condition_rating_image_url','cape_accessory_structure_count','cape_accessory_structure_roof_condition_rating','cape_tree_overhang','cape_yard_debris_coverage_pct', 'cape_yard_debris_coverage_sqft','cape_roof_solar_panel', 'cape_liquidity_score']
    #summary_list = df.columns.values.tolist()


    #pool_df = df[pool_list].copy()
    #pool_df.rename(columns = {'cape_pool_condition_rating_image_url':'url'}, inplace = True)

    #roof_df = df[roof_list].copy()
    #roof_df.rename(columns = {'cape_roof_condition_rating_image_url':'url'}, inplace = True)

    #tree_overhang_df = df[tree_overhang_list].copy()
    #tree_overhang_df.rename(columns = {'cape_tree_overhang_image_url':'url'}, inplace = True)

    #yard_df = df[yard_list].copy()
    #yard_df.rename(columns = {'cape_yard_debris_coverage_pct_image_url':'url'}, inplace = True)

    propertysummary_df = df.copy()
    propertysummary_df.rename(columns = {'cape_roof_condition_rating_image_url':'url'}, inplace = True)

    #location_factors_df = df[loc_factors_list].copy()
    
    #df_options = {"EVERYTHING": propertysummary_df.columns.values.tolist()}
    #option = st.selectbox(
    #'Pick a set of attributes',
    #list(df_options.keys()))
    #chosen_df = df_options[option]

    #st.write('You selected:', option)

    #filtered_df = st.dataframe(filter_dataframe(chosen_df),use_container_width=True)
    filtered_df = filter_dataframe(propertysummary_df)
    st.write(filtered_df)
    filtered_df2 = filtered_df['url'].to_list()
    st.info("PICK FILTERS, SELECT APPROPRIATE COLUMNS AND TINKER WITH THE DATAFRAME, THEN ENTER THE NUMBER OF IMAGES YOU NEED.")
    #all_imgs = filtered_df['url'].to_list()
    max_imgs = len(filtered_df2)
    n = st.number_input('Number of Images to Display', min_value=1, max_value=max_imgs, value=1)
    size = st.number_input('Image Width in pixels, default 400', min_value=1, max_value=1000, value=400)
    #n_images = all_imgs[:n]
    
    #print(n, n_images)
    for i in range(n):
        #lat = filtered_df.loc[i,'cape_primary_structure_latitude']
        #long = filtered_df.loc[i,'cape_primary_structure_longitude']
        #long = filtered_df['cape_primary_structure_longitude'][i]
        #coords = f'{lat},{long}'
        #geolocator = Nominatim(user_agent="geoapiExercises")
        #location = geolocator.reverse(coords)
        #address = location.raw['address']
        #city = address.get('town', '')
        #state = address.get('state', '')
        #country = address.get('country', '')
        #code = address.get('country_code')
        #zipcode = address.get('postcode')
        st.image(filtered_df2[i],caption=f"Imagery Date: {filtered_df.iloc[i]['cape_roof_condition_rating_date']}", width=size)
        #count += 1
        st.download_button(
            label="Download image",
            data=filtered_df2[i],
            file_name=f"{i}.png",
          )
    
    st.info("HAVE FEEDBACK? WAS THIS USEFUL? LET ME KNOW!")

    locations = filtered_df.copy()
    locations2 = locations.rename(columns = {'cape_primary_structure_latitude':'lat', 'cape_primary_structure_longitude': 'long'}, inplace = True)

    st.map(locations2)
    st.write(locations2)