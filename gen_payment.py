import mercadopago, pytz, datetime, json, requests, time

def expiration():
    with open('config/config.json', 'r') as file:
        config = json.loads(file.read())
        expiration_payment = config['expiration_payment_in_minutes']
    
    time_change = datetime.timedelta(minutes=int(expiration_payment))
    new_time = datetime.datetime.now() + time_change

    tz = pytz.timezone("America/Bahia")
    aware_dt = tz.localize(new_time)

    a = aware_dt.isoformat()
    
    return a[:23]+a[26:]


def gen_payment(value, token):
    sdk = mercadopago.SDK(token)
    payment_data = {
        "transaction_amount": float(str(value)+'.00'),
        "description": "BOT TELEGRAM",
        "payment_method_id": "pix",
        "payer": {
            "email": 'xateja1315@rockdian.com',
            "first_name": 'Compra',
            "last_name": 'Compra',
            "identification": {
                "type": "CPF",
                "number": ''
            },
            "address": {
                "zip_code": '',
                "street_name": '',
                "street_number": '',
                "neighborhood": '',
                "city": '',
                "federal_unit": ''
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)

    payment = payment_response["response"]

    id_pix = str(payment["id"])

    return id_pix

def status(id_a, token):
  try:
    with open('config/config.json', 'r') as file:
        config = json.loads(file.read())

    expiration_payment = config['expiration_payment_in_minutes']
    headers = {"Authorization": f"Bearer {token}"}
    contador = 0
    while True:
        contador += 1
        
        request = requests.get(f'https://api.mercadopago.com/v1/payments/{id_a}', headers=headers).json()
        status = str(request['status']).strip()
        
        if not contador > int(expiration_payment):
            if status == 'pending':
                pass
                
            elif status == 'approved':
                r = 1
                break
            
            time.sleep(5)
            
        else:
            r = 0
            break

    if r == 1:
        return True
    
    else:
        return False
  except:
        return 'Erro'