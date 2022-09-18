from app.preprocessing import *
import random



def create_df_cleaned(path_excel_file, split_columns, exclude):

    df = pd.read_excel(path_excel_file, sheet_name="ALL_ANONYMISED")

    
    df_cleaned = df.copy()
    for column in list(set(df.columns) - set(split_columns).union(set(exclude))):
        df_cleaned[column] = hero.clean(df_cleaned[column], custom_pipeline)
        df_cleaned[column] = df_cleaned[column].apply(lemmatize_text)

    for column in split_columns:
        df_cleaned[column] = hero.preprocessing.lowercase(df_cleaned[column])
    df_cleaned.replace('report', '', inplace=True, regex=True)
    df_cleaned.replace('reporting', '', inplace=True, regex=True)
    df_cleaned = df_cleaned.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df, df_cleaned

def return_results(path_excel_file, sentence, split_columns, exclude, method):
    df, df_cleaned = create_df_cleaned(path_excel_file, split_columns, exclude)
    return return_best_n(df, df_cleaned, sentence, method, exclude, split_columns, top=5)

def return_response(path_excel_file, sentence, split_columns, exclude):
    df, df_cleaned = create_df_cleaned(path_excel_file, split_columns, exclude)
    try:
        list_found = return_best_n(df, df_cleaned, sentence, "n_grams", exclude, split_columns, top=5)
    except:
         list_found = return_best_n(df, df_cleaned, sentence, "basic_cosine_similarity", exclude, split_columns, top=5)
    response_structure = dict()
    for i in list_found:
        response_structure[i] = df.iloc[i].to_dict()
    return response_structure