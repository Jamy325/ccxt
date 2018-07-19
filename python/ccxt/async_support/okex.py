# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.okcoinusd import okcoinusd


class okex (okcoinusd):

    def describe(self):
        return self.deep_extend(super(okex, self).describe(), {
            'id': 'okex',
            'name': 'OKEX',
            'countries': ['CN', 'US'],
            'has': {
                'CORS': False,
                'futures': True,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/32552768-0d6dd3c6-c4a6-11e7-90f8-c043b64756a7.jpg',
                'api': {
                    'web': 'https://www.okex.com/v2',
                    'public': 'https://www.okex.com/api',
                    'private': 'https://www.okex.com/api',
                },
                'www': 'https://www.okex.com',
                'doc': 'https://github.com/okcoin-okex/API-docs-OKEx.com',
                'fees': 'https://www.okex.com/fees.html',
            },
            'commonCurrencies': {
                'CAN': 'Content And AD Network',
                'FAIR': 'FairGame',
                'MAG': 'Maggie',
                'YOYO': 'YOYOW',
            },
            'options': {
                'fetchTickersMethod': 'fetchTickersFromApi',
            },
        })

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        key = 'quote'
        rate = market[takerOrMaker]
        cost = float(self.cost_to_precision(symbol, amount * rate))
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(self.fee_to_precision(symbol, cost)),
        }

    async def fetch_markets(self):
        markets = await super(okex, self).fetch_markets()
        # TODO: they have a new fee schedule as of Feb 7
        # the new fees are progressive and depend on 30-day traded volume
        # the following is the worst case
        for i in range(0, len(markets)):
            if markets[i]['spot']:
                markets[i]['maker'] = 0.0015
                markets[i]['taker'] = 0.0020
            else:
                markets[i]['maker'] = 0.0003
                markets[i]['taker'] = 0.0005
        return markets

    async def fetch_tickers_from_api(self, symbols=None, params={}):
        await self.load_markets()
        request = {}
        response = await self.publicGetTickers(self.extend(request, params))
        tickers = response['tickers']
        timestamp = int(response['date']) * 1000
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            market = None
            if 'symbol' in ticker:
                marketId = ticker['symbol']
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
            ticker = self.parse_ticker(self.extend(tickers[i], {'timestamp': timestamp}), market)
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    async def fetch_tickers_from_web(self, symbols=None, params={}):
        await self.load_markets()
        request = {}
        response = await self.webGetSpotMarketsTickers(self.extend(request, params))
        tickers = response['data']
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    async def fetch_tickers(self, symbol=None, params={}):
        method = self.options['fetchTickersMethod']
        response = await getattr(self, method)(symbol, params)
        return response
