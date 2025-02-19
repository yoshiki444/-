import pandas as pd

def save_to_excel(data, filename):
    """
    データをExcelファイルとして保存する関数
    :param data: 保存するデータ（リストまたはDataFrame）
    :param filename: 保存するファイル名
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise ValueError("データはリストまたはDataFrameである必要があります")
    df.to_excel(filename, index=False)
    print(f"データが {filename} として保存されました。")

def read_from_excel(filename):
    """
    Excelファイルからデータを読み込む関数
    :param filename: 読み込むファイル名
    :return: 読み込んだデータ（DataFrame）
    """
    try:
        df = pd.read_excel(filename)
        print(f"{filename} からデータを読み込みました。")
        return df
    except FileNotFoundError:
        print(f"ファイル {filename} が見つかりません。")
        return None
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        return None
