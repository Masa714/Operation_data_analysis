"""
date:2026/04/26
author:ikuta
this file for valiables 
"""

#---------------------------------------------------
# Parameters

orbit_cycle = 6000 # 軌道1周の周期[s]
excel_base_time = "1900/01/01 0:00:00.00" # OBC_Timeが0の時のcsvファイル表記

# 以下はRTCのHK D/Lの際にモニターに出てくる値 (PC TimeとOBC Time)で更新　 
# MOBC再起動したら更新すること！
# 1U
OBC_time_sample_1U = "83:51:24.000" # OBCtimeをUTCに変換する際に使用 (HKのcsvにあるOBC Timeを入れないこと！ 時刻表記ではなく, 累積時間表記で記入)
UTC_time_sample_1U = "2026/06/07 02:45:17.281764" # OBCtimeをUTCに変換する際に使用 (PC Timeを使用)
# 2U
OBC_time_sample_2U = "225:04:57.000" # OBCtimeをUTCに変換する際に使用 (HKのcsvにあるOBC Timeを入れないこと！ 時刻表記ではなく, 累積時間表記で記入)
UTC_time_sample_2U = "2026/05/25 02:45:14.990250" # OBCtimeをUTCに変換する際に使用(PC Timeを使用)

# 抽出方法について　(基本はfloatとして抽出される)
non_float_header = ["OBC Time"] # floatに変換してほしくないものを記載 (時刻など)

# プロットの設定(一般的なもの)
plot_enable = 0 # 0：描画しない,  1：描画する
utc_fontsize = 6 # 時刻歴の横軸メモリのフォントサイズ
apply_time_condition = True # plot_timerangeを使用するかどうか True：使用する, False：使用しない
plot_timerange = 100 # 時刻歴について、一番時刻が古いデータから何分間のデータをプロットするのか TLCとRTCのHKが混ざったときの対策 
                     # 使用しない場合, csvファイル内の全てのデータをプロットする
time_tick_interval = int(plot_timerange * 0.2) # 時刻歴-横軸の目盛り間隔(整数)  timerangeの5分の1程度がいい, 自分で設定する際は「interval=数字(分)」で設定
#-----------------------------------------------------------------------------------------
# extra operation

#おまけ機能
# その1
wanna_convert_enable = 0 # 任意のutc時刻をobctimeに変換する機能を使うかどうか 0:不使用, 1:使用
wanna_convert_obc_time_1U = "2026/05/07 3:28:12.000000" # おまけ機能：任意のutctimeをobcに変換
wanna_convert_obc_time_2U = "2026/05/07 3:28:12.000000" # おまけ機能：任意のutctimeをobcに変換



