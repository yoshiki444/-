import pandas as pd

def normalize_patient_data(patient_data):
    """
    患者データを正規化する関数
    :param patient_data: 正規化する患者データのリスト
    :return: 正規化された患者データのリスト
    """
    normalized_data = []
    for patient in patient_data:
        services = patient["サービス"].split()
        for service in services:
            normalized_patient = patient.copy()
            normalized_patient["サービス"] = service
            normalized_data.append(normalized_patient)
    return normalized_data

def analyze_patient_data(df):
    """
    患者データを分析する関数
    :param df: 分析する患者データのDataFrame
    :return: 分析結果の辞書
    """
    analysis = {
        "総患者数": len(df),
        "平均年齢": calculate_average_age(df),
        "要介護度別患者数": df["要介護度"].value_counts().to_dict(),
        "サービス別利用者数": df["サービス"].value_counts().to_dict()
    }
    return analysis

def calculate_average_age(df):
    """
    平均年齢を計算する関数
    :param df: 患者データのDataFrame
    :return: 平均年齢
    """
    current_year = pd.Timestamp.now().year
    df["年齢"] = df["生年月日"].apply(lambda x: current_year - pd.to_datetime(x).year)
    return df["年齢"].mean()
