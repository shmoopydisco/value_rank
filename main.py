import streamlit as st


def check_respond_valid(respond):
    center = len(respond[0]) // 2  # middle of num of columns
    for row in range(4):
        for column in range(center - row, center + row + 1):
            if not respond[row][column]:
                return False
    return True


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
        for column_id, column_container in enumerate(st.columns(7)):
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
                    # add the pyramid cells
                    respond[row][column_id] = column_container.text_input(
                        f"{row,column_id}", label_visibility="hidden"
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
            if check_respond_valid(respond):
                st.success("Submitted")
                st.write(respond)
            else:
                st.error("Please fill in all the cells")


if __name__ == "__main__":
    main()
