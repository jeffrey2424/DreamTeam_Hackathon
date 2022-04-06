"""
    Static history of ticker downloads. Currently uses list of FTSE250 companies

    Downloads a csv of High, Low, Open, Close, Volume for every ticker for a given date range and interval.

    e.g.
        python finance_eda.py "2022-03-05" "2022-04-05" 1d 
"""
import yfinance as yf
import argparse


ticker_string_ftse250 = "3IN FOUR 888 ASL APEO ATST ATT APAX ASCL ASHM AGR AML ATG AGT BAB BGFD USA BBY BCG BNKR BBGI BEZ AJB BBH BWY BHMG BIFF BYG BRSC THRG BRWM BCPT BGSC BOY BRW BPT BVIC BYIT CCR CLDN CAPC CGT CNE CCL CEY CNA CHG CHRY CTY CKN CLG CBG CLI CMCX COA CCC GLO CTEC CSP CWK CRST CURY DARK DLN DPLM DLG DSCV DEC DOM DRX DOCS DNLM EZJ EDIN EWI ELM ENOG ESNT ERM JEO FDM FXPO FCSS FEML FEV FSV FGT FGP FCIT FRAS FUTR GAW GCP GEN GNS GFTU GRI GPOR UKW GNC GRG HMSO HBR HVPE HAS HTWS HSL HRI HGT HICL HILS HFG SONG HSX HOC HSV IBST ICGT IGG IMI IEM INCH INDV IHP INPP INVP IPO IWG JMAT JAM JMG JEDT JFJ JTC JUP JUST KNOS LRE LWDB LIO LMP LXI EMG MKS MSLH MDC MRC MCRO MAB MTO GROW MONY MNKS MOON MGAM MGNS MUT MYI NEX NETW NBPE NCC N91 OSB OXB OXIG PAGE PIN PAG PNN PNL PHLL PETS PTEC PLUS PCT PFD PHP PFG PRTC PZC QQ QLT RNK RAT REDD RDW RSW RHIM RCP ROR RICA SAFE SNN SVS SDP SOI SAIN SEIT SEQI SRP SHB SRE SSON SCT SXS SPI SPT SSPG SYNC SYNT TATE TBCG TEP TMPL TEM TRIG TIFS TCAP TRN TPK BBOX EBOX TRY TRST TUI TLW TYMN UKCM ULE UTG SHED VSVS VCT VEIL VOF VMUK VTY VVO FAN WOSG WEIR JDW SMWH WTAN WIZZ WG WKP WWH XPP"
ticker_string_ftse100 = "III ABDN ADM AAF AAL ANTO AHT ABF AZN AUTO AVST AVV AV BME BA BARC BDEV BKG BP BATS BLND BT-A BNZL BRBY CCH CPG CRH CRDA DCC DPH DGE ECM EDV ENT EXPN FERG FLTR FRES GSK GLEN HLMA HL HIK HWDN HSBA IHG IMB INF ICP IAG ITRK ITV JD KGF LAND LGEN LLOY LSEG MNG MGGT MRO MNDI NG NWG NXT OCDO PSON PSH PSN PHNX PRU RKT REL RTO RMV RIO RR RMG SGE SBRY SDR SMT SGRO SVT SHEL SMDS SMIN SN SKG SPX SSE STAN STJ TW TSCO ULVR UU VOD WTB WPP"

