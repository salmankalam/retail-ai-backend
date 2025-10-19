from .supabase_client import supabase

ANALYZE_TABLE = "analyze_data"
CLEAN_TABLE = "clean_data"
PREDICT_TABLE = "predict_data"

# ---------------- ANALYZE ----------------
def insert_analyze(email, file_name, df, summary):
    data_json = df.to_dict(orient="records")
    return supabase.table(ANALYZE_TABLE).insert({
        "email": email,
        "file_name": file_name,
        "analyzed_data": data_json,
        "summary": summary
    }).execute()


def get_analyze(email):
    return supabase.table(ANALYZE_TABLE).select("*").eq("email", email).execute()


# ---------------- CLEAN ----------------
def insert_clean(email, file_name, df):
    data_json = df.to_dict(orient="records")
    return supabase.table(CLEAN_TABLE).insert({
        "email": email,
        "file_name": file_name,
        "cleaned_data": data_json
    }).execute()


def get_clean(email):
    return supabase.table(CLEAN_TABLE).select("*").eq("email", email).execute()


# ---------------- PREDICT ----------------
def insert_predict(email, file_name, df, summary):
    data_json = df.to_dict(orient="records")
    return supabase.table(PREDICT_TABLE).insert({
        "email": email,
        "file_name": file_name,
        "predicted_data": data_json,
        "prediction_summary": summary
    }).execute()


def get_predict(email):
    return supabase.table(PREDICT_TABLE).select("*").eq("email", email).execute()
