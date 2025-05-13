import streamlit as st
import pandas as pd

# Title
st.title("Drilling Cost Optimization Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload Cost Optimization Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Constants
    mud_cost_per_bbl = 100
    haul_off_cost_per_bbl = 20

    # Calculations
    df["Mud_Cost"] = df["Total_Dil"] * mud_cost_per_bbl
    df["Haul_Off_Cost"] = df["Haul_OFF"] * haul_off_cost_per_bbl
    df["Dilution_Cost_Per_Foot"] = df["Mud_Cost"] / df["IntLength"]
    df["Haul_Off_Cost_Per_Foot"] = df["Haul_Off_Cost"] / df["IntLength"]
    df["Cumulative_Cost"] = df["Mud_Cost"] + df["Haul_Off_Cost"]
    df["Cost_Per_Day"] = df["Cumulative_Cost"] / df["DOW"]

    # Sidebar filters
    st.sidebar.header("Filter Wells")
    operator_filter = st.sidebar.multiselect("Select Operator", options=df["Operator"].dropna().unique())
    contractor_filter = st.sidebar.multiselect("Select Contractor", options=df["Contractor"].dropna().unique())

    if operator_filter:
        df = df[df["Operator"].isin(operator_filter)]
    if contractor_filter:
        df = df[df["Contractor"].isin(contractor_filter)]

    # Display dataframe
    st.subheader("Calculated Cost Metrics")
    st.dataframe(df[[
        "Well_Job_ID", "Operator", "Contractor", "Total_Dil", "Haul_OFF", "IntLength", "DOW",
        "Mud_Cost", "Haul_Off_Cost", "Dilution_Cost_Per_Foot",
        "Haul_Off_Cost_Per_Foot", "Cumulative_Cost", "Cost_Per_Day"
    ]])

    # Optional charts
    st.subheader("Cost Per Day Distribution")
    st.bar_chart(df.set_index("Well_Job_ID")["Cost_Per_Day"])

    st.subheader("Dilution Cost Per Foot by Well")
    st.line_chart(df.set_index("Well_Job_ID")["Dilution_Cost_Per_Foot"])

    st.subheader("Haul-Off Cost Per Foot by Well")
    st.line_chart(df.set_index("Well_Job_ID")["Haul_Off_Cost_Per_Foot"])

    # Export to Excel
    st.subheader("Download Results")
    output_df = df[[
        "Well_Job_ID", "Operator", "Contractor", "Total_Dil", "Haul_OFF", "IntLength", "DOW",
        "Mud_Cost", "Haul_Off_Cost", "Dilution_Cost_Per_Foot",
        "Haul_Off_Cost_Per_Foot", "Cumulative_Cost", "Cost_Per_Day"
    ]]
    output_excel = output_df.to_excel(index=False, engine='openpyxl')
    st.download_button("Download Data as Excel", data=output_excel, file_name="drilling_cost_report.xlsx")

else:
    st.info("Please upload a drilling cost optimization report in Excel format.")
