import datetime as dt

class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        """ amount of money or calories """
        self.comment = comment
        """ explains what money is spent on or 
        where the calories come from """
        if date is None:
            self.date = dt.date.today()
        else:    
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        """ date of the record """

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        """ daily limit of money or calories """
        self.records = []
        """ list of expenses """
        self.today = dt.date.today()
        """ determines today's date """
        self.week_ago = self.today - dt.timedelta(days=7)
        """ amount of money spent or calories received in the last 7 days """
    
    def add_record(self, record):
        self.records.append(record)
        """ adds new expenses """

    def get_today_stats(self):
        today_stats = []
        for record in self.records:
            if record.date == self.today:
                today_stats.append(record.amount)
        return sum(today_stats)
        """ amount of money spent or calories received today """ 

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)
        """ amount of money spent or calories received in the last week """

    def get_any_stats(self, count_days):
        any_stats = []
        count_days = self.today - dt.timedelta(days=count_days)
        for record in self.records:
            if self.today == dt.date.today():
                if count_days <= record.date <= self.today:
                    any_stats.append(record.amount)
        return sum(any_stats)
        """ amount of money spent or calories received in the last ... days """    

    def get_today_limit_balance(self):
        today_limit_balance = self.limit - self.get_today_stats()
        return today_limit_balance
        """ amount of money or calories remained today  """   

class CashCalculator(Calculator):
    USD_RATE = 75.0
    EURO_RATE = 90.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency="rub"):
        """ amount of money free to spend """
        currencies = {'rub': ('руб', CashCalculator.RUB_RATE),
                    'usd': ('USD', CashCalculator.USD_RATE),
                    'eur': ('Euro', CashCalculator.EURO_RATE)
                    }
        cash_remained = self.get_today_limit_balance()
        if cash_remained == 0:
            return "Денег нет, держись"
        if currency not in currencies:
            return f"Валюта {currency} не поддерживается"
        else:
            name, rate = currencies[currency]
            cash_remained = round(cash_remained / rate, 2)
            if cash_remained < 0:
                cash_remained = abs(cash_remained)
                message = (f"Денег нет, держись: твой долг - {cash_remained} "
                          f"{name}")
            else:
                message = (f"На сегодня осталось {cash_remained} "
                          f"{name}")     
        return message

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """ amount of money free to spend """
        if self.get_today_stats() < self.limit:
            calories_remained = self.get_today_limit_balance()
            message = (f"Сегодня можно съесть что-нибудь ещё, "
                      f"но с общей калорийностью не более {calories_remained} кКал")
        else:
            message = "Хватит есть!"
        return message              


cash_calculator = CashCalculator(2500)
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
cash_calculator.add_record(Record(amount=700, comment="Серёге за обед", date="08.11.2019"))
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
print(cash_calculator.get_today_cash_remained("usd"))

cal_calculator = CaloriesCalculator(1200)
cal_calculator.add_record(Record(amount=720, comment="макдональдс"))
cal_calculator.add_record(Record(amount=450, comment="сытный обед"))
cal_calculator.add_record(Record(amount=110, comment="яблочко", date="08.11.2019"))
print(cal_calculator.get_calories_remained())
