import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time

# Add this near the top of your script
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add this function near the top of your script
def reset_filters():
    st.session_state.active_filter = None
    st.session_state.active_value = None

# Load data (replace with your actual data loading logic)
@st.cache_data
def load_data(vulnerability_type):
    return pd.DataFrame({
        'Vulnerability ID': [f'{vulnerability_type}-001', f'{vulnerability_type}-002', f'{vulnerability_type}-003', 
                             f'{vulnerability_type}-004', f'{vulnerability_type}-005', f'{vulnerability_type}-006'],
        'Product Name': ['Product A', 'Product B', 'Product A', 'Product C', 'Product B', 'Product D'],
        'Vulnerability': [f'{vulnerability_type} Vuln 1', f'{vulnerability_type} Vuln 2', f'{vulnerability_type} Vuln 3',
                          f'{vulnerability_type} Vuln 4', f'{vulnerability_type} Vuln 5', f'{vulnerability_type} Vuln 6'],
        'Owner': ['Owner 1', 'Owner 2', 'Owner 1', 'Owner 3', 'Owner 2', 'Owner 3'],
        'Due Date': [datetime(2023, 6, 1), datetime(2023, 6, 15), datetime(2023, 7, 1),
                     datetime(2023, 7, 15), datetime(2023, 8, 1), datetime(2023, 8, 15)],
        'Comment': ['Initial finding', 'Under review', 'Patch in progress', 
                    'Awaiting vendor response', 'Scheduled for next sprint', 'Needs prioritization'],
        'CVE ID': ['CVE-2023-0001', 'CVE-2023-0002', 'CVE-2023-0003',
                   'CVE-2023-0004', 'CVE-2023-0005', 'CVE-2023-0006'],
        'Status': ['Open', 'In Progress', 'Open', 'Awaiting Info', 'In Progress', 'Open']
    })

# Update comment in the dataframe
def update_comment(data, update_type, update_value, new_comment):
    if update_type == 'Vulnerability ID':
        data.loc[data['Vulnerability ID'] == update_value, 'Comment'] = new_comment
    elif update_type == 'Owner':
        data.loc[data['Owner'] == update_value, 'Comment'] = new_comment
    elif update_type == 'Product Name':
        data.loc[data['Product Name'] == update_value, 'Comment'] = new_comment
    return data

# Send email notification
def send_email(to_email, subject, body):
    # Implement your email sending logic here
    pass

# Update the filter_data function to handle multiple filters
def filter_data(data, filters):
    filtered_data = data.copy()
    for filter_type, filter_value in filters.items():
        if filter_value:
            if filter_type == 'Owner':
                filtered_data = filtered_data[filtered_data['Owner'] == filter_value]
            elif filter_type == 'Product Name':
                filtered_data = filtered_data[filtered_data['Product Name'] == filter_value]
            elif filter_type == 'Vulnerability ID':
                filtered_data = filtered_data[filtered_data['Vulnerability ID'] == filter_value]
    return filtered_data

