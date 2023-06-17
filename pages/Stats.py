import streamlit as st
from pathlib import Path
import pandas as pd


def main():
    st.set_page_config(page_title="Value Stats", page_icon="📈", layout="wide")
    st.title(
        "📊 Value Statistics",
        anchor=False,
    )

    # get the values
    try:
        conn = st.experimental_connection("values_db", type="sql", ttl=60 * 5)
        user_data = conn.query("SELECT * FROM user_values", ttl=60 * 5)
    except Exception as e:
        st.error(e)
        st.stop()

    st.subheader("Top 1st Values")
    st.bar_chart(user_data["value7"].value_counts())

    st.subheader("Bottom Last Values")
    st.bar_chart(user_data["value1"].value_counts())

    st.subheader("Most Common Values Considering Importance")
    series_list = []
    for column in range(1, 8):
        for value in user_data[f"value{column}"]:
            # unpack the values in each column to a list
            counts = pd.Series(value.split(";")).value_counts()
            # multiply count by column number
            weighted_counts = counts.apply(lambda x: x * column)
            series_list.append(weighted_counts)
    st.bar_chart(
        pd.concat(series_list).groupby(level=0).sum().sort_values(ascending=True)
    )

    st.subheader("Most Common Values (regardless of position))")
    st.bar_chart(user_data.stack().value_counts().sort_values(ascending=True))

    with st.expander("Expand to see each column distribution"):
        for column in range(1, 8):
            st.subheader(f"Column {column} Distribution (Higher is more important)")
            # unpack the values in each column to a list
            for value in user_data[f"value{column}"]:
                st.bar_chart(pd.Series(value.split(";")).value_counts())

    with st.expander("Expand to see full database"):
        db_file = Path("values.db").read_bytes()
        st.download_button("Download database", db_file, file_name="values.db")
        st.dataframe(user_data)


if __name__ == "__main__":
    main()
