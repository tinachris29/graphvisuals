# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Input Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

csv_df, json_data, json_df = None, None, None

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    try:
        csv_df = pd.read_csv("data.csv")
        csv_df.columns = [c.strip() for c in csv_df.columns]
        if not {"Category", "Value"}.issubset(set(csv_df.columns)):
            st.error("'data.csv' must have columns: Category, Value")
            csv_df = None
        else:
            st.success("Loaded data.csv ✅")
            st.dataframe(csv_df, use_container_width = True)
    except Exception as e:
        st.error(f"Error reading data.csv: {e}")
else:
    st.warning("'data.csv' is missing or empty.")

if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
    try:
        f = open("data.json", "r")
        json_data = json.load(f)
        f.close()
        
        if isinstance(json_data, dict) and "average_screen_time" in json_data:
            avg = json_data["average_screen_time"]
            json_df = pd.DataFrame(list(avg.items()), columns = ["Category", "Value"])
            
        else:
            st.error("'data.json' must include keys: 'Apps' and 'Hours'.")
    except Exception as e:
        st.error(f"Error reading data.json: {e}")
else:
    st.warning("'data.json' is missing or empty.")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Christina's App Data") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.caption("Description: a Static Bar Graph plotting data from JSON. Christina's Top 7 Apps on the x-axis & each App's coresponding Screen Time on the y-axis.")
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
if not (os.path.exists("data.json") and os.path.getsize("data.json")) > 0:
    st.info("JSON not available.")
else:
    f = None
    try:
        f = open("data.json", "r")
        data = json.load(f)

        if "average_screen_time" not in data or not isinstance(data["average_screen_time"], dict):
            st.error("'data.json' must include an 'average_screen_time' dictionary.")
        else:
            avg = data["average_screen_time"]
            df = pd.DataFrame(list(avg.items()), columns = ["App", "Hours"])

            if "top_apps" in data and isinstance(data["top_apps"], list):
                df["App"] = pd.Categorical(df["App"], categories=data["top_apps"], ordered = True)
                df = pd.DataFrame(list(avg.items()), columns = ["App", "Hours"])

                if "top_apps" in data and isinstance(data["top_apps"], list):
                    df["App"] = pd.Categorical(df["App"], categories = data["top_apps"], ordered = True)
                    df = df.sort_values("App")

                    st.bar_chart(df.set_index("App")["Hours"])  #new
                

    except Exception as e:
        st.error(f"Error reading or parsing data.json: {e}")
    finally:
        try:
            if f is not None:
                f.close()
        except:
            pass

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Line Graph of Input Data + Minimum Screen Time Filter") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.caption("Description: a Dynamic Bar Graph plotting data from CSV. Slider for user to select a minimum value of Screen Time to filter the data displayed on the Graph. User's Top 7 Apps on the x-axis & each App's coresponding Screen Time (filtered) on the y-axis.")

# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

if not (os.path.exists("data.csv") and os.path.getsize("data.csv") > 0):
    st.info("CSV not available.")
else:
    try:
        df = pd.read_csv("data.csv")
        df.columns = [c.strip() for c in df.columns]
        if not {"Category", "Value"}.issubset(df.columns):
            st.error("'data.csv' must have columns: Category, Value")
        else:
            df["Category"] = (df["Category"]).astype(str)
            df["Value"] = pd.to_numeric(df["Value"], errors = "coerce")
            df = df.dropna(subset = ["Value"])      #new

            if "min_hours" not in st.session_state:
                st.session_state.min_hours = 0.0        #new

            st.session_state.min_hours = st.slider(     #new
                "Minimum Screen Time (hours):",
                min_value = 0.0,
                max_value = 24.0,
                value = float(st.session_state.min_hours),
                step = 0.5,
                help = "Show only apps with Screen Time at or above this value."
                )

            filtered = df[df["Value"] >= st.session_state.min_hours].copy()

            if filtered.empty:
                st.warning("No rows match the current minimun hours. Please lower the slider.")
            else:
                filtered = filtered.sort_values("Category")
                st.line_chart(filtered.set_index("Category")["Value"])
               
                
    except Exception as e:
        st.error(f"Error reading data.csv: {e}")
            


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Scatter Chart of Input Data + Selected Apps Filter") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.caption("Description: a Dynamic Scatter Chart plotting data from CSV. Multiselect for user to select which Apps to display on the Graph. User's Top Apps (filtered) on the x-axis & each App's coresponding Screen Time on the y-axis.")

# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

if not (os.path.exists("data.csv") and os.path.getsize("data.csv") > 0):
    st.info("CSV not available.")
else:
    try:
        df = pd.read_csv("data.csv")
        df.columns = [c.strip() for c in df.columns]
        if not {"Category", "Value"}.issubset(df.columns):
            st.error("'data.csv' must have columns: Category, Value")
        else:
            df["Category"] = (df["Category"]).astype(str)
            df["Value"] = pd.to_numeric(df["Value"], errors = "coerce")
            df = df.dropna(subset = ["Value"])

            if "selected_apps_scatter" not in st.session_state:
                st.session_state.selected_apps_scatter = sorted(df["Category"].unique().tolist())


            st.session_state.selected_apps_scatter = st.multiselect(       #new
                "Choose which Apps to include in the Scatter Plot:",
                options = sorted(df["Category"].unique().tolist()),
                default = st.session_state.selected_apps_scatter,
                )

            filtered = df[df["Category"].isin(st.session_state.selected_apps_scatter)].copy()
                                                                                             

            if filtered.empty:
                st.warning("No data to plot. Please select at least one app.")
            else:
               filtered = filtered.reset_index(drop = True)     #new
               filtered["App_Index"] = range(1, len(filtered) +1)

               st.scatter_chart(        #new
                   data = filtered,
                   x = "App_Index",
                   y = "Value",
                   )

    except Exception as e:
        st.error(f"Error reading data.csv: {e}")
            





