"""
date: 2026/05/04
author: ikuta
this file for csv output process
"""

#-------------------------------------------------------------
# import
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
#-------------------------------------------------------------
#function

# 格納されたデータのうち、最初の行のUTC時刻をファイル名に記録するための関数
def create_filename_with_utc(original_file_name, merged_list):

    # UTCの1行目（ヘッダー除いた最初）
    first_utc = next((t for t in merged_list.get("UTC Time", []) if t is not None), None)

    # UTCが存在しない場合（全てNoneなど）
    if first_utc is None:
        print("[WARNING] UTC Time is all None")
        return f"invalid_{original_file_name}"

    # datetimeに変換
    try:
        dt = datetime.strptime(first_utc, "%Y/%m/%d %H:%M:%S")
    except Exception as e:
        print(f"[ERROR] UTC format invalid: {first_utc}")
        return f"invalid_{original_file_name}"

    # YYMMDD_HHMMSS に変換
    time_str = dt.strftime("%y%m%d_%H%M%S")

    # 新しい名前
    new_name = f"{time_str}_{original_file_name}.csv"

    return new_name

# CSVデータを整理・加工して、条件ごとに必要な形でCSVやExcelに出力するデータ処理のベースコード
def export_data(name, header_list, data, use_utc_name=False, base_name=None, header_map=None):
    
    # ======================
    # ファイル名決定
    # ======================
    # base_nameが指定されていればそれを使う
    if base_name is not None:
        name_to_use = base_name
    else:
        name_to_use = name

    # ======================
    # 出力フォルダ分岐
    # ======================
    if "1U" in name_to_use:
        output_dir = Path(__file__).resolve().parents[3] / "data" / "Output" / "1U"
    elif "2U" in name_to_use:
        output_dir = Path(__file__).resolve().parents[3] / "data" / "Output" / "2U"
    else:
        output_dir = Path(__file__).resolve().parents[3] / "data" / "Output" / "others"

    output_dir.mkdir(parents=True, exist_ok=True)

    # 拡張子除去
    name_to_use = name_to_use.replace(".csv", "").replace(".xlsx", "")

    # UTC付きファイル名処理
    if use_utc_name:
        file_name_csv = create_filename_with_utc(name_to_use, data)
        file_name_xlsx = file_name_csv.replace(".csv", ".xlsx")
    else:
        file_name_csv = f"{name_to_use}.csv"
        file_name_xlsx = f"{name_to_use}.xlsx"

    # ======================
    # ヘッダー処理
    # ======================
    if header_list is None:
        headers = list(data.keys())
    else:
        headers = [col for col in header_list if col in data]
    # 表示用ヘッダー作成    
    if header_map:
        display_headers = [header_map.get(col, col) for col in headers]
    else:
        display_headers = headers

    # debug
    #print("header_map is:", header_map)
    
    #print("=== header_map is ===")
    #print(header_map)

    #print("=== headers ===")
    #for h in headers:
    #    print(f"[{h}]")

    #print("=== mapping result ===")
    #for h in headers:
    #    print(h, "->", header_map.get(h, "❌ not found") if header_map else "header_map is None")

    # ======================
    # 行数
    # ======================
    num_rows = len(next(iter(data.values())))

    # ======================
    # 行データ作成
    # ======================
    
    # 行データ
    rows = []
    for i in range(num_rows):
        row = {}
        for key, disp_key in zip(headers, display_headers):
            values = data.get(key, [])
            row[disp_key] = values[i] if i < len(values) else ""
        rows.append(row)

    # CSV出力
    csv_file = output_dir / file_name_csv
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=display_headers)
        writer.writeheader()
        writer.writerows(rows)


    # ======================
    # Excel出力
    # ======================
    xlsx_file = output_dir / file_name_xlsx

    df = pd.DataFrame({key: data[key] for key in headers})
    df.columns = display_headers
    df.to_excel(xlsx_file, index=False)

# 実際に値をcsv, xlsxで出力する関数
# 引数：データリスト, 出力するヘッダーのリスト, 名前の前に一番古いデータのutc時刻を付けるか, 任意で付けたい名前 (inputのcsvと同じ名前にしたいときはNone)
def output_csv_excel(data, header_list=None, use_utc_name=False, base_name=None, header_map=None):

    # ======================
    # ✅ パターン①：all_data_listから各ファイルを出力（list）
    # ======================
    if isinstance(data, list):

        for item in data:

            export_data(
                name=item["name"],
                header_list=header_list,
                data=item["data"],
                use_utc_name=use_utc_name,
                base_name=base_name,
                header_map=header_map
            )

    # ======================
    # ✅ パターン②：単一ファイルを抽出した後、様々なファイル出力を行う場合（nameなし・dataのみ格納されたdict）
    # ======================
    elif isinstance(data, dict):

        export_data(
            name="single_file",  # ← 必要ならここ調整
            header_list=header_list,
            data=data,
            use_utc_name=use_utc_name,
            base_name=base_name,
            header_map=header_map
        )