"""
create date: 2026/04/23
author: ikuta
content: main (このファイルを実行する)
"""
#------------------------------------------------------------------------------------
#import
from pathlib import Path
import src.sat_1U.main_1U as main_1U
import src.sat_2U.main_2U as main_2U
import src.utils.csv_processor.extract_process_from_Input_csv as input
import src.settings_init.common_valiables as com_val
import src.utils.csv_processor.output_process as output
import src.utils.extra_functions as extra
#------------------------------------------------------------------------------------
# main

# 生データの入っているcsvファイルのフォルダパスを参照(1U)
data_dir_1U = Path(__file__).resolve().parent/"data"/"Input"/"1U"
data_dir_2U = Path(__file__).resolve().parent/"data"/"Input"/"2U"
# フォルダが存在しないときにエラーを出す (デバッグ用)
# if not data_dir_1U.exists():
   # raise FileNotFoundError(f"Output folder not found: {data_dir_1U}")
# if not data_dir_2U.exists():
   # raise FileNotFoundError(f"Output folder not found: {data_dir_2U}")

# inputファイルの全てのデータを格納し, UTC時刻を足したリストを作成(1U/2Uそれぞれ)
all_list_1U = input.read_csv_and_add_utc(data_dir_1U, com_val.OBC_time_sample_1U, com_val.UTC_time_sample_1U)
all_list_2U = input.read_csv_and_add_utc(data_dir_2U, com_val.OBC_time_sample_2U, com_val.UTC_time_sample_2U)

# 作成したリストを各ファイルに分けて再度出力 (csvとxlsx)  ※これは単位がつかない
output.output_csv_excel(all_list_1U, header_list=None, use_utc_name=False, base_name=None)
output.output_csv_excel(all_list_2U, header_list=None, use_utc_name=False, base_name=None)

# 1Uと2Uそれぞれでデータ処理
main_1U.analysis_1U(all_list_1U) # 1Uのプログラムを実行
main_2U.analysis_2U(all_list_2U) # 2Uのプログラムを実行

#-----------------------------------------------------------------------------------
# おまけ機能
extra.extra_functions()