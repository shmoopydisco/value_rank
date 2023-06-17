import streamlit as st
from streamlit_datalist import stDatalist
from sqlalchemy.sql import text


def is_response_valid(response):
    for column_id in response:
        for value in range(len(response[column_id])):
            if not response[column_id][value]:
                return False
    return True


def is_cell_part_of_pyramid(row, column):
    if (
        (row + column < 3)
        or (row == 0 and column != 3)
        or (row == 1 and column > 4)
        or (row == 2 and column > 5)
    ):
        return False
    return True


def main():
    st.set_page_config(page_title="Value Rank", page_icon="🏆", layout="wide")
    st.title(
        "🏅 Rank Your Values!",
        anchor=False,
    )

    # trick to get the columns to align to the bottom
    st.markdown(
        """
    <style>
        div[data-testid="column"]
        {
            align-self: flex-end;
        } 
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.form("my_form", clear_on_submit=False):
        # define response scheme
        response = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
        }
        suggestions = [
            "עבודת צוות",
            "התנהגות ראויה",
            "יכולות הוראה",
            "שימור סקרנות",
            "רפלקציה",
            "שימור חוסן",
            "יושרה",
            "מעורבות במחקר",
            "יכולת מנהיגות",
            "Professional identity formation",
            "הומניסטיקה",
            "מעורבות בקהילה",
            "רוח באר שבע",
            "ענווה",
            "חמלה",
            "חוסר שיפוטיות",
        ]
        for column_id, column_container in enumerate(st.columns(7)):
            for row in range(4):
                # skip the empty cells
                if not is_cell_part_of_pyramid(row, column_id):
                    continue
                else:
                    # add the pyramid cells
                    with column_container:
                        response[column_id].append(
                            stDatalist(
                                label="",
                                options=suggestions,
                                key=f"{column_id}{row}",
                            )
                        )

        col1, col2 = st.columns([3, 1])
        col1.header("Less important values ⬅️", anchor=False)
        col2.header("➡️ Most important values", anchor=False)

        submitted = st.form_submit_button(
            "Submit",
            type="primary",
            use_container_width=True,
        )
        if submitted:
            if is_response_valid(response):
                st.success("Thank you for your submission!")
                # join every list with several items into one list with items joined by semicolon
                concat_response = {
                    f"value{column_id+1}": ";".join(response[column_id])
                    for column_id in response
                    if response[column_id]
                }
                conn = st.experimental_connection("values_db", type="sql")
                with conn.session as s:
                    # create table with 7 values
                    s.execute(
                        text(
                            """CREATE TABLE IF NOT EXISTS user_values (
                                value1 TEXT NOT NULL,
                                value2 TEXT NOT NULL,
                                value3 TEXT NOT NULL,
                                value4 TEXT NOT NULL,
                                value5 TEXT NOT NULL,
                                value6 TEXT NOT NULL,
                                value7 TEXT NOT NULL
                            )"""
                        )
                    )
                    s.execute(
                        text(
                            "INSERT INTO user_values VALUES (:value1, :value2, :value3, :value4, :value5, :value6, :value7)"
                        ),
                        (concat_response),
                    )
                    s.commit()


if __name__ == "__main__":
    main()
