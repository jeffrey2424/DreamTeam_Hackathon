"""
    Static history of ticker downloads. Currently uses list of FTSE250 companies

    Downloads a csv of High, Low, Open, Close, Volume for every ticker for a given date range and interval.

    e.g.
        python finance_eda.py "2022-03-05" "2022-04-05" 1d 
"""
import yfinance as yf
import argparse
from datetime import datetime

ticker_string_ftse250 = "3IN FOUR 888 ASL APEO ATST ATT APAX ASCL ASHM AGR AML ATG AGT BAB BGFD USA BBY BCG BNKR BBGI BEZ AJB BBH BWY BHMG BIFF BYG BRSC THRG BRWM BCPT BGSC BOY BRW BPT BVIC BYIT CCR CLDN CAPC CGT CNE CCL CEY CNA CHG CHRY CTY CKN CLG CBG CLI CMCX COA CCC GLO CTEC CSP CWK CRST CURY DARK DLN DPLM DLG DSCV DEC DOM DRX DOCS DNLM EZJ EDIN EWI ELM ENOG ESNT ERM JEO FDM FXPO FCSS FEML FEV FSV FGT FGP FCIT FRAS FUTR GAW GCP GEN GNS GFTU GRI GPOR UKW GNC GRG HMSO HBR HVPE HAS HTWS HSL HRI HGT HICL HILS HFG SONG HSX HOC HSV IBST ICGT IGG IMI IEM INCH INDV IHP INPP INVP IPO IWG JMAT JAM JMG JEDT JFJ JTC JUP JUST KNOS LRE LWDB LIO LMP LXI EMG MKS MSLH MDC MRC MCRO MAB MTO GROW MONY MNKS MOON MGAM MGNS MUT MYI NEX NETW NBPE NCC N91 OSB OXB OXIG PAGE PIN PAG PNN PNL PHLL PETS PTEC PLUS PCT PFD PHP PFG PRTC PZC QQ QLT RNK RAT REDD RDW RSW RHIM RCP ROR RICA SAFE SNN SVS SDP SOI SAIN SEIT SEQI SRP SHB SRE SSON SCT SXS SPI SPT SSPG SYNC SYNT TATE TBCG TEP TMPL TEM TRIG TIFS TCAP TRN TPK BBOX EBOX TRY TRST TUI TLW TYMN UKCM ULE UTG SHED VSVS VCT VEIL VOF VMUK VTY VVO FAN WOSG WEIR JDW SMWH WTAN WIZZ WG WKP WWH XPP"
ticker_string_ftse100 = "III ABDN ADM AAF AAL ANTO AHT ABF AZN AUTO AVST AVV AV BME BA BARC BDEV BKG BP BATS BLND BT-A BNZL BRBY CCH CPG CRH CRDA DCC DPH DGE ECM EDV ENT EXPN FERG FLTR FRES GSK GLEN HLMA HL HIK HWDN HSBA IHG IMB INF ICP IAG ITRK ITV JD KGF LAND LGEN LLOY LSEG MNG MGGT MRO MNDI NG NWG NXT OCDO PSON PSH PSN PHNX PRU RKT REL RTO RMV RIO RR RMG SGE SBRY SDR SMT SGRO SVT SHEL SMDS SMIN SN SKG SPX SSE STAN STJ TW TSCO ULVR UU VOD WTB WPP"
ticker_list_ftse250 = ['3IN.L', 'FOUR', '888.L', 'ASL.L', 'APEO.L', 'ATST.L', 'ATT.L', 'APAX.L', 'ASCL.L', 'ASHM.L', 'AGR', 'AML.L', 'ATG.L', 'AGT', 'BAB', 'BGFD.L', 'USA', 'BBY', 'BCG.L', 'BNKR.L', 'BBGI', 'BEZ.L', 'AJB.L', 'BBH', 'BWY.L', 'BHMG.L', 'BIFF.L', 'BYG.L', 'BRSC.L', 'THRG.L', 'BRWM.L', 'BCPT.L', 'BGSC.L', 'BOY.L', 'BRW', 'BPT', 'BVIC.L', 'BYIT.L', 'CCR.L', 'CLDN.L', 'CAPC', 'CGT.L', 'CNE.L', 'CCL', 'CEY', 'CNA', 'CHG.L', 'CHRY.L', 'CTY.L', 'CKN.L', 'CLG.L', 'CBG.L', 'CLI.L', 'CMCX.L', 'COA.L', 'CCC.L', 'GLO', 'CTEC', 'CSP.L', 'CWK', 'CRST.L', 'CURY.L', 'DARK.L', 'DLN', 'DPLM.L', 'DLG.L', 'DSCV.L', 'DEC.L', 'DOM.L', 'DRX.L', 'DOCS', 'DNLM.L', 'EZJ', 'EDIN.L', 'EWI', 'ELM.L', 'ENOG.L', 'ESNT', 'ERM', 'JEO.L', 'FDM', 'FXPO.L', 'FCSS.L', 'FEML.L', 'FEV.L', 'FSV', 'FGT.L', 'FGP.L', 'FCIT', 'FRAS.L', 'FUTR.L', 'GAW.L', 'GCP', 'GEN.L', 'GNS.L', 'GFTU.L', 'GRI', 'GPOR', 'UKW.L', 'GNC.L', 'GRG.L', 'HMSO.L', 'HBR.L', 'HVPE.L', 'HAS', 'HTWS.L', 'HSL.L', 'HRI', 'HGT.L', 'HICL.L', 'HILS', 'HFG.L', 'SONG.L', 'HSX.L', 'HOC.L', 'HSV.L', 'IBST.L', 'ICGT.L', 'IGG.L', 'IMI.L', 'IEM.L', 'INCH.L', 'INDV.L', 'IHP.L', 'INPP.L', 'INVP.L', 'IPO', 'IWG.L', 'JMAT.L', 'JAM.L', 'JMG.L', 'JEDT.L', 'JFJ.L', 'JTC.L', 'JUP.L', 'JUST', 'KNOS', 'LRE.L', 'LWDB.L', 'LIO.L', 'LMP.L', 'LXI.L', 'EMG.L', 'MKS.L', 'MSLH.L', 'MDC', 'MRC', 'MCRO', 'MAB.L', 'MTO.L', 'GROW', 'MONY.L', 'MNKS.L', 'MOON', 'MGAM.L', 'MGNS.L', 'MUT.L', 'MYI', 'NEX', 'NETW.L', 'NBPE.L', 'NCC.L', 'N91.L', 'OSB.L', 'OXB.L', 'OXIG.L', 'PAGE.L', 'PIN', 'PAG', 'PNN.L', 'PNL.L', 'PHLL.L', 'PETS', 'PTEC.L', 'PLUS', 'PCT', 'PFD', 'PHP.L', 'PFG', 'PRTC', 'PZC', 'QQ.L', 'QLT.L', 'RNK.L', 'RAT.L', 'REDD.L', 'RDW', 'RSW.L', 'RHIM.L', 'RCP.L', 'ROR.L', 'RICA.L', 'SAFE', 'SNN', 'SVS.L', 'SDP', 'SOI', 'SAIN.L', 'SEIT.L', 'SEQI.L', 'SRP.L', 'SHB.L', 'SRE', 'SSON.L', 'SCT.L', 'SXS.L', 'SPI', 'SPT', 'SSPG.L', 'SYNC.L', 'SYNT.L', 'TATE.L', 'TBCG.L', 'TEP.L', 'TMPL.L', 'TEM.L', 'TRIG.L', 'TIFS.L', 'TCAP.L', 'TRN', 'TPK.L', 'BBOX.L', 'EBOX.L', 'TRY.L', 'TRST', 'TUI.L', 'TLW.L', 'TYMN.L', 'UKCM.L', 'ULE', 'UTG', 'SHED.L', 'VSVS.L', 'VCT.L', 'VEIL.L', 'VOF.L', 'VMUK.L', 'VTY.L', 'VVO.L', 'FAN', 'WOSG.L', 'WEIR.L', 'JDW.L', 'SMWH.L', 'WTAN.L', 'WIZZ.L', 'WG.L', 'WKP.L', 'WWH.L', 'XPP']

