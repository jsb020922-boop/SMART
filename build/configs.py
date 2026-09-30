def g(top,step,n): return [top-step*i for i in range(n)]
I='../img/'
CFGS={
 'sksquare':dict(img=I+'v3_p20_x399_924x407.png',start_search='2026-03-03',cal='KR',high=2338000,high_date='2026-06-25',low=460000,low_date='2026-04-02',cur=1117000,last_ohlc=(1099000,1123000,1072000,1117000),gridvals=g(2000000,500000,4),vgridvals=g(4000000,1000000,4)),
 'hdhyundai':dict(img=I+'v3_p21_x402_926x407.png',start_search='2026-03-03',cal='KR',high=336000,high_date='2026-05-04',low=178000,low_date='2026-07-29',cur=202500,last_ohlc=(210500,211500,200000,202500),gridvals=g(300000,50000,3),vgridvals=g(500000,100000,4)),
 'hdksoe':dict(img=I+'v3_p22_x405_926x407.png',start_search='2026-03-03',cal='KR',high=488000,high_date='2026-05-11',low=314000,low_date='2026-07-29',cur=323500,last_ohlc=(333000,333500,320000,323500),gridvals=g(500000,50000,4),vgridvals=g(700000,100000,6)),
 'lselectric':dict(img=I+'v3_p23_x408_926x407.png',start_search='2026-03-03',cal='KR',high=347500,high_date='2026-05-07',low=127000,low_date='2026-03-09',cur=205500,last_ohlc=(202500,207500,201500,205500),gridvals=g(350000,50000,6),vgridvals=g(7000000,1000000,7)),
 'hanwhaaero':dict(img=I+'v3_p24_x411_926x407.png',start_search='2026-01-02',cal='KR',high=1713000,high_date='2026-03-04',low=783000,low_date='2026-07-29',cur=1016000,last_ohlc=(1043000,1043000,1000000,1016000),gridvals=g(1700000,100000,10),vgridvals=g(2500000,500000,5)),
 'dbins':dict(img=I+'v3_p25_x414_926x407.png',start_search='2026-01-02',cal='KR',high=237000,high_date='2026-02-23',low=120600,low_date='2026-01-14',cur=190800,last_ohlc=(190900,193300,189200,190800),gridvals=g(240000,10000,13),vgridvals=g(1000000,250000,4)),
 'eotech':dict(img=I+'v3_p26_x417_926x407.png',start_search='2026-03-03',cal='KR',high=628000,high_date='2026-06-15',low=230000,low_date='2026-07-29',cur=501000,last_ohlc=(468000,508000,465500,501000),gridvals=g(650000,50000,9),vgridvals=g(750000,250000,3)),
 'rfmat':dict(img=I+'v3_p27_x420_926x407.png',start_search='2026-01-02',cal='KR',high=63427,high_date='2026-05-12',low=10285,low_date='2026-01-20',cur=49000,last_ohlc=(45400,50200,44750,49000),gridvals=g(60000,10000,6),vgridvals=g(3000000,500000,6)),
 'isc':dict(img=I+'v3_p28_x423_926x407.png',start_search='2026-01-02',cal='KR',high=298000,high_date='2026-04-09',low=94800,low_date='2026-01-20',cur=209500,last_ohlc=(203500,210500,199900,209500),gridvals=g(300000,50000,5),vgridvals=g(2500000,500000,5)),
 'lseco':dict(img=I+'v3_p29_x426_926x407.png',start_search='2026-03-03',cal='KR',high=109800,high_date='2026-05-14',low=32000,low_date='2026-07-30',cur=62800,last_ohlc=(62800,62800,59300,62800),gridvals=g(110000,10000,9),vgridvals=g(3000000,500000,6)),
 'samsungsdi':dict(img=I+'v3_p30_x429_926x407.png',start_search='2026-03-03',cal='KR',high=820000,high_date='2026-04-22',low=341500,low_date='2026-07-29',cur=514000,last_ohlc=(533000,533000,505000,514000),gridvals=g(800000,100000,6),vgridvals=g(5000000,1000000,5)),
 'skinno':dict(img=I+'v3_p31_x432_919x401.png',start_search='2026-03-03',cal='KR',high=164700,high_date='2026-09-10',low=87700,low_date='2026-06-26',cur=146200,last_ohlc=(158900,158900,144100,146200),gridvals=g(160000,10000,8),vgridvals=g(6000000,1000000,6)),
 'gev':dict(img=I+'v3_p32_x435_926x407.png',start_search='2026-01-02',cal='US',high=1195.94,high_date='2026-07-06',low=636.4897,low_date='2026-01-14',cur=951.56,last_ohlc=(954.24,955.85,940.1752,951.56),gridvals=g(1200,100,7),vgridvals=g(5000000,1000000,4)),
 'anet':dict(img=I+'v3_p33_x438_926x407.png',start_search='2026-01-02',cal='US',high=214.89,high_date='2026-08-05',low=115.42,low_date='2026-03-30',cur=207.05,last_ohlc=(206.1094,207.2965,203.0987,207.05),gridvals=g(220,10,12),vgridvals=g(35000000,5000000,6)),
 'msft':dict(img=I+'v3_p34_x441_926x407.png',start_search='2026-01-02',cal='US',high=519.40,high_date='2026-09-25',low=348.5439,low_date='2026-06-25',cur=507.97,last_ohlc=(508.9625,509.22,506.13,507.97),gridvals=g(500,50,4),vgridvals=g(150000000,50000000,3)),
}
for k,v in CFGS.items():
    v.setdefault('last','2026-09-29')
