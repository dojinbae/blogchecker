import requests
import base64

# 인증결과로 받은 paymentKey 를 사용하여 승인을 요청한다
def getPayment(paymentKey, orderId, amount, base64ApiKey):
    headers = {
        'Authorization': 'Basic '+base64ApiKey
    }
    json_data = {
        'paymentKey': paymentKey,
        'orderId': orderId,
        'amount': amount,
    }
    response = requests.post('https://api.tosspayments.com/v1/payments/confirm', headers=headers, json=json_data)
    print("승인결과")
    print(response.text)
    return response

# paymentKey 를 받아서 승인을 취소한다.
def getCancel(paymentKey, base64ApiKey):
    headers = {
        'Authorization': 'Basic '+base64ApiKey
    }
    json_data = {
#        'paymentKey': paymentKey,
        'cancelReason': '고객이 취소를 원함',
    }
    cancelReqUrl = 'https://api.tosspayments.com/v1/payments/'+paymentKey+'/cancel'
    response = requests.post(cancelReqUrl, headers=headers, json=json_data)
    print(cancelReqUrl)
    print("취소결과")
    print(response.text)
    return response


# apiKey 를 받아서 base64 형태로 변환한다
def getBase64Str(apiKey):
    apiKey_bytes = apiKey.encode('ascii')
    apiKey_base64 = base64.b64encode(apiKey_bytes)
    apiKey_base64_str = apiKey_base64.decode('ascii')
    return apiKey_base64_str
