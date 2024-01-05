"""
Very Basic And Very Miscellaneous Functions Which Do Basic Data Handling Tasks. They Are Very Specific To This Project
And Are Too Overly Specific To Put In Another FIle.
"""


def dekebabify(text: str):
    text_list = text.split("_")
    updated = ""
    for word in text_list:
        updated += word.title() + " "
    return updated.strip()


def clean_column_names(dataframe):
    for col in dataframe:
        if "id" in col:
            pass
        else:
            new_col = dekebabify(col)

            dataframe.rename(columns={col: new_col}, inplace=True)


def convert_bools_to_ints(DF):
    print(DF['has_children'].dtype)
    for col in DF.columns:
        if DF[col].dtype == "bool":
            DF[col] = DF[col].astype(int)
    return DF


def get_non_binary_data(DF):
    dummy = DF.copy()
    for col in dummy.columns:
        if dummy[col].dtype == "bool":
            dummy.drop(columns=[col], inplace=True)
    return dummy


def pull_only_number_cols(DF):
    ml_fixed_cols = [col for col in DF.columns
                     if (col == "Male" or col == "Female" or col == "user_id" or DF[col].dtype != "object")]
    return DF[ml_fixed_cols]


def rename_cells(DF):
    for col in DF.columns:
        if col not in ["user_id", 'male', 'female', 'age']:
            if col not in ['has_children', 'hotel_booked', 'flight_booked', 'cancellation', 'married']:
                DF.rename(columns={col: f"avg_{col}"}, inplace=True)
            else:
                DF.rename(columns={col: f"prop_{col}"}, inplace=True)
    return DF


def update_agg_cols(DF):
    for col in DF.columns:
        name, tag = col
        if name not in ['user_id', 'male', 'female', 'age']:
            if name in ['has_children', 'hotel_booked', 'flight_booked', 'cancellation', 'married']:
                tag = "prop"
            else:
                if tag == "mean":
                    tag = "avg"
                elif tag == "sum":
                    tag = "total"
            new_col_name = f"{tag}_{name}"

            DF.rename(columns={name: new_col_name}, inplace=True)
    return DF


def find_infs(DF, remove=False):
    counter = 0
    for col in DF.columns:
        try:
            this_col = k[col]
            for index, row in enumerate(this_col):
                if np.isinf(row) or np.isnan(row):
                    print(f"COL: {col}, ROW: {index}, VALUE: {row}")
                    counter += 1
                    if remove:
                        DF[col].replace(np.nan, 0, inplace=True).replace(np.inf, 0, inplace=True)

        except KeyError:
            print(f"COL: {col} Didn't Fit For Some reason.")
    print("Num Infs: ", counter)
    return DF



