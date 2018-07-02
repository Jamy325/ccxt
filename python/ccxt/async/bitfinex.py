# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange
import base64
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import ROUND
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS


class bitfinex (Exchange):

    def describe(self):
        return self.deep_extend(super(bitfinex, self).describe(), {
            'id': 'bitfinex',
            'name': 'Bitfinex',
            'countries': ['VG'],
            'version': 'v1',
            'rateLimit': 1500,
            # new metainfo interface
            'has': {
                'CORS': False,
                'createDepositAddress': True,
                'deposit': True,
                'fetchClosedOrders': True,
                'fetchDepositAddress': True,
                'fetchTradingFees': True,
                'fetchFundingFees': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchTickers': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '3h': '3h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1D',
                '1w': '7D',
                '2w': '14D',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766244-e328a50c-5ed2-11e7-947b-041416579bb3.jpg',
                'api': 'https://api.bitfinex.com',
                'www': 'https://www.bitfinex.com',
                'doc': [
                    'https://bitfinex.readme.io/v1/docs',
                    'https://github.com/bitfinexcom/bitfinex-api-node',
                ],
            },
            'api': {
                'v2': {
                    'get': [
                        'candles/trade:{timeframe}:{symbol}/{section}',
                        'candles/trade:{timeframe}:{symbol}/last',
                        'candles/trade:{timeframe}:{symbol}/hist',
                    ],
                },
                'public': {
                    'get': [
                        'book/{symbol}',
                        # 'candles/{symbol}',
                        'lendbook/{currency}',
                        'lends/{currency}',
                        'pubticker/{symbol}',
                        'stats/{symbol}',
                        'symbols',
                        'symbols_details',
                        'tickers',
                        'today',
                        'trades/{symbol}',
                    ],
                },
                'private': {
                    'post': [
                        'account_fees',
                        'account_infos',
                        'balances',
                        'basket_manage',
                        'credits',
                        'deposit/new',
                        'funding/close',
                        'history',
                        'history/movements',
                        'key_info',
                        'margin_infos',
                        'mytrades',
                        'mytrades_funding',
                        'offer/cancel',
                        'offer/new',
                        'offer/status',
                        'offers',
                        'offers/hist',
                        'order/cancel',
                        'order/cancel/all',
                        'order/cancel/multi',
                        'order/cancel/replace',
                        'order/new',
                        'order/new/multi',
                        'order/status',
                        'orders',
                        'orders/hist',
                        'position/claim',
                        'position/close',
                        'positions',
                        'summary',
                        'taken_funds',
                        'total_taken_funds',
                        'transfer',
                        'unused_taken_funds',
                        'withdraw',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': 0.1 / 100,
                    'taker': 0.2 / 100,
                    'tiers': {
                        'taker': [
                            [0, 0.2 / 100],
                            [500000, 0.2 / 100],
                            [1000000, 0.2 / 100],
                            [2500000, 0.2 / 100],
                            [5000000, 0.2 / 100],
                            [7500000, 0.2 / 100],
                            [10000000, 0.18 / 100],
                            [15000000, 0.16 / 100],
                            [20000000, 0.14 / 100],
                            [25000000, 0.12 / 100],
                            [30000000, 0.1 / 100],
                        ],
                        'maker': [
                            [0, 0.1 / 100],
                            [500000, 0.08 / 100],
                            [1000000, 0.06 / 100],
                            [2500000, 0.04 / 100],
                            [5000000, 0.02 / 100],
                            [7500000, 0],
                            [10000000, 0],
                            [15000000, 0],
                            [20000000, 0],
                            [25000000, 0],
                            [30000000, 0],
                        ],
                    },
                },
                'funding': {
                    'tierBased': False,  # True for tier-based/progressive
                    'percentage': False,  # fixed commission
                    # Actually deposit fees are free for larger deposits(> $1000 USD equivalent)
                    # these values below are deprecated, we should not hardcode fees and limits anymore
                    # to be reimplemented with bitfinex funding fees from their API or web endpoints
                    'deposit': {
                        'BTC': 0.0004,
                        'IOTA': 0.5,
                        'ETH': 0.0027,
                        'BCH': 0.0001,
                        'LTC': 0.001,
                        'EOS': 0.24279,
                        'XMR': 0.04,
                        'SAN': 0.99269,
                        'DASH': 0.01,
                        'ETC': 0.01,
                        'XRP': 0.02,
                        'YYW': 16.915,
                        'NEO': 0,
                        'ZEC': 0.001,
                        'BTG': 0,
                        'OMG': 0.14026,
                        'DATA': 20.773,
                        'QASH': 1.9858,
                        'ETP': 0.01,
                        'QTUM': 0.01,
                        'EDO': 0.95001,
                        'AVT': 1.3045,
                        'USDT': 0,
                        'TRX': 28.184,
                        'ZRX': 1.9947,
                        'RCN': 10.793,
                        'TNB': 31.915,
                        'SNT': 14.976,
                        'RLC': 1.414,
                        'GNT': 5.8952,
                        'SPK': 10.893,
                        'REP': 0.041168,
                        'BAT': 6.1546,
                        'ELF': 1.8753,
                        'FUN': 32.336,
                        'SNG': 18.622,
                        'AID': 8.08,
                        'MNA': 16.617,
                        'NEC': 1.6504,
                    },
                    'withdraw': {
                        'BTC': 0.0004,
                        'IOTA': 0.5,
                        'ETH': 0.0027,
                        'BCH': 0.0001,
                        'LTC': 0.001,
                        'EOS': 0.24279,
                        'XMR': 0.04,
                        'SAN': 0.99269,
                        'DASH': 0.01,
                        'ETC': 0.01,
                        'XRP': 0.02,
                        'YYW': 16.915,
                        'NEO': 0,
                        'ZEC': 0.001,
                        'BTG': 0,
                        'OMG': 0.14026,
                        'DATA': 20.773,
                        'QASH': 1.9858,
                        'ETP': 0.01,
                        'QTUM': 0.01,
                        'EDO': 0.95001,
                        'AVT': 1.3045,
                        'USDT': 20,
                        'TRX': 28.184,
                        'ZRX': 1.9947,
                        'RCN': 10.793,
                        'TNB': 31.915,
                        'SNT': 14.976,
                        'RLC': 1.414,
                        'GNT': 5.8952,
                        'SPK': 10.893,
                        'REP': 0.041168,
                        'BAT': 6.1546,
                        'ELF': 1.8753,
                        'FUN': 32.336,
                        'SNG': 18.622,
                        'AID': 8.08,
                        'MNA': 16.617,
                        'NEC': 1.6504,
                    },
                },
            },
            'commonCurrencies': {
                'BCC': 'CST_BCC',
                'BCU': 'CST_BCU',
                'CTX': 'CTXC',
                'DAT': 'DATA',
                'DSH': 'DASH',  # Bitfinex names Dash as DSH, instead of DASH
                'IOS': 'IOST',
                'IOT': 'IOTA',
                'MNA': 'MANA',
                'QSH': 'QASH',
                'QTM': 'QTUM',
                'SNG': 'SNGLS',
                'SPK': 'SPANK',
                'STJ': 'STORJ',
                'YYW': 'YOYOW',
                'USD': 'USDT',
            },
            'exceptions': {
                'exact': {
                    'temporarily_unavailable': ExchangeNotAvailable,  # Sorry, the service is temporarily unavailable. See https://www.bitfinex.com/ for more info.
                    'Order could not be cancelled.': OrderNotFound,  # non-existent order
                    'No such order found.': OrderNotFound,  # ?
                    'Order price must be positive.': InvalidOrder,  # on price <= 0
                    'Could not find a key matching the given X-BFX-APIKEY.': AuthenticationError,
                    'This API key does not have permission for self action': AuthenticationError,  # authenticated but not authorized
                    'Key price should be a decimal number, e.g. "123.456"': InvalidOrder,  # on isNaN(price)
                    'Key amount should be a decimal number, e.g. "123.456"': InvalidOrder,  # on isNaN(amount)
                    'ERR_RATE_LIMIT': DDoSProtection,
                    'Nonce is too small.': InvalidNonce,
                    'No summary found.': ExchangeError,  # fetchTradingFees(summary) endpoint can give self vague error message
                },
                'broad': {
                    'Invalid order: not enough exchange balance for ': InsufficientFunds,  # when buying cost is greater than the available quote currency
                    'Invalid order: minimum size for ': InvalidOrder,  # when amount below limits.amount.min
                    'Invalid order': InvalidOrder,  # ?
                    'The available balance is only': InsufficientFunds,  # {"status":"error","message":"Cannot withdraw 1.0027 ETH from your exchange wallet. The available balance is only 0.0 ETH. If you have limit orders, open positions, unused or active margin funding, self will decrease your available balance. To increase it, you can cancel limit orders or reduce/close your positions.","withdrawal_id":0,"fees":"0.0027"}
                },
            },
            'precisionMode': SIGNIFICANT_DIGITS,
            'options': {
                'currencyNames': {
                    'AGI': 'agi',
                    'AID': 'aid',
                    'AIO': 'aio',
                    'ANT': 'ant',
                    'AVT': 'aventus',  # #1811
                    'BAT': 'bat',
                    'BCH': 'bcash',  # undocumented
                    'BCI': 'bci',
                    'BFT': 'bft',
                    'BTC': 'bitcoin',
                    'BTG': 'bgold',
                    'CFI': 'cfi',
                    'DAI': 'dai',
                    'DADI': 'dad',
                    'DASH': 'dash',
                    'DATA': 'datacoin',
                    'DTH': 'dth',
                    'EDO': 'eidoo',  # #1811
                    'ELF': 'elf',
                    'EOS': 'eos',
                    'ETC': 'ethereumc',
                    'ETH': 'ethereum',
                    'ETP': 'metaverse',
                    'FUN': 'fun',
                    'GNT': 'golem',
                    'IOST': 'ios',
                    'IOTA': 'iota',
                    'LRC': 'lrc',
                    'LTC': 'litecoin',
                    'LYM': 'lym',
                    'MANA': 'mna',
                    'MIT': 'mit',
                    'MKR': 'mkr',
                    'MTN': 'mtn',
                    'NEO': 'neo',
                    'ODE': 'ode',
                    'OMG': 'omisego',
                    'OMNI': 'mastercoin',
                    'QASH': 'qash',
                    'QTUM': 'qtum',  # #1811
                    'RCN': 'rcn',
                    'RDN': 'rdn',
                    'REP': 'rep',
                    'REQ': 'req',
                    'RLC': 'rlc',
                    'SAN': 'santiment',
                    'SNGLS': 'sng',
                    'SNT': 'status',
                    'SPANK': 'spk',
                    'STORJ': 'stj',
                    'TNB': 'tnb',
                    'TRX': 'trx',
                    'USD': 'wire',
                    'UTK': 'utk',
                    'USDT': 'tetheruso',  # undocumented
                    'VEE': 'vee',
                    'WAX': 'wax',
                    'XLM': 'xlm',
                    'XMR': 'monero',
                    'XRP': 'ripple',
                    'XVG': 'xvg',
                    'YOYOW': 'yoyow',
                    'ZEC': 'zcash',
                    'ZRX': 'zrx',
                },
            },
        })

    async def fetch_funding_fees(self, params={}):
        await self.load_markets()
        response = await self.privatePostAccountFees(params)
        fees = response['withdraw']
        withdraw = {}
        ids = list(fees.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            code = id
            if id in self.currencies_by_id:
                currency = self.currencies_by_id[id]
                code = currency['code']
            withdraw[code] = self.safe_float(fees, id)
        return {
            'info': response,
            'withdraw': withdraw,
            'deposit': withdraw,  # only for deposits of less than $1000
        }

    async def fetch_trading_fees(self, params={}):
        await self.load_markets()
        response = await self.privatePostSummary(params)
        return {
            'info': response,
            'maker': self.safe_float(response, 'maker_fee'),
            'taker': self.safe_float(response, 'taker_fee'),
        }

    async def fetch_markets(self):
        markets = await self.publicGetSymbolsDetails()
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            id = market['pair'].upper()
            baseId = id[0:3]
            quoteId = id[3:6]
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'price': market['price_precision'],
                'amount': market['price_precision'],
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'minimum_order_size'),
                    'max': self.safe_float(market, 'maximum_order_size'),
                },
                'price': {
                    'min': math.pow(10, -precision['price']),
                    'max': math.pow(10, precision['price']),
                },
            }
            limits['cost'] = {
                'min': limits['amount']['min'] * limits['price']['min'],
                'max': None,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, ROUND, self.markets[symbol]['precision']['price'], self.precisionMode)

    def price_to_precision(self, symbol, price):
        return self.decimal_to_precision(price, ROUND, self.markets[symbol]['precision']['price'], self.precisionMode)

    def amount_to_precision(self, symbol, amount):
        return self.decimal_to_precision(amount, TRUNCATE, self.markets[symbol]['precision']['amount'], self.precisionMode)

    def fee_to_precision(self, currency, fee):
        return self.decimal_to_precision(fee, ROUND, self.currencies[currency]['precision'], self.precisionMode)

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        rate = market[takerOrMaker]
        cost = amount * rate
        key = 'quote'
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(self.fee_to_precision(market[key], cost)),
        }

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balanceType = self.safe_string(params, 'type', 'exchange')
        balances = await self.privatePostBalances()
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            if balance['type'] == balanceType:
                currency = balance['currency']
                uppercase = currency.upper()
                uppercase = self.common_currency_code(uppercase)
                account = self.account()
                account['free'] = float(balance['available'])
                account['total'] = float(balance['amount'])
                account['used'] = account['total'] - account['free']
                result[uppercase] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['limit_bids'] = limit
            request['limit_asks'] = limit
        orderbook = await self.publicGetBookSymbol(self.extend(request, params))
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price', 'amount')

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(params)
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            parsedTicker = self.parse_ticker(ticker)
            symbol = parsedTicker['symbol']
            result[symbol] = parsedTicker
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetPubtickerSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_float(ticker, 'timestamp') * 1000
        symbol = None
        if market is not None:
            symbol = market['symbol']
        elif 'pair' in ticker:
            id = ticker['pair']
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
            if market is not None:
                symbol = market['symbol']
            else:
                baseId = id[0:3]
                quoteId = id[3:6]
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
        last = self.safe_float(ticker, 'last_price')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': self.safe_float(ticker, 'mid'),
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = int(float(trade['timestamp'])) * 1000
        side = trade['type'].lower()
        orderId = self.safe_string(trade, 'order_id')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = price * amount
        fee = None
        if 'fee_amount' in trade:
            feeCost = -self.safe_float(trade, 'fee_amount')
            feeCurrency = self.safe_string(trade, 'fee_currency')
            if feeCurrency in self.currencies_by_id:
                feeCurrency = self.currencies_by_id[feeCurrency]['code']
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return {
            'id': str(trade['tid']),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'order': orderId,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=50, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'limit_trades': limit,
        }
        if since is not None:
            request['timestamp'] = int(since / 1000)
        response = await self.publicGetTradesSymbol(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        if limit is not None:
            request['limit_trades'] = limit
        if since is not None:
            request['timestamp'] = int(since / 1000)
        response = await self.privatePostMytrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        orderType = type
        if (type == 'limit') or (type == 'market'):
            orderType = 'exchange ' + type
        amount = self.amount_to_precision(symbol, amount)
        order = {
            'symbol': self.market_id(symbol),
            'amount': amount,
            'side': side,
            'type': orderType,
            'ocoorder': False,
            'buy_price_oco': 0,
            'sell_price_oco': 0,
        }
        if type == 'market':
            order['price'] = str(self.nonce())
        else:
            order['price'] = self.price_to_precision(symbol, price)
        result = await self.privatePostOrderNew(self.extend(order, params))
        return self.parse_order(result)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privatePostOrderCancel({'order_id': int(id)})

    def parse_order(self, order, market=None):
        side = order['side']
        open = order['is_live']
        canceled = order['is_cancelled']
        status = None
        if open:
            status = 'open'
        elif canceled:
            status = 'canceled'
        else:
            status = 'closed'
        symbol = None
        if not market:
            exchange = order['symbol'].upper()
            if exchange in self.markets_by_id:
                market = self.markets_by_id[exchange]
        if market:
            symbol = market['symbol']
        orderType = order['type']
        exchange = orderType.find('exchange ') >= 0
        if exchange:
            parts = order['type'].split(' ')
            orderType = parts[1]
        timestamp = int(float(order['timestamp']) * 1000)
        result = {
            'info': order,
            'id': str(order['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'price': self.safe_float(order, 'price'),
            'average': self.safe_float(order, 'avg_execution_price'),
            'amount': self.safe_float(order, 'original_amount'),
            'remaining': self.safe_float(order, 'remaining_amount'),
            'filled': self.safe_float(order, 'executed_amount'),
            'status': status,
            'fee': None,
        }
        return result

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        if symbol is not None:
            if not(symbol in list(self.markets.keys())):
                raise ExchangeError(self.id + ' has no symbol ' + symbol)
        response = await self.privatePostOrders(params)
        orders = self.parse_orders(response, None, since, limit)
        if symbol:
            orders = self.filter_by(orders, 'symbol', symbol)
        return orders

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        response = await self.privatePostOrdersHist(self.extend(request, params))
        orders = self.parse_orders(response, None, since, limit)
        if symbol is not None:
            orders = self.filter_by(orders, 'symbol', symbol)
        orders = self.filter_by(orders, 'status', 'closed')
        return orders

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privatePostOrderStatus(self.extend({
            'order_id': int(id),
        }, params))
        return self.parse_order(response)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0],
            ohlcv[1],
            ohlcv[3],
            ohlcv[4],
            ohlcv[2],
            ohlcv[5],
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        if limit is None:
            limit = 100
        market = self.market(symbol)
        v2id = 't' + market['id']
        request = {
            'symbol': v2id,
            'timeframe': self.timeframes[timeframe],
            'sort': 1,
            'limit': limit,
        }
        if since is not None:
            request['start'] = since
        response = await self.v2GetCandlesTradeTimeframeSymbolHist(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def get_currency_name(self, currency):
        if currency in self.options['currencyNames']:
            return self.options['currencyNames'][currency]
        raise NotSupported(self.id + ' ' + currency + ' not supported for withdrawal')

    async def create_deposit_address(self, currency, params={}):
        response = await self.fetch_deposit_address(currency, self.extend({
            'renew': 1,
        }, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {
            'currency': currency,
            'address': address,
            'info': response['info'],
        }

    async def fetch_deposit_address(self, currency, params={}):
        name = self.get_currency_name(currency)
        request = {
            'method': name,
            'wallet_name': 'exchange',
            'renew': 0,  # a value of 1 will generate a new address
        }
        response = await self.privatePostDepositNew(self.extend(request, params))
        address = response['address']
        tag = None
        if 'address_pool' in response:
            tag = address
            address = response['address_pool']
        self.check_address(address)
        return {
            'currency': currency,
            'address': address,
            'tag': tag,
            'info': response,
        }

    async def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        name = self.get_currency_name(currency)
        request = {
            'withdraw_type': name,
            'walletselected': 'exchange',
            'amount': str(amount),
            'address': address,
        }
        if tag:
            request['payment_id'] = tag
        responses = await self.privatePostWithdraw(self.extend(request, params))
        response = responses[0]
        id = response['withdrawal_id']
        message = response['message']
        errorMessage = self.find_broadly_matched_key(self.exceptions['broad'], message)
        if id == 0:
            if errorMessage is not None:
                ExceptionClass = self.exceptions['broad'][errorMessage]
                raise ExceptionClass(self.id + ' ' + message)
            raise ExchangeError(self.id + ' withdraw returned an id of zero: ' + self.json(response))
        return {
            'info': response,
            'id': id,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        if api == 'v2':
            request = '/' + api + request
        else:
            request = '/' + self.version + request
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + request
        if (api == 'public') or (path.find('/hist') >= 0):
            if query:
                suffix = '?' + self.urlencode(query)
                url += suffix
                request += suffix
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            query = self.extend({
                'nonce': str(nonce),
                'request': request,
            }, query)
            query = self.json(query)
            query = self.encode(query)
            payload = base64.b64encode(query)
            secret = self.encode(self.secret)
            signature = self.hmac(payload, secret, hashlib.sha384)
            headers = {
                'X-BFX-APIKEY': self.apiKey,
                'X-BFX-PAYLOAD': self.decode(payload),
                'X-BFX-SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def find_broadly_matched_key(self, map, broadString):
        partialKeys = list(map.keys())
        for i in range(0, len(partialKeys)):
            partialKey = partialKeys[i]
            if broadString.find(partialKey) >= 0:
                return partialKey
        return None

    def handle_errors(self, code, reason, url, method, headers, body):
        if len(body) < 2:
            return
        if code >= 400:
            if body[0] == '{':
                response = json.loads(body)
                feedback = self.id + ' ' + self.json(response)
                message = None
                if 'message' in response:
                    message = response['message']
                elif 'error' in response:
                    message = response['error']
                else:
                    raise ExchangeError(feedback)  # malformed(to our knowledge) response
                exact = self.exceptions['exact']
                if message in exact:
                    raise exact[message](feedback)
                broad = self.exceptions['broad']
                broadKey = self.find_broadly_matched_key(broad, message)
                if broadKey is not None:
                    raise broad[broadKey](feedback)
                raise ExchangeError(feedback)  # unknown message
