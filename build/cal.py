import datetime as dt
KR_HOL = {"2026-01-01","2026-02-16","2026-02-17","2026-02-18","2026-03-02","2026-05-01","2026-05-05",
          "2026-05-25","2026-06-03","2026-07-17","2026-08-17","2026-09-24","2026-09-25","2025-12-31"}
US_HOL = {"2026-01-01","2026-01-19","2026-02-16","2026-04-03","2026-05-25","2026-06-19","2026-07-03","2026-09-07"}
def days(start,end,kind,extra_hol=()):
    d=dt.date.fromisoformat(start); e=dt.date.fromisoformat(end); out=[]
    hol = set(extra_hol) | (KR_HOL if kind=="KR" else US_HOL if kind=="US" else set())
    while d<=e:
        if kind=="CRYPTO" or (d.weekday()<5 and d.isoformat() not in hol): out.append(d)
        d+=dt.timedelta(days=1)
    return out
