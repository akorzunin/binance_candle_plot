

class StopLoss(object): 
    '''docstring for StopLoss'''
    def __init__(self, **kwargs):
        super(StopLoss, self).__init__()
        self._STOP_LOSS_THRESHOLD = kwargs.pop('STOP_LOSS_THRESHOLD', None)
        self._stop_loss_count = 0 

    def stop_loss_alg(self, **kwargs):
        trade_data = kwargs.pop('trade_data', None)
        p_trdr = kwargs.pop('p_trdr', None)
        row = kwargs.pop('row', None)
        # stop_loss_trade_flag = kwargs.pop('stop_loss_trade_flag', None)

        try:
            prev_buy = trade_data.iloc[-1]['buy_price']
            prev_op = trade_data.iloc[-1]['type']
        except IndexError: prev_buy = None

        if prev_buy is not None:
            curr_buy_pr = float(row['open_'])
                    # percent_loss показывает на сколько изменилась цена отностительно последней покупки в процентах
            percent_loss = (curr_buy_pr - prev_buy)*100/prev_buy
        else: percent_loss = 0
        # r = lambda x: round(x, 4)

        if percent_loss < self._STOP_LOSS_THRESHOLD and prev_op == 'buy':
            # logging.info(f"[STOP LOSS]{r(percent_loss)=} abs_loss{r(curr_buy_pr-prev_buy)} {r(prev_buy)=} {r(curr_buy_pr)=} {row['date_created']}")
            # sell money
            p_trdr.trade(
                            amount=p_trdr.main_currency_amount, 
                            trade_type="SELL", 
                            sell_price=float(row['open_']),
                            buy_price=float(row['open_']),
                        )
            trade_data.loc[len(trade_data)] = p_trdr.get_df(timestamp=row['date_created']).squeeze()
            stop_loss_trade_flag = True
            self._stop_loss_count += 1
        else: stop_loss_trade_flag = False

        return stop_loss_trade_flag, trade_data

    @property
    def stop_loss_count(self):
        return self._stop_loss_count

    @property
    def STOP_LOSS_THRESHOLD(self):
        return self._STOP_LOSS_THRESHOLD


if __name__ == '__main__':
    STOP_LOSS_THRESHOLD = -1

    s = StopLoss(
        STOP_LOSS_THRESHOLD=STOP_LOSS_THRESHOLD,
    )
    print(s.STOP_LOSS_THRESHOLD)
    print(s.stop_loss_count)