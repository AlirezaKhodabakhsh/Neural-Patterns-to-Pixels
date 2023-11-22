def time_resolution(i:str):

    m = int(i[-2:])
    h = int(i[:2])

    if 0<=m<15:
        m=00
    elif 15<=m<30:
        m=30
    elif 30<=m<45:
        m=30
    elif m>=45:
        m=0
        h+=1

    if m<10 and h<10:
        i = str(h).zfill(2) + ':' + str(m).zfill(2)
    elif m<10:
        i = str(h) + ':' + str(m).zfill(2)
    elif h<10:
        i = str(h).zfill(2) + ':' + str(m)
    else:
        i = str(h) + ':' + str(m)


    return i


import pandas as pd

data = pd.read_excel("sleep_habits.xlsx", index_col=0)


date_s = list(data['dates'])
sleep_time_s = list(data['sleep times'])
wakeup_time_s = list(data['wakeup times'])
start_morning_time_s = list(data['start morning times'])
start_noon_time_s = list(data['start noon times'])

from datetime import date
today = date.today()
d = today.strftime("%d/%b")
if d in date_s:
    raise RuntimeError("Sleep Time at {} has been already recorded!".format(d))


sleep_time = time_resolution(input('When you fell to sleep at {}?'.format(d)))
wakeup_time = time_resolution(input('When you get up at {}?'.format(d)))
start_morning_time = time_resolution(input('When you start morning at {}?'.format(d)))
start_noon_time = time_resolution(input('When you start noon at {}?'.format(d)))
date_s.append(d)
sleep_time_s.append(sleep_time)
wakeup_time_s.append(wakeup_time)
start_morning_time_s.append(start_morning_time)
start_noon_time_s.append(start_noon_time)


d = {
    "dates": pd.Series(date_s),
    "sleep times": pd.Series(sleep_time_s),
    "wakeup times": pd.Series(wakeup_time_s),
    "start morning times" : pd.Series(start_morning_time_s),
    "start noon times" : pd.Series(start_noon_time_s),
}
dft1 = pd.DataFrame(d)
dft1.to_excel("sleep_habits.xlsx")


import matplotlib.pyplot as plt
plt.figure()
plt.plot(date_s, sleep_time_s)
plt.plot(date_s, sleep_time_s, 'o')
plt.title('Sleep Time Tracker')

plt.figure()
plt.plot(date_s, wakeup_time_s)
plt.plot(date_s, wakeup_time_s, 'o')
plt.title('Wake-Up Time Tracker')


plt.figure()
plt.plot(date_s, start_morning_time_s)
plt.plot(date_s, start_morning_time_s, 'o')
plt.title('Start Morning Time Tracker')

plt.figure()
plt.plot(date_s, start_noon_time_s)
plt.plot(date_s, start_noon_time_s, 'o')
plt.title('Start Noon Time Tracker')
