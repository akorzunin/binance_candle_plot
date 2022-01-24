
import logging


class PaperTrader(object): 
    '''simulate currensy exchange operations w/ custom price, fee'''
    def __init__(self, **kwargs):
        super(PaperTrader, self).__init__()
        self.sell_price = kwargs.get('sell_price', None)  
        self.buy_price = kwargs.get('buy_price', None)

        self.fee = float(kwargs.get('fee', 0))
        self.fee_c = 1 - 0.01*self.fee

        self.main_currency_label = kwargs.get('main_currency_label', 'main_currency')
        self.secondary_currency_label = kwargs.get('secondary_currency_label', 'secondary_currency')

        self.main_currency_amount = kwargs.get('main_currency_amount', 0)
        self.secondary_currency_amount = kwargs.get('secondary_currency_amount', 0)

    def trade(self, *args, **kwargs):
        '''amount: how many of currensy been spent\n
        trade_type: sell or buy\n
            [sell] means we gonna spent {amount} of {main_currency} to buy {secondary_currency} w/ {sell_price}\n
            [buy] means we'll spend {amount} of {secondary_currency}' to buy {main_currency} w/ {buy_price}\n
        '''
        amount = kwargs.pop('amount', 0)
        trade_type = kwargs.pop('trade_type', None)
        sell_price = kwargs.pop('sell_price', None)
        buy_price = kwargs.pop('buy_price', None)
        
        if trade_type.lower() == 'sell':
            # straigt currensy conversion formula
            self.secondary_currency_amount += amount * self.fee_c * float(sell_price)
            self.main_currency_amount -= amount
            # logs
            logging.info(f'{self.main_currency_label}: {round(self.main_currency_amount, 2)}')
            logging.info(f'{self.secondary_currency_label}: {round(self.secondary_currency_amount, 2)}')
            logging.info(f'{trade_type=}')
            logging.info(f'{sell_price=}')
            
        elif trade_type.lower() == 'buy': 
            # reverse currensy conversion formula
            self.main_currency_amount += amount * self.fee_c / float(buy_price)
            self.secondary_currency_amount -= amount 
            # logs
            logging.info(f'{self.main_currency_label}: {round(self.main_currency_amount, 2)}')
            logging.info(f'{self.secondary_currency_label}: {round(self.secondary_currency_amount, 2)}')
            logging.info(f'{trade_type=}')
            logging.info(f'{buy_price=}')
            

    def get_info(self):
        logging.info(f'{self.main_currency_label}: {round(self.main_currency_amount, 2)}')
        logging.info(f'{self.secondary_currency_label}: {round(self.secondary_currency_amount, 2)}')
        logging.info(f'{self.fee=}')

    def convert_to_main(self, price):
        '''Convert all available currensy to main currensy'''
        self.trade(
            amount=self.secondary_currency_amount,
            trade_type='BUY',
            buy_price=price,
        )
        self.get_info()

    def convert_to_secondary(self, price):
        '''Convert all available currensy to secondary currensy'''
        self.trade(
            amount=self.main_currency_amount,
            trade_type='SELL',
            sell_price=price,
        )
        self.get_info()
    
    def get_main_currency(self):
        return self.main_currency_amount

    def get_secondary_currency(self):
        return self.secondary_currency_amount
    

if __name__ == '__main__':
    import logging
    DEBUG = __debug__ 
    LOG_FILE_NAME = 'log_file_name.log'
    format = '%(asctime)s [%(levelname)s]: %(message)s'
    logger = logging.basicConfig(
        filename=LOG_FILE_NAME if not DEBUG else None, 
        format=format,
        encoding='utf-8', 
        level=logging.DEBUG, 
    )
    if not DEBUG:
        logging.getLogger(logger).addHandler(logging.StreamHandler())


    p_trdr = PaperTrader(
        main_currency_label='RVN',
        secondary_currency_label='USD',
        main_currency_amount=10,
        # secondary_currency_amount=0
        fee=0.1,
        # logging_level=logging.DEBUG,
    )
    trade_type = "SELL" if 1 else "BUY"
    p_trdr.trade(
        amount=10,
        trade_type=trade_type, # buy main or sell main
        sell_price=9.9,
        buy_price=10.1,
    )
    p_trdr.get_info()
    