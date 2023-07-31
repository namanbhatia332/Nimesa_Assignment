import requests

def is_datevalid(day,month,year,max_yr,min_yr):
    '''Checks whether date is valid or not'''
    try:
        day = int(day)
        month = int(month)
        year = int(year)
    except:
        return False
    
    if year>max_yr or year<min_yr:
        return False
    if month<1 or month>12:
        return False
    
    if ((year%100==0) and (year%400==0)) or (year%4==0):
        leap = True
    else:
        leap = False

    if month in [1,3,5,7,8,10,12] and day>=1 and day<=31:
        return True
    elif month in [4,6,9,11] and day>=1 and day<=30:
        return True
    else:
        if leap and day>=1 and day<=29:
            return True
        elif not leap and day>=1 and day<=28:
            return True
    
    return False

def display():
    '''To display the user choices'''
    print('Enter choice:')
    print('(1) Get weather')
    print('(2) Get wind speed')
    print('(3) Get pressure')
    print('(0) Exit')

def enter_date(max_year,min_year):
    '''To enter the date. It returns whether the date is valid or not and return the day,month,year of the entered date'''
    print('\nEnter date')
    d = input('Day-> ')
    m = input('Month-> ')
    y = input('Year-> ')
    return [is_datevalid(d,m,y,max_year,min_year),d,m,y]

def formatted_date(d,m,y):
    if len(d)==1:
        d = '0' + d
    if len(m)==1:
        m = '0' + m
    return f'{y}-{m}-{d}'

#main



#data collection
URL = 'https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22'
response = requests.get(URL)

#customisable year ranges to validate the date entered by the user
max_year = 2025
min_year = 1900

#data manipulation
#data will be in the form of
# data = {
#     date1:{
#         time1:{
#             temp:value,
#             windspeed:value,
#             pressure:value
#         },
#         time2:{
#             temp:value,
#             windspeed:value,
#             pressure:value
#         },.....
#     }
#     date2:{....}
# }
result = response.json()
objs = result['list']
data = {}
for obj in objs:
    date = obj['dt_txt'][:10]
    time = obj['dt_txt'][-8:]

    if date in data:
        data[date][time] = {
            'Temp': obj['main']['temp'],
            'WindSpeed': obj['wind']['speed'],
            'Pressure': obj['main']['pressure']
        }
    else:
        data[date] = {
            time:
            {
                'Temp': obj['main']['temp'],
                'WindSpeed': obj['wind']['speed'],
                'Pressure': obj['main']['pressure']
            }
                      }


#user interface begins here
while True:
    
    display()

    ch = input()
    #check whether the entered choice is valid or not
    if ch not in ['0','1','2','3']: 
        print('\nInvalid choice!')
        print('Choose again!\n')
        continue
    ch = int(ch)
    if ch==0:
        print('Thank you :)')
        break

    #check whether the entered data is valid or not and if it is invalid the program keeps on asking date till it gets a valid date
    while True:
        res = enter_date(max_year,min_year)
        if res[0]:
            date = formatted_date(res[1],res[2],res[3])

            #checks whether the entered valid date is present or not in the response provided by the api
            if date not in data:
                print('\nSorry, date not present in database!')
                print('Please choose another date!\n')
                continue

            break
        
        print('\nInvalid Date!')
        print('Enter again!')

    print('\nDate->',date)

    #switch case
    if ch==1:
        for time in data[date]:
            print(f"Time-> {time}\t Temp->{data[date][time]['Temp']}")
    elif ch==2:
        for time in data[date]:
            print(f"Time-> {time}\t Wind Speed->{data[date][time]['WindSpeed']}")
    elif ch==3:
        for time in data[date]:
            print(f"Time-> {time}\t Pressure->{data[date][time]['Pressure']}")
    
    print()
