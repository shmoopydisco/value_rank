from random import randint

import streamlit as st


def main():
    st.set_page_config(page_title="Value Rank", page_icon="🏆", layout="wide")
    st.title(
        "🏅 Rank Your Values!",
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
        # define empty 7x4 respond
        respond = [[None] * 7 for _ in range(4)]
        for column_id, column in enumerate(st.columns(7)):
            for row in range(4):
                # skip the empty cells
                if (
                    (row + column_id < 3)
                    or (row == 0 and column_id != 3)
                    or (row == 1 and column_id > 4)
                    or (row == 2 and column_id > 5)
                ):
                    continue
                else:
                    print(row, column_id)
                    respond[row][column_id] = column.text_input(
                        f"{row,column_id}",
                    )

        submitted = st.form_submit_button(
            "Submit",
            type="primary",
            use_container_width=True,
        )
        if submitted:
            st.success("Submitted")
            st.write(respond)


if __name__ == "__main__":
    main()
