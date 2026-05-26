"""
create date: 2026/04/23
author: ikuta
content: main_1U
"""

#------------------------------------------------------
# import  
import src.settings_init.HK.header_HK as head_HK
import src.settings_init.HK.output_file_name_HK as out_HK
import src.utils.csv_processor.output_process as output
import src.data_process.HK.calc.PWR.Battery_calc as bc
import src.data_process.HK.calc.PWR.Power_budget_calc as bud
import src.data_process.HK.calc.PWR.Power_Generation_calc as PG
import src.data_process.HK.plot.SAP_data_plot as SP
import src.data_process.HK.plot.Battery_data_plot as Bp
#------------------------------------------------------
# main

def analysis_1U(extracted_list):

    for item in extracted_list: # ファイル名による条件分岐
    #-----------------------------------------------------------------------------------
    # HKデータ解析
        # HKという文字がファイル名に入っているものをここで処理
        if "HK" in item["name"]:
            HK_data = item["data"] # HKのファイルに入っている全てのヘッダー列を抽出

            # 1. 抽出したデータから計算・各種データ処理

            # PWR系
            # 〇 SAPでの発電量計算 & 計算結果をリストに格納
            HK_data = PG.SAP_calc_result(HK_data)
            # 〇 バッテリーでの発電量計算 & 計算結果をリストに格納
            HK_data = bc.BAT_calc_result(HK_data)
            # 〇 電力収支計算 & 計算結果をリストに格納 (これは発電・バッテリー計算結果を格納した後に持ってくること！)
            HK_data = bud.Budget_result(HK_data)
            
            # 本体のリストを更新
            item["data"] = HK_data

            # 2. csvファイルに出力
            
            # PWR系
            # SAP関係のcsvファイル出力
            output.output_csv_excel(HK_data, header_list=head_HK.columns_gene, use_utc_name=True, base_name=out_HK.Gene_name_1U, header_map=head_HK.header_map)
            # バッテリー関係のcsvファイル出力
            output.output_csv_excel(HK_data, header_list=head_HK.columns_BAT, use_utc_name=True, base_name=out_HK.BAT_name_1U, header_map=head_HK.header_map)
            # 電力収支関係のcsvファイル出力
            output.output_csv_excel(HK_data, header_list=head_HK.columns_budget, use_utc_name=True, base_name=out_HK.budget_name_1U, header_map=head_HK.header_map)

            # 3. plot
            # PWR系
            SP.sap_plot(HK_data) # SAP
            Bp.BAT_plot(HK_data) # battery

