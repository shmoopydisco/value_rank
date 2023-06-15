import streamlit as st


def is_response_valid(response):
    # center = len(respond[0]) // 2  # middle of num of columns
    # for row in range(4):
    #     for column in range(center - row, center + row + 1):
    #         if not respond[row][column]:
    #             return False
    # return True
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
        for column_id, column_container in enumerate(st.columns(7)):
            for row in range(4):
                # skip the empty cells
                if not is_cell_part_of_pyramid(row, column_id):
                    continue
                else:
                    # add the pyramid cells
                    response[column_id].append(
                        column_container.text_input(
                            f"{row,column_id}", label_visibility="hidden"
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
                st.write(concat_response)
                conn = st.experimental_connection("values_db", type="sql")
                with conn.session as s:
                    # create table with 7 values
                    s.execute(
                        """CREATE TABLE IF NOT EXISTS user_values (value1 TEXT NOT NULL, value2 TEXT NOT NULL, value3 TEXT NOT NULL, value4 TEXT NOT NULL, value5 TEXT NOT NULL, value6 TEXT NOT NULL, value7 TEXT NOT NULL)"""
                    )
                    s.execute(
                        "INSERT INTO user_values VALUES (:value1, :value2, :value3, :value4, :value5, :value6, :value7)",
                        (concat_response),
                    )
                    s.commit()

                st.dataframe(conn.query("SELECT * FROM user_values"))

            else:
                st.error("Please fill in all the cells")


if __name__ == "__main__":
    main()
