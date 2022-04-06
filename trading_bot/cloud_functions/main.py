import alpaca_trade_api as tradeapi

import config


def trade_stock(req):
    data = req.get_json()

    if 'passphrase' not in data or data['passphrase'] != config.PASSPHRASE:
        return {
            'code': 'error',
            'message': 'not authenticated'
        }

    api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)

    try:
        order = api.submit_order(
            data['symbol'],
            data['quantity'],
            data['side'],
            data['order_type'],
            data['time_in_force']
        )
    except Exception as e:
        return {
            'code': 'error',
            'message': str(e)
        }

    return {
        'code': 'success',
        'order_id': order.id,
        'order_status': order.status
    }