# Main app
def main():
    st.set_page_config(layout="wide")
    local_css("style.css")  # Load custom CSS
    st.title("Vulnerability Management App")

    
    
    # App description
    st.markdown("""
    This app allows you to view and manage vulnerabilities across different categories. 
    Use the sidebar to navigate between vulnerability types, filter the data, and update comments.
    """)
    
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    current_page = st.session_state.get('current_page', "VTMs")
    new_page = st.sidebar.selectbox("Select Vulnerability Type", ["VTMs", "GEMs", "Self Service"], index=["VTMs", "GEMs", "Self Service"].index(current_page))

    if new_page != current_page:
        # Reset filters when changing pages
        st.session_state.filters = {
            "Vulnerability ID": None,
            "Owner": None,
            "Product Name": None
        }
        st.session_state.current_page = new_page
        # Reset selectbox values
        st.session_state.vuln_id_filter = "None"
        st.session_state.owner_filter = "None"
        st.session_state.product_filter = "None"
        st.rerun()  # Force a rerun to reset selectbox values

    page = new_page

    # Help section in sidebar
    with st.sidebar.expander("Help"):
        st.markdown("""
        - **VTMs**: Vulnerability Team Managed
        - **GEMs**: Globally Exposed Managed
        - **Self Service**: Self-managed vulnerabilities
        
        Use the filter buttons below to narrow down the vulnerabilities displayed.
        """)
    
    # Load data based on selected page
    if 'data' not in st.session_state:
        st.session_state.data = {vuln_type: load_data(vuln_type) for vuln_type in ["VTMs", "GEMs", "Self Service"]}
    
    data = st.session_state.data[page]
    
    # Initialize session state for filters if not exists
    if 'active_filter' not in st.session_state:
        st.session_state.active_filter = None
        st.session_state.active_value = None

    st.sidebar.header("Filter and Update")

    # Initialize filters if not exists
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            "Vulnerability ID": None,
            "Owner": None,
            "Product Name": None
        }

    # Filter options
    st.sidebar.subheader("Apply Filters")

    # Vulnerability ID filter
    vuln_id_filter = st.sidebar.selectbox(
        "Filter by Vulnerability ID",
        ["None"] + list(data['Vulnerability ID'].unique()),
        index=0,
        key="vuln_id_filter"
    )
    st.session_state.filters["Vulnerability ID"] = None if vuln_id_filter == "None" else vuln_id_filter

    # Owner filter
    owner_filter = st.sidebar.selectbox(
        "Filter by Owner",
        ["None"] + list(data['Owner'].unique()),
        index=0,
        key="owner_filter"
    )
    st.session_state.filters["Owner"] = None if owner_filter == "None" else owner_filter

    # Product Name filter
    product_filter = st.sidebar.selectbox(
        "Filter by Product Name",
        ["None"] + list(data['Product Name'].unique()),
        index=0,
        key="product_filter"
    )
    st.session_state.filters["Product Name"] = None if product_filter == "None" else product_filter

    # Apply filters
    filtered_data = filter_data(data, st.session_state.filters)

    # Display filter information
    active_filters = [f"{k}: {v}" for k, v in st.session_state.filters.items() if v is not None]
    if active_filters:
        st.info(f"Active filters: {', '.join(active_filters)}")
    else:
        st.info(f"Displaying all vulnerabilities for {page}")

    # Update comment section
    if any(st.session_state.filters.values()):
        st.sidebar.markdown("### Update Comment")
        if filtered_data.empty:
            st.sidebar.warning("No vulnerabilities match the current filters. Cannot update comments.")
        else:
            st.sidebar.markdown("Use this section to update the comment for the selected vulnerability/vulnerabilities.")
            new_comment = st.sidebar.text_area("New Comment")
            if st.sidebar.button("Submit Update"):
                for filter_type, filter_value in st.session_state.filters.items():
                    if filter_value:
                        st.session_state.data[page] = update_comment(data, filter_type, filter_value, new_comment)
                st.sidebar.success("Update submitted successfully!")
                # Force a rerun to update the table
                st.rerun()

    # Display the fixed-size table
    st.header(f"{page} Vulnerabilities")
    
    # Custom CSS for fixed-size table with wrapped headers
    st.markdown("""
    <style>
    .fixed-table {
        width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
    }
    .fixed-table th, .fixed-table td {
        border: 1px solid #ddd;
        padding: 8px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .fixed-table th {
        background-color: #f2f2f2;
        font-weight: bold;
        white-space: normal;
        word-wrap: break-word;
        height: 60px;
        vertical-align: middle;
    }
    .fixed-table td {
        white-space: nowrap;
    }
    .fixed-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .comment-cell {
        white-space: normal;
        word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create HTML table
    table_html = "<table class='fixed-table'>"
    table_html += "<tr><th style='width:10%'>Vulnerability ID</th><th style='width:10%'>Product Name</th>"
    table_html += "<th style='width:15%'>Vulnerability</th><th style='width:10%'>Owner</th>"
    table_html += "<th style='width:10%'>Due Date</th><th style='width:20%'>Comment</th>"
    table_html += "<th style='width:10%'>CVE ID</th><th style='width:10%'>Status</th></tr>"

    for _, row in filtered_data.iterrows():
        table_html += "<tr>"
        table_html += f"<td>{row['Vulnerability ID']}</td>"
        table_html += f"<td>{row['Product Name']}</td>"
        table_html += f"<td>{row['Vulnerability']}</td>"
        table_html += f"<td>{row['Owner']}</td>"
        table_html += f"<td>{row['Due Date'].strftime('%Y-%m-%d')}</td>"
        table_html += f"<td class='comment-cell'>{row['Comment']}</td>"
        table_html += f"<td>{row['CVE ID']}</td>"
        table_html += f"<td>{row['Status']}</td>"
        table_html += "</tr>"

    table_html += "</table>"

    # Display the fixed-size table
    st.markdown(table_html, unsafe_allow_html=True)

    # Status legend
    st.markdown("### Status Legend")
    st.markdown("""
    - **Open**: Vulnerability identified but not yet addressed
    - **In Progress**: Work is being done to address the vulnerability
    - **Awaiting Info**: More information is needed before proceeding
    - **Closed**: Vulnerability has been resolved
    """)



if __name__ == "__main__":
    main()
