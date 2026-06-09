"""
date: 2026/05/04
author: ikuta
this file for power budget
"""

#------------------------------------------------------------------
# import
import src.utils.organizing_datalist as org
#------------------------------------------------------------------
# function

# 1. バスでの電力消費を計算する関数
def bus_consumption_calc(curs_bus, vols_bus):
    mW_bus = curs_bus * vols_bus
    # 辞書で返す（ヘッダー付き）
    return {
        "Bus_consumption":mW_bus
    }

# 2. 電力収支の合計を計算する関数
def budget_check(SAP_gene, battery_charge, bus_consume):
    # 理想は０　(発電量 = 充電 + バス消費) 
    budget_total = SAP_gene - battery_charge - bus_consume
    return{
        "budget_check":budget_total        
    }

# 3. MTQの電力消費を計算する関数
def calc_mtq(curs_mtqa_x, curs_mtqa_y, curs_mtqa_z, curs_mtqo_z2, curs_mtqo_z3, curs_mtqo_z4, vols_mtqa, vols_mtqo_plasma):
    # MTQ_Aの各軸消費電力を計算
    if vols_mtqa > 2.0: # vols_mtqaが2Vより大きいならMTQAが通電している判定, それ以下ならFETがつながっていない判定(本来は5Vor0V)
        pwr_mtqa_x = curs_mtqa_x * vols_mtqa
        pwr_mtqa_y = curs_mtqa_y * vols_mtqa
        pwr_mtqa_z = curs_mtqa_z * vols_mtqa
    else:
        pwr_mtqa_x = 0
        pwr_mtqa_y = 0
        pwr_mtqa_z = 0

    # MTQ_Oの各軸消費電力を計算
    if vols_mtqo_plasma > 2.0: # vols_mtqo_plasmaが2V以上ならMTQOが通電している判定, それ以下ならFETがつながっていない判定(本来は5Vor0V)
        pwr_mtqo_z2 = curs_mtqo_z2 * vols_mtqo_plasma
        pwr_mtqo_z3 = curs_mtqo_z3 * vols_mtqo_plasma
        pwr_mtqo_z4 = curs_mtqo_z4 * vols_mtqo_plasma
    else:
        pwr_mtqo_z2 = 0
        pwr_mtqo_z3 = 0
        pwr_mtqo_z4 = 0
    # 各MTQの合計消費電力を計算
    pwr_mtqa_total = pwr_mtqa_x + pwr_mtqa_y + pwr_mtqa_z # MTQ_A
    pwr_mtqo_total = pwr_mtqo_z2 + pwr_mtqo_z3 + pwr_mtqo_z4 # MTQ_O
    
    #辞書で返す
    return {
        "pwr_mtqa_x":pwr_mtqa_x,
        "pwr_mtqa_y":pwr_mtqa_y,
        "pwr_mtqa_z":pwr_mtqa_z,
        "pwr_mtqo_z2":pwr_mtqo_z2,
        "pwr_mtqo_z3":pwr_mtqo_z3,
        "pwr_mtqo_z4":pwr_mtqo_z4,
        "pwr_mtqa_total":pwr_mtqa_total,
        "pwr_mtqo_total":pwr_mtqo_total
    }

#------------------------------------------------------------------------------
# main

# 電力収支関連の計算を行い, 結果を全てリストに格納する (引数：dict)
def Budget_result(extracted_list):
    
    #------------------------------------------------
    # 1.の関数
    # 値格納用のリストの作成
    budget_list = []

    # バス消費電力の計算
    for curs_bus, vols_bus in zip(
        extracted_list["curs_bus"],
        extracted_list["vols_bus"]
    ):
    
        result = bus_consumption_calc(
            curs_bus, vols_bus
        )
    
        # リストに値を格納
        budget_list.append(result["Bus_consumption"])

    # extracted_listに列を追加 (ここでこれやっとかないと, 2.の計算ができない)
    org.dict_append("Bus_consumption", budget_list, extracted_list)
    #----------------------------------------------------------
    # 2.の関数
    # 値格納用のリストの作成
    check_list = []

    # 収支のチェック
    for SAP_generation_total, Battery_charge, Bus_consumption in zip(
        extracted_list["pwr_sap_total"],
        extracted_list["Battery_charge"],
        extracted_list["Bus_consumption"]
    ):
    
        result = budget_check(
            SAP_generation_total, Battery_charge, Bus_consumption
        )
    
        # リストに値を格納
        check_list.append(result["budget_check"])
    
    # extracted_listに列を追加
    org.dict_append("budget_check", check_list, extracted_list)
    #-------------------------------------------------------------------
     # 3.の関数
    # 値格納用のリストの作成
    mtqa_x_list = []
    mtqa_y_list = []
    mtqa_z_list = []
    mtqo_z2_list = []
    mtqo_z3_list = []
    mtqo_z4_list = []
    mtqa_total_list = []
    mtqo_total_list = []

    # MTQの消費電力計算
    for curs_mtqa_x, curs_mtqa_y, curs_mtqa_z, curs_mtqo_z2, curs_mtqo_z3, curs_mtqo_z4, vols_mtqa, vols_mtqo_plasma in zip(
        extracted_list["curs_mtqx"],
        extracted_list["curs_mtqy"],
        extracted_list["curs_mtqz1"],
        extracted_list["curs_mtqz2"],
        extracted_list["curs_mtqz3"],
        extracted_list["curs_mtqz4"],
        extracted_list["vols_mtqa"],
        extracted_list["vols_mtqo_plasma"],
    ):
    
        result = calc_mtq(
            curs_mtqa_x, curs_mtqa_y, curs_mtqa_z, curs_mtqo_z2, curs_mtqo_z3, curs_mtqo_z4, vols_mtqa, vols_mtqo_plasma
        )
    
        # リストに値を格納
        mtqa_x_list.append(result["pwr_mtqa_x"])
        mtqa_y_list.append(result["pwr_mtqa_y"])
        mtqa_z_list.append(result["pwr_mtqa_z"])
        mtqo_z2_list.append(result["pwr_mtqo_z2"])
        mtqo_z3_list.append(result["pwr_mtqo_z3"])
        mtqo_z4_list.append(result["pwr_mtqo_z4"])
        mtqa_total_list.append(result["pwr_mtqa_total"])
        mtqo_total_list.append(result["pwr_mtqo_total"])
    
    # extracted_listに列を追加
    org.dict_append("pwr_mtqa_x", mtqa_x_list, extracted_list)
    org.dict_append("pwr_mtqa_y", mtqa_y_list, extracted_list)
    org.dict_append("pwr_mtqa_z", mtqa_z_list, extracted_list)
    org.dict_append("pwr_mtqo_z2", mtqo_z2_list, extracted_list)
    org.dict_append("pwr_mtqo_z3", mtqo_z3_list, extracted_list)
    org.dict_append("pwr_mtqo_z4", mtqo_z4_list, extracted_list)
    org.dict_append("pwr_mtqa_total", mtqa_total_list, extracted_list)
    org.dict_append("pwr_mtqo_total", mtqo_total_list, extracted_list)
    #-------------------------------------------------------------------------

    return extracted_list