ticker_list_ftse250 = ['3IN.L', 'FOUR', '888.L', 'ASL.L', 'APEO.L', 'ATST.L', 'ATT.L', 'APAX.L', 'ASCL.L', 'ASHM.L', 'AGR', 'AML.L', 'ATG.L', 'AGT', 'BAB', 'BGFD.L', 'USA', 'BBY', 'BCG.L', 'BNKR.L', 'BBGI', 'BEZ.L', 'AJB.L', 'BBH', 'BWY.L', 'BHMG.L', 'BIFF.L', 'BYG.L', 'BRSC.L', 'THRG.L', 'BRWM.L', 'BCPT.L', 'BGSC.L', 'BOY.L', 'BRW', 'BPT', 'BVIC.L', 'BYIT.L', 'CCR.L', 'CLDN.L', 'CAPC', 'CGT.L', 'CNE.L', 'CCL', 'CEY', 'CNA', 'CHG.L', 'CHRY.L', 'CTY.L', 'CKN.L', 'CLG.L', 'CBG.L', 'CLI.L', 'CMCX.L', 'COA.L', 'CCC.L', 'GLO', 'CTEC', 'CSP.L', 'CWK', 'CRST.L', 'CURY.L', 'DARK.L', 'DLN', 'DPLM.L', 'DLG.L', 'DSCV.L', 'DEC.L', 'DOM.L', 'DRX.L', 'DOCS', 'DNLM.L', 'EZJ', 'EDIN.L', 'EWI', 'ELM.L', 'ENOG.L', 'ESNT', 'ERM', 'JEO.L', 'FDM', 'FXPO.L', 'FCSS.L', 'FEML.L', 'FEV.L', 'FSV', 'FGT.L', 'FGP.L', 'FCIT', 'FRAS.L', 'FUTR.L', 'GAW.L', 'GCP', 'GEN.L', 'GNS.L', 'GFTU.L', 'GRI', 'GPOR', 'UKW.L', 'GNC.L', 'GRG.L', 'HMSO.L', 'HBR.L', 'HVPE.L', 'HAS', 'HTWS.L', 'HSL.L', 'HRI', 'HGT.L', 'HICL.L', 'HILS', 'HFG.L', 'SONG.L', 'HSX.L', 'HOC.L', 'HSV.L', 'IBST.L', 'ICGT.L', 'IGG.L', 'IMI.L', 'IEM.L', 'INCH.L', 'INDV.L', 'IHP.L', 'INPP.L', 'INVP.L', 'IPO', 'IWG.L', 'JMAT.L', 'JAM.L', 'JMG.L', 'JEDT.L', 'JFJ.L', 'JTC.L', 'JUP.L', 'JUST', 'KNOS', 'LRE.L', 'LWDB.L', 'LIO.L', 'LMP.L', 'LXI.L', 'EMG.L', 'MKS.L', 'MSLH.L', 'MDC', 'MRC', 'MCRO', 'MAB.L', 'MTO.L', 'GROW', 'MONY.L', 'MNKS.L', 'MOON', 'MGAM.L', 'MGNS.L', 'MUT.L', 'MYI', 'NEX', 'NETW.L', 'NBPE.L', 'NCC.L', 'N91.L', 'OSB.L', 'OXB.L', 'OXIG.L', 'PAGE.L', 'PIN', 'PAG', 'PNN.L', 'PNL.L', 'PHLL.L', 'PETS', 'PTEC.L', 'PLUS', 'PCT', 'PFD', 'PHP.L', 'PFG', 'PRTC', 'PZC', 'QQ.L', 'QLT.L', 'RNK.L', 'RAT.L', 'REDD.L', 'RDW', 'RSW.L', 'RHIM.L', 'RCP.L', 'ROR.L', 'RICA.L', 'SAFE', 'SNN', 'SVS.L', 'SDP', 'SOI', 'SAIN.L', 'SEIT.L', 'SEQI.L', 'SRP.L', 'SHB.L', 'SRE', 'SSON.L', 'SCT.L', 'SXS.L', 'SPI', 'SPT', 'SSPG.L', 'SYNC.L', 'SYNT.L', 'TATE.L', 'TBCG.L', 'TEP.L', 'TMPL.L', 'TEM.L', 'TRIG.L', 'TIFS.L', 'TCAP.L', 'TRN', 'TPK.L', 'BBOX.L', 'EBOX.L', 'TRY.L', 'TRST', 'TUI.L', 'TLW.L', 'TYMN.L', 'UKCM.L', 'ULE', 'UTG', 'SHED.L', 'VSVS.L', 'VCT.L', 'VEIL.L', 'VOF.L', 'VMUK.L', 'VTY.L', 'VVO.L', 'FAN', 'WOSG.L', 'WEIR.L', 'JDW.L', 'SMWH.L', 'WTAN.L', 'WIZZ.L', 'WG.L', 'WKP.L', 'WWH.L', 'XPP']

def get_data(start_date, end_date, interval):

    data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = ticker_list_ftse250,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            # period = "ytd",
            start = start_date,
            end = end_date,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = interval,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy = None
        )


    data.to_csv(f"{start_date}_{end_date}_{interval}_ftse250.csv")


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('start_date', type=str,
                        help='Start date YYYY-MM-DD')
    parser.add_argument('end_date', type=str,
                        help='End date YYYY-MM-DD')
    parser.add_argument('interval', type=str,
                        help='1 Day = 1d')

    args = parser.parse_args()   
    get_data(args.start_date, args.end_date, args.interval)