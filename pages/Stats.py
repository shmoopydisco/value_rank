import streamlit as st
from pathlib import Path


def main():
    st.set_page_config(page_title="Value Stats", page_icon="📈", layout="wide")
    st.title(
        "📊 Value Statistics",
        anchor=False,
    )
    with st.expander("Expand to see full database"):
        db_file = Path("values.db").read_bytes()
        st.download_button("Download database", db_file, file_name="values.db")
        conn = st.experimental_connection("values_db", type="sql")
        st.dataframe(conn.query("SELECT * FROM user_values"))


if __name__ == "__main__":
    main()
