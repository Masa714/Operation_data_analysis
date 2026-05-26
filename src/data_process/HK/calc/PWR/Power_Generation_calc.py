"""
date:2026/05/04
author ikuta
this file for SAP Power Generation
"""
#--------------------------------------------------------
#import
import src.utils.organizing_datalist as org
#---------------------------------------------------------
# function

# 1. SAP発電量を計算する関数

def SAP_generation_func(curs_sap_px, curs_sap_py, curs_sap_pz, curs_sap_mx, curs_sap_my, vols_sap1, vols_sap2):

    # 各面のSAP発電量計算
    gene_px = curs_sap_px * vols_sap1 #px面
    gene_py = curs_sap_py * vols_sap1 #py面
    gene_pz = curs_sap_pz * vols_sap1 #pz面
    gene_mx = curs_sap_mx * vols_sap2 #mx面
    gene_my = curs_sap_my * vols_sap2 #my面
    
    # SAPのP,M面の合計
    gene_P = gene_px + gene_py + gene_pz
    gene_M = gene_mx + gene_my

    # SAPでの総発電量
    SAP_generation_total = gene_P + gene_M

    # 辞書で返す（ヘッダー付き）
    return {
        "pwr_sap_px":gene_px,
        "pwr_sap_py":gene_py,
        "pwr_sap_pz":gene_pz,
        "pwr_sap_mx":gene_mx,
        "pwr_sap_my":gene_my,
        "pwr_sap_P": gene_P,
        "pwr_sap_M": gene_M,
        "pwr_sap_total": SAP_generation_total
    }

# 2. SUNSのベクトルから正面から当たったときの発電量を概算する関数
def max_gene_estimate(SAP_generation_px, 
                      SAP_generation_py, 
                      SAP_generation_pz, 
                      SAP_generation_mx, 
                      SAP_generation_my, 
                      sun_x, 
                      sun_y, 
                      sun_z
                      ):
    # 先に太陽センサの各軸の値の逆数を計算しておく
    if sun_x != 0: #0割り防止
        inv_sunx = 1 / sun_x
    else:
        inv_sunx = 0
    if sun_y != 0: #0割り防止
        inv_suny = 1 / sun_y
    else:
        inv_suny = 0
    if sun_z != 0: #0割り防止
        inv_sunz = 1 / sun_z
    else:
        inv_sunz = 0

    # 発電量と太陽センサの値(方向余弦)から, 各面の最大発電量を概算
    if inv_sunx > 0: # 太陽ベクトルx軸が正なら、px面で発電
        max_gene_px = SAP_generation_px * inv_sunx
        max_gene_mx = 0
    else:# 太陽ベクトルx軸が負なら、mx面で発電
        max_gene_mx = -SAP_generation_mx * inv_sunx
        max_gene_px = 0
    if inv_suny > 0: # 太陽ベクトルy軸が正なら、py面で発電
        max_gene_py = SAP_generation_py * inv_suny
        max_gene_my = 0
    else:# 太陽ベクトルy軸が負なら、my面で発電
        max_gene_my = -SAP_generation_my * inv_suny
        max_gene_py = 0
    if inv_sunx > 0: # 太陽ベクトルx軸が正なら、pz面で発電
        max_gene_pz = SAP_generation_pz * inv_sunz
    else:# 太陽ベクトルx軸が負なら、発電無し
        max_gene_pz = 0

    # 辞書で返す（ヘッダー付き）
    return {
        "est_max_pwr_px":max_gene_px,
        "est_max_pwr_py":max_gene_py,
        "est_max_pwr_pz":max_gene_pz,
        "est_max_pwr_mx":max_gene_mx,
        "est_max_pwr_my":max_gene_my
    }
#----------------------------------------------------------------------------------------
# main