nasdaq_list = ["A", "AA", "AAL", "AAP", "AAPL", "ABB", "ABBV", "ABC", "ABEV", "ABMD", "ABNB", "ABT", "ACGL", "ACH", "ACI", "ACM", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEG", "AEM", "AEP", "AER", "AES", "AFG", "AFL", "AFRM", "AGCO", "AGR", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALC", "ALGN", "ALL", "ALLY", "ALNY", "AMAT", "AMC", "AMCR", "AMD", "AME", "AMGN", "AMH", "AMOV", "AMP", "AMT", "AMX", "AMZN", "ANET", "ANSS", "ANTM", "AON", "AOS", "APA", "APD", "APH", "APO", "APP", "APTV", "AQN", "AR", "ARCC", "ARE", "ARES", "ARGX", "ASML", "ASX", "ATO", "ATVI", "AVB", "AVGO", "AVTR", "AVY", "AWK", "AXP", "AZN", "AZO", "AZPN", "BA", "BABA", "BAC", "BAH", "BAM", "BAP", "BAX", "BBD", "BBDO", "BBVA", "BBWI", "BBY", "BCE", "BCH", "BCS", "BDX", "BEKE", "BEN", "BEP", "BG", "BGNE", "BHP", "BIDU", "BIIB", "BILI", "BILL", "BIO", "BIP", "BK", "BKI", "BKNG", "BKR", "BLDR", "BLK", "BLL", "BMO", "BMRN", "BMY", "BNS", "BNTX", "BP", "BR", "BRO", "BSAC", "BSBR", "BSX", "BSY", "BTI", "BUD", "BURL", "BX", "BXP", "BZ", "C", "CAG", "CAH", "CAJ", "CAR", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCEP", "CCI", "CCJ", "CCK", "CCL", "CDNS", "CDW", "CE", "CEG", "CERN", "CF", "CFG", "CFLT", "CG", "CGNX", "CHD", "CHK", "CHKP", "CHRW", "CHT", "CHTR", "CHWY", "CI", "CIB", "CINF", "CL", "CLF", "CLR", "CLVT", "CLX", "CM", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNA", "CNC", "CNHI", "CNI", "CNP", "CNQ", "COF", "COIN", "COO", "COP", "COST", "CP", "CPB", "CPNG", "CPRT", "CPT", "CQP", "CRH", "CRL", "CRM", "CRWD", "CS", "CSCO", "CSGP", "CSL", "CSX", "CTAS", "CTLT", "CTRA", "CTSH", "CTVA", "CTXS", "CUBE", "CUK", "CVE", "CVS", "CVX", "CZR", "D", "DAL", "DAR", "DASH", "DB", "DD", "DDOG", "DE", "DELL", "DEO", "DFS", "DG", "DGX", "DHI", "DHR", "DIDI", "DIS", "DISCB", "DISCK", "DISH", "DLR", "DLTR", "DOCU", "DOV", "DOW", "DOX", "DPZ", "DRE", "DRI", "DT", "DTE", "DUK", "DVA", "DVN", "DXCM", "E", "EA", "EBAY", "EBR", "EC", "ECL", "ED", "EFX", "EIX", "EL", "ELAN", "ELP", "ELS", "EMN", "EMR", "ENB", "ENIA", "ENPH", "ENTG", "EOG", "EPAM", "EPD", "EQH", "EQIX", "EQNR", "EQR", "EQT", "ERIC", "ES", "ESS", "ET", "ETN", "ETR", "ETSY", "EVRG", "EW", "EWBC", "EXAS", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FB", "FCNCA", "FCX", "FDS", "FDX", "FE", "FERG", "FFIV", "FHN", "FICO", "FIS", "FISV", "FITB", "FLT", "FMC", "FMS", "FMX", "FNF", "FNV", "FOX", "FOXA", "FRC", "FTNT", "FTS", "FTV", "FWONA", "FWONK", "GD", "GDDY", "GE", "GFI", "GFL", "GFS", "GGB", "GGG", "GIB", "GILD", "GIS", "GL", "GLOB", "GLPI", "GLW", "GM", "GMAB", "GME", "GNRC", "GOLD", "GOOG", "GOOGL", "GPC", "GPN", "GRAB", "GRMN", "GS", "GSK", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HDB", "HEI", "HES", "HIG", "HLT", "HMC", "HOLX", "HON", "HOOD", "HPE", "HPQ", "HRL", "HSBC", "HSIC", "HST", "HSY", "HTHT", "HUBS", "HUM", "HWM", "HZNP", "IBM", "IBN", "ICE", "ICL", "ICLR", "IDXX", "IEP", "IEX", "IFF", "IHG", "ILMN", "IMO", "INCY", "INFY", "ING", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", "ISRG", "IT", "ITUB", "ITW", "IX", "J", "JBHT", "JCI", "JD", "JHX", "JKHY", "JLL", "JNJ", "JNPR", "JPM", "K", "KB", "KDP", "KEP", "KEY", "KEYS", "KHC", "KIM", "KKR", "KLAC", "KMB", "KMI", "KMX", "KO", "KOF", "KR", "L", "LAMR", "LBRDA", "LBRDK", "LBTYA", "LBTYB", "LBTYK", "LCID", "LDOS", "LEN", "LFC", "LH", "LHX", "LI", "LIN", "LKQ", "LLY", "LMT", "LNC", "LNG", "LNT", "LOGI", "LOW", "LPLA", "LRCX", "LSI", "LSXMA", "LSXMB", "LSXMK", "LU", "LULU", "LUMN", "LUV", "LVS", "LYB", "LYFT", "LYG", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDB", "MDLZ", "MDT", "MELI", "MET", "MFC", "MFG", "MGA", "MGM", "MKC", "MKL", "MKTX", "MLM", "MMC", "MMM", "MMP", "MNST", "MO", "MOH", "MORN", "MOS", "MPC", "MPLX", "MPW", "MPWR", "MRK", "MRNA", "MRO", "MRVL", "MS", "MSCI", "MSFT", "MSI", "MT", "MTB", "MTCH", "MTD", "MTN", "MU", "MUFG", "NDAQ", "NDSN", "NEE", "NEM", "NET", "NFLX", "NGG", "NI", "NICE", "NIO", "NKE", "NLOK", "NMR", "NOC", "NOK", "NOW", "NSC", "NTAP", "NTES", "NTR", "NTRS", "NU", "NUE", "NVDA", "NVO", "NVR", "NVS", "NWG", "NWS", "NWSA", "NXPI", "O", "ODFL", "OKE", "OKTA", "OMC", "ON", "ORAN", "ORCL", "ORLY", "OTEX", "OTIS", "OVV", "OXY", "PANW", "PARA", "PARAA", "PATH", "PAYC", "PAYX", "PBA", "PBR", "PCAR", "PCG", "PCTY", "PDD", "PEAK", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHG", "PINS", "PKG", "PKI", "PKX", "PLD", "PLTR", "PLUG", "PM", "PNC", "PODD", "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PTR", "PUK", "PWR", "PXD", "PYPL", "QCOM", "QGEN", "QRVO", "QSR", "RACE", "RBLX", "RCI", "RCL", "RE", "REG", "REGN", "RELX", "REXR", "RF", "RHI", "RIO", "RIVN", "RJF", "RMD", "RNG", "ROK", "ROKU", "ROL", "ROP", "ROST", "RPM", "RPRX", "RS", "RSG", "RTX", "RY", "RYAAY", "SAN", "SAP", "SBAC", "SBNY", "SBSW", "SBUX", "SCCO", "SCHW", "SCI", "SE", "SEDG", "SGEN", "SHEL", "SHG", "SHOP", "SHW", "SIRI", "SIVB", "SJM", "SJR", "SKM", "SLB", "SLF", "SMFG", "SNA", "SNAP", "SNN", "SNOW", "SNP", "SNPS", "SNY", "SO", "SONY", "SPG", "SPGI", "SPLK", "SPOT", "SQ", "SQM", "SRE", "SSL", "SSNC", "STE", "STLA", "STLD", "STM", "STT", "STX", "STZ", "SU", "SUI", "SUZ", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAK", "TAP", "TCOM", "TD", "TDG", "TDOC", "TDY", "TEAM", "TECH", "TECK", "TEF", "TEL", "TER", "TEVA", "TFC", "TFX", "TGT", "TJX", "TLK", "TM", "TMO", "TMUS", "TOST", "TPL", "TRGP", "TRI", "TRMB", "TROW", "TRP", "TRU", "TRV", "TS", "TSCO", "TSLA", "TSM", "TSN", "TT", "TTD", "TTE", "TTM", "TTWO", "TU", "TW", "TWLO", "TWTR", "TXN", "TXT", "TYL", "U", "UAL", "UBER", "UBS", "UDR", "UHAL", "UHS", "UI", "UL", "ULTA", "UMC", "UNH", "UNP", "UPS", "URI", "USB", "V", "VALE", "VEEV", "VFC", "VICI", "VIV", "VLO", "VMC", "VMW", "VOD", "VRSK", "VRSN", "VRTX", "VST", "VTR", "VTRS", "VZ", "W", "WAB", "WAT", "WBA", "WBDWV", "WCN", "WDAY", "WDC", "WEC", "WELL", "WES", "WFC", "WIT", "WLK", "WM", "WMB", "WMG", "WMT", "WOLF", "WPC", "WPM", "WPP", "WRB", "WRK", "WSM", "WSO", "WST", "WTRG", "WTW", "WY", "XEL", "XM", "XOM", "XP", "XPEV", "XRAY", "XYL", "Y", "YUM", "YUMC", "Z", "ZBH", "ZBRA", "ZEN", "ZG", "ZI", "ZM", "ZNGA", "ZS", "ZTO", "ZTS"
]

