import streamlit as st
import ui.home
import ui.explore
# import ui.check

def main(app_data):
    app_data.pages = [
        st.Page(ui.home.main, title="Home :)", default=True),
        st.Page(ui.explore.main, title="Explore", url_path="/explore"),
        # st.Page(ui.check.main, title="Check", url_path="/check"),
    ]
    
    ui.home.init(app_data)
    ui.explore.init(app_data)
    # ui.check.init(app_data)

    page = st.navigation(app_data.pages)

    st.logo(":material/home:")
    
    page.run()
