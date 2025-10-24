# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please enter your Top 7 most used Apps (does not have to be in order) & the Screen Time (in hours) for each App below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    category_inputs = []
    value_inputs = []
    for i in range(7):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
        category_inputs.append(st.text_input(f"Enter App #{i+1}:", key = f"app_{i}"))
        value_inputs.append(st.text_input(f"Enter the corresponding Screen Time #{i+1} (hours):", key = f"time_{i}"))

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        rows = []
        for i, app in enumerate(category_inputs):
            if app and value_inputs[i]:
                try:
                    hours = float(value_inputs[i])
                except ValueError:
                    continue
                rows.append({"Category": app, "Value": hours})

        if rows:
            file_has_data = os.path.exists('data.csv') and os.path.getsize('data.csv') > 0
            pd.DataFrame(rows).to_csv('data.csv', mode = 'a', header = not file_has_data, index = False)
            
            st.success("Your data has been submitted!")
            st.write("You entered:")
            st.dataframe(pd.DataFrame(rows))

        else:
            st.warning("No valid (App, Screen Time) pairs were entered. PLease check if the hours are numeric.")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
