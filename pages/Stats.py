import streamlit as st
from pathlib import Path


def main():
    st.set_page_config(page_title="Value Stats", page_icon="📈", layout="wide")
    st.title(
        "📊 Value Statistics",
        anchor=False,
    )

    # get the values
    conn = st.experimental_connection("values_db", type="sql")
    user_data = conn.query("SELECT * FROM user_values")

    st.subheader("Top Values")
    st.bar_chart(user_data["value7"].value_counts().head(10))

    st.subheader("Bottom Values")
    st.bar_chart(user_data["value1"].value_counts().head(10))

    st.subheader("Most Common Values")
    st.bar_chart(user_data.stack().value_counts().head(10))

    with st.expander("Expand to see full database"):
        db_file = Path("values.db").read_bytes()
        st.download_button("Download database", db_file, file_name="values.db")
        st.dataframe(user_data)


if __name__ == "__main__":
    main()