# SAP関連の計算を行い, 結果を全てリストに格納する
def SAP_calc_result(extracted_list):
    
    #------------------------------------------------
    # 1.の関数
    # 値格納用のリストの作成
    SAP_px_list = []
    SAP_py_list = []
    SAP_pz_list = []
    SAP_mx_list = []
    SAP_my_list = []
    SAP_P_list = []
    SAP_M_list = []
    SAP_total_list = []

    # 発電量の計算
    for curs_sap_px, curs_sap_py, curs_sap_pz, curs_sap_mx, curs_sap_my, vols_sap1, vols_sap2 in zip(
        extracted_list["curs_sap1_px"],
        extracted_list["curs_sap1_py"],
        extracted_list["curs_sap1_pz"],
        extracted_list["curs_sap2_mx"],
        extracted_list["curs_sap2_my"],
        extracted_list["vols_sap1"],
        extracted_list["vols_sap2"]
    ):

        result = SAP_generation_func(
            curs_sap_px, curs_sap_py, curs_sap_pz, curs_sap_mx, curs_sap_my, vols_sap1, vols_sap2
        )
        
        # リストに値を格納
        SAP_px_list.append(result["pwr_sap_px"])
        SAP_py_list.append(result["pwr_sap_py"])
        SAP_pz_list.append(result["pwr_sap_pz"])
        SAP_mx_list.append(result["pwr_sap_mx"])
        SAP_my_list.append(result["pwr_sap_my"])
        SAP_P_list.append(result["pwr_sap_P"])
        SAP_M_list.append(result["pwr_sap_M"])
        SAP_total_list.append(result["pwr_sap_total"])
    
    # extracted_listに列を追加
    org.dict_append("pwr_sap_px", SAP_px_list, extracted_list)
    org.dict_append("pwr_sap_py", SAP_py_list, extracted_list)
    org.dict_append("pwr_sap_pz", SAP_pz_list, extracted_list)
    org.dict_append("pwr_sap_mx", SAP_mx_list, extracted_list)
    org.dict_append("pwr_sap_my", SAP_my_list, extracted_list)
    org.dict_append("pwr_sap_P", SAP_P_list, extracted_list)
    org.dict_append("pwr_sap_M", SAP_M_list, extracted_list)
    org.dict_append("pwr_sap_total", SAP_total_list, extracted_list)
    #------------------------------------------------------------------------
    # 2.の関数
    # 値格納用のリストの作成
    est_px_list = []
    est_py_list = []
    est_pz_list = []
    est_mx_list = []
    est_my_list = []

    # 発電量の計算
    for SAP_generation_px, SAP_generation_py, SAP_generation_pz, SAP_generation_mx, SAP_generation_my, sun_x, sun_y, sun_z in zip(
        extracted_list["pwr_sap_px"],
        extracted_list["pwr_sap_py"],
        extracted_list["pwr_sap_pz"],
        extracted_list["pwr_sap_mx"],
        extracted_list["pwr_sap_my"],
        extracted_list["sunx"],
        extracted_list["suny"],
        extracted_list["sunz"]
    ):

        result = max_gene_estimate(
            SAP_generation_px, SAP_generation_py, SAP_generation_pz, SAP_generation_mx, SAP_generation_my, sun_x, sun_y, sun_z
        )
        
        # リストに値を格納
        est_px_list.append(result["est_max_pwr_px"])
        est_py_list.append(result["est_max_pwr_py"])
        est_pz_list.append(result["est_max_pwr_pz"])
        est_mx_list.append(result["est_max_pwr_mx"])
        est_my_list.append(result["est_max_pwr_my"])
        
    # extracted_listに列を追加
    org.dict_append("est_max_pwr_px", est_px_list, extracted_list)
    org.dict_append("est_max_pwr_py", est_py_list, extracted_list)
    org.dict_append("est_max_pwr_pz", est_pz_list, extracted_list)
    org.dict_append("est_max_pwr_mx", est_mx_list, extracted_list)
    org.dict_append("est_max_pwr_my", est_my_list, extracted_list)

    return extracted_list