# nasdaq_list = ["A", "AA", "AAL"]

TICKERS = 'nasdaq'
TICKER_LIST = nasdaq_list


def get_data(start_date=None, end_date=None, interval=None):

    if start_date:
        inputs = {
            "start_date" : start_date,
            "end_date" : end_date,
            "interval" : interval
        }
        filename = f"{start_date}_{end_date}_{interval}_{TICKERS}.csv"

    else:
        print("No inputs provided... Collecting Year-to-date...")

        inputs = {
            "period" : '1y',
        }

        now = datetime.now()
        today = now.strftime("%Y%m%d")
        filename = f"{today}_1d_{TICKERS}.csv"

    data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = TICKER_LIST,

            **inputs,


            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            # period = "ytd",
            # start = start_date,
            # end = end_date,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            # interval = interval,

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

    print(data)
    data = data.unstack().reset_index()
    data.columns = ["Company", "Attribute", "Date", "Value"]
    data = data.pivot(index=["Date", "Company"], columns=["Attribute"], values= ['Value'])


    data.to_csv(f"{filename}")


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--start_date', required=False, type=str,  default=None,
                        help='Start date YYYY-MM-DD')

    parser.add_argument('--end_date', type=str, required=False,  default=None,
                        help='End date YYYY-MM-DD')

    parser.add_argument('--interval', type=str, required=False,  default=None,
                        help='1 Day = 1d')

    args = parser.parse_args()   
    get_data(args.start_date, args.end_date, args.interval)