#/usr/bin/python -f
import os
import requests
import json
from ROOT import *

application_id="1234abcd" # get your application ID
user_name="tkhoge"
m_debug=False

def get_tankopedia():
    params = (
        ('application_id', application_id),
        ('language', 'en'),
        ('fields', 'name,tier,tank_id,type,nation'),
    )
    response = requests.get('https://api.wotblitz.asia/wotb/encyclopedia/vehicles/', params=params)
    global tank_data
    tank_data = response.json()['data']
# end get_tankopedia()

def get_userid():
    params = (
        ('application_id', application_id),
        ('search', user_name),
    )
    response = requests.get('https://api.wotblitz.asia/wotb/account/list/', params=params)
    user_data = response.json()
    global account_id
    account_id = json.dumps(user_data["data"][0]["account_id"])
# end get_userid()

def get_stats():
    params = (
        ('application_id', application_id),
        ('account_id', account_id),
    )
    response = requests.get('https://api.wotblitz.asia/wotb/tanks/stats/', params=params)
    global tank_stats
    tank_stats = response.json()["data"][account_id]
# end get_stats()

if __name__ == '__main__':
    # access tankopedia
    get_tankopedia()
    if m_debug:
        print json.dumps(tank_data, indent=4)

    # get account_id
    get_userid()
    print "user: " + user_name + "\t" + "account_id: " + account_id

    # get stats
    get_stats()
    if m_debug:
        print json.dumps(tank_stats, indent=4)    
        
    # TH1 definitions
    h_LT_all = TH1D("h_LT_all", "h_LT_all", 10, 1.0, 11.0)
    h_MT_all = TH1D("h_MT_all", "h_MT_all", 10, 1.0, 11.0)
    h_HT_all = TH1D("h_HT_all", "h_HT_all", 10, 1.0, 11.0)
    h_TD_all = TH1D("h_TD_all", "h_TD_all", 10, 1.0, 11.0)
    h_LT_win = TH1D("h_LT_win", "h_LT_win", 10, 1.0, 11.0)
    h_MT_win = TH1D("h_MT_win", "h_MT_win", 10, 1.0, 11.0)
    h_HT_win = TH1D("h_HT_win", "h_HT_win", 10, 1.0, 11.0)
    h_TD_win = TH1D("h_TD_win", "h_TD_win", 10, 1.0, 11.0)

    h_ussr_all    = TH1D("h_ussr_all", "h_ussr_all", 10, 1.0, 11.0)
    h_ussr_win    = TH1D("h_ussr_win", "h_ussr_win", 10, 1.0, 11.0)
    h_usa_all     = TH1D("h_usa_all", "h_usa_all", 10, 1.0, 11.0)
    h_usa_win     = TH1D("h_usa_win", "h_usa_win", 10, 1.0, 11.0) 
    h_germany_all = TH1D("h_germany_all", "h_germany_all", 10, 1.0, 11.0)
    h_germany_win = TH1D("h_germany_win", "h_germany_win", 10, 1.0, 11.0)
    h_france_all  = TH1D("h_france_all", "h_france_all", 10, 1.0, 11.0)
    h_france_win  = TH1D("h_france_win", "h_france_win", 10, 1.0, 11.0)
    h_uk_all      = TH1D("h_uk_all", "h_uk_all", 10, 1.0, 11.0)
    h_uk_win      = TH1D("h_uk_win", "h_uk_win", 10, 1.0, 11.0)
    h_japan_all   = TH1D("h_japan_all", "h_japan_all", 10, 1.0, 11.0)
    h_japan_win   = TH1D("h_japan_win", "h_japan_win", 10, 1.0, 11.0)
    h_china_all   = TH1D("h_china_all", "h_china_all", 10, 1.0, 11.0)
    h_china_win   = TH1D("h_china_win", "h_china_win", 10, 1.0, 11.0) 
    h_other_all   = TH1D("h_other_all", "h_other_all", 10, 1.0, 11.0)
    h_other_win   = TH1D("h_other_win", "h_other_win", 10, 1.0, 11.0)

    h_damage_dealt = TH2D("h_damage_dealt", "h_damage_dealt", 10, 1.0, 11.0, 80, 0.0, 4000.0)
    
    # analyses
    for key in tank_stats:
        this_tankID =  key['tank_id']
        this_tankDict   = tank_data[str(this_tankID)]
        this_tankTier   = this_tankDict['tier']
        this_tankNation = this_tankDict['nation']
        this_tankType   = this_tankDict['type']

        this_battles = key['all']['battles']
        this_wins    = key['all']['wins']
        this_damage_dealt   = key['all']['damage_dealt']
        this_average_damage = float(this_damage_dealt)/float(this_battles)
        h_damage_dealt.Fill(this_tankTier, this_average_damage)
        
        if this_tankType == "lightTank":
            for i_battle in range(1, this_battles):
                h_LT_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_LT_win.Fill(this_tankTier)
        elif this_tankType == "mediumTank":
            for i_battle in range(1, this_battles):
                h_MT_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_MT_win.Fill(this_tankTier)
        elif this_tankType == "heavyTank": 
            for i_battle in range(1, this_battles):
                h_HT_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_HT_win.Fill(this_tankTier)
        elif this_tankType == "AT-SPG":
            for i_battle in range(1, this_battles):
                h_TD_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_TD_win.Fill(this_tankTier)
        
        if this_tankNation == "ussr": 
            for i_battle in range(1, this_battles):
                h_ussr_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_ussr_win.Fill(this_tankTier)
        elif this_tankNation == "usa":
            for i_battle in range(1, this_battles):
                h_usa_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_usa_win.Fill(this_tankTier)
        elif this_tankNation == "germany":
            for i_battle in range(1, this_battles):
                h_germany_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_germany_win.Fill(this_tankTier)
        elif this_tankNation == "france":
            for i_battle in range(1, this_battles):
                h_france_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_france_win.Fill(this_tankTier)
        elif this_tankNation == "uk":
            for i_battle in range(1, this_battles):
                h_uk_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_uk_win.Fill(this_tankTier)
        elif this_tankNation == "japan":
            for i_battle in range(1, this_battles):
                h_japan_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_japan_win.Fill(this_tankTier)
        elif this_tankNation == "china":
            for i_battle in range(1, this_battles):
                h_china_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_china_win.Fill(this_tankTier)
        elif this_tankNation == "other":
            for i_battle in range(1, this_battles):
                h_other_all.Fill(this_tankTier)
            for i_win in range(1, this_wins):
                h_other_win.Fill(this_tankTier)


                
    # TEfficiency
    eff_LT = TEfficiency(h_LT_win, h_LT_all)
    eff_LT.SetLineColor(4)
    eff_LT.SetMarkerColor(4)
    eff_LT.SetMarkerStyle(24)
    eff_MT = TEfficiency(h_MT_win, h_MT_all) 
    eff_MT.SetLineColor(3)
    eff_MT.SetMarkerColor(3)
    eff_MT.SetMarkerStyle(26)
    eff_HT = TEfficiency(h_HT_win, h_HT_all)
    eff_HT.SetLineColor(2)
    eff_HT.SetMarkerColor(2)
    eff_HT.SetMarkerStyle(25)
    eff_TD = TEfficiency(h_TD_win, h_TD_all)
    eff_TD.SetLineColor(6)
    eff_TD.SetMarkerColor(6)
    eff_TD.SetMarkerStyle(34)

    # Axis
    h_axis = TH1D("h_axis", (user_name+"; Tier; Win Rate"), 10, 1.0, 11.0)
    h_axis.GetXaxis().SetBinLabel(1, "1")
    h_axis.GetXaxis().SetBinLabel(2, "2")
    h_axis.GetXaxis().SetBinLabel(3, "3")
    h_axis.GetXaxis().SetBinLabel(4, "4")
    h_axis.GetXaxis().SetBinLabel(5, "5")
    h_axis.GetXaxis().SetBinLabel(6, "6")
    h_axis.GetXaxis().SetBinLabel(7, "7")
    h_axis.GetXaxis().SetBinLabel(8, "8")
    h_axis.GetXaxis().SetBinLabel(9, "9")
    h_axis.GetXaxis().SetBinLabel(10, "10")
    h_axis.GetYaxis().SetRangeUser(0.2, 0.8)
    
    # Draw
    gStyle.SetOptStat(0000000)
    c = TCanvas("c", "c")
    h_axis.Draw()

    h_leg_type = TLegend(0.5, 0.2, 0.85, 0.4)
    h_leg_type.SetBorderSize(0)
    h_leg_type.SetEntrySeparation(0.02)
    h_leg_type.SetMargin(0.15)
    h_leg_type.SetTextFont(42)
    h_leg_type.AddEntry(eff_LT, "Light Tanks", "lp")
    h_leg_type.AddEntry(eff_MT, "Medium Tanks", "lp")
    h_leg_type.AddEntry(eff_HT, "Heavy Tanks", "lp")
    h_leg_type.AddEntry(eff_TD, "Tank Destroyers", "lp")
    
    eff_LT.Draw("same")
    eff_MT.Draw("same")
    eff_HT.Draw("same")
    eff_TD.Draw("same")
    h_leg_type.Draw()
    if not os.path.exists("figures"):
        os.makedirs("figures")
    c.Print("figures/Type_Tier.pdf")
    c.Print("figures/Type_Tier.jpg")
    c.Print("figures/Type_Tier.png")

    c.Clear()

    h_damage_dealt.SetTitle(user_name)
    h_damage_dealt.GetXaxis().SetTitle("Tier")
    h_damage_dealt.GetYaxis().SetTitle("Average Damage")
    h_damage_dealt.GetYaxis().SetTitleOffset(1.3)
    h_damage_dealt.GetXaxis().SetBinLabel(1, "1")
    h_damage_dealt.GetXaxis().SetBinLabel(2, "2")
    h_damage_dealt.GetXaxis().SetBinLabel(3, "3")
    h_damage_dealt.GetXaxis().SetBinLabel(4, "4")
    h_damage_dealt.GetXaxis().SetBinLabel(5, "5")
    h_damage_dealt.GetXaxis().SetBinLabel(6, "6")
    h_damage_dealt.GetXaxis().SetBinLabel(7, "7")
    h_damage_dealt.GetXaxis().SetBinLabel(8, "8")
    h_damage_dealt.GetXaxis().SetBinLabel(9, "9")
    h_damage_dealt.GetXaxis().SetBinLabel(10, "10")
    
    h_damage_dealt.Draw("COLZ")
    iTier=1
    this_line_1 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_1.SetLineColor(2)
    this_line_1.SetLineWidth(3)
    this_line_1.SetLineStyle(2)
    this_line_1.Draw()
    iTier=2
    this_line_2 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_2.SetLineColor(2)
    this_line_2.SetLineWidth(3)
    this_line_2.SetLineStyle(2)
    this_line_2.Draw()
    iTier=3
    this_line_3 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_3.SetLineColor(2)
    this_line_3.SetLineWidth(3)
    this_line_3.SetLineStyle(2)
    this_line_3.Draw()
    iTier=4
    this_line_4 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_4.SetLineColor(2)
    this_line_4.SetLineWidth(3)
    this_line_4.SetLineStyle(2)
    this_line_4.Draw()
    iTier=5
    this_line_5 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_5.SetLineColor(2)
    this_line_5.SetLineWidth(3)
    this_line_5.SetLineStyle(2)
    this_line_5.Draw()
    iTier=6
    this_line_6 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_6.SetLineColor(2)
    this_line_6.SetLineWidth(3)
    this_line_6.SetLineStyle(2)
    this_line_6.Draw()
    iTier=7
    this_line_7 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_7.SetLineColor(2)
    this_line_7.SetLineWidth(3)
    this_line_7.SetLineStyle(2)
    this_line_7.Draw()
    iTier=8
    this_line_8 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_8.SetLineColor(2)
    this_line_8.SetLineWidth(3)
    this_line_8.SetLineStyle(2)
    this_line_8.Draw()
    iTier=9
    this_line_9 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_9.SetLineColor(2)
    this_line_9.SetLineWidth(3)
    this_line_9.SetLineStyle(2)
    this_line_9.Draw()
    iTier=10
    this_line_10 = TLine( (iTier), (iTier*200), (iTier+1), (iTier*200))
    this_line_10.SetLineColor(2)
    this_line_10.SetLineWidth(3)
    this_line_10.SetLineStyle(2)
    this_line_10.Draw()

    if not os.path.exists("figures"):
        os.makedirs("figures")
    c.Print("figures/Ave_Damage.pdf")
    c.Print("figures/Ave_Damage.jpg")
    c.Print("figures/Ave_Damage.png")
