"""
date: 2026/05/04
author: ikuta
this file for battery analysis
"""

#------------------------------------------------------------------
# import
import src.utils.organizing_datalist as org
#------------------------------------------------------------------
# function

# 1. バッテリーの充電電力を計算する関数
def battery_charge_calc(curs_2ndbat, vols_2ndbat):
    # 充電が+, 放電は-になる
    Charging_mW_2ndbat = curs_2ndbat * vols_2ndbat
    # 辞書で返す（ヘッダー付き）
    return {
        "Battery_charge":Charging_mW_2ndbat
    }

# 2.真のバッテリー電圧を推定する関数
def estimate_true_battery_voltage(curs_2ndbat, vols_2ndbat, resistance):
    # 取得したバッテリー電圧値とバッテリー内部抵抗による電圧降下から、真のバッテリー電圧を推定(電流はmA単位であることに注意！)
    est_true_vols_2ndbat = vols_2ndbat - resistance * curs_2ndbat *0.001 
    # 辞書で返す（ヘッダー付き）
    return {
        "est_true_vols_2ndbat":est_true_vols_2ndbat
    }

#----------------------------------------------------------------
# main

# バッテリー関連の計算を行い, 結果を全てリストに格納する (引数：dict, 定数)
def BAT_calc_result(extracted_list, resistance):
    
    #------------------------------------------------
    # 1.の関数
    # 値格納用のリストの作成
    charging_list = []

    # バッテリー充電電力の計算
    for curs_2ndbat, vols_2ndbat in zip(
        extracted_list["curs_2ndbat"],
        extracted_list["vols_2ndbat"]
    ):
    
        result = battery_charge_calc(
            curs_2ndbat, vols_2ndbat
        )
    
        # リストに値を格納
        charging_list.append(result["Battery_charge"])
    # extracted_listに列を追加
    org.dict_append("Battery_charge", charging_list, extracted_list)
    #----------------------------------------------------------
    # 2.の関数
    # 値格納用のリストの作成
    est_true_bettery_list = []

    # 真のバッテリー電圧の計算
    for curs_2ndbat, vols_2ndbat in zip(
        extracted_list["curs_2ndbat"],
        extracted_list["vols_2ndbat"]
    ):
    
        result = estimate_true_battery_voltage(
            curs_2ndbat, vols_2ndbat, resistance
        )
    
        # リストに値を格納
        est_true_bettery_list.append(result["est_true_vols_2ndbat"])
    # extracted_listに列を追加
    org.dict_append("est_true_vols_2ndbat", est_true_bettery_list, extracted_list)
    #----------------------------------------------------------
    
    return extracted_list

