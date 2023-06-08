import time, json, os, requests, random, mercadopago, telebot, uuid
from markups import *
import random
from data import *
from gen_payment import *
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
import os
import csv

client = pymongo.MongoClient("localhost", 27017)
db = client.cc
coll_users = db.users
coll_normal = db.normal
coll_full = db.full
coll_mix = db.mix
coll_values = db.values
coll_contas = db.contas
coll_config = db.config
coll_gifts = db.gifts
registerNow = False

giftcard = uuid.uuid4()

with open('config/config.json', 'r') as file:
  config = json.loads(file.read())
  token = config['token']
  user = config['userAdmin']
  idAdmin = config['admin']

bot = telebot.TeleBot(token)



# Notificações

def notify_recharge(id, value, user):
  bot.send_message(idAdmin, f"""
  🎁 Recarga Pix realizada

Id da transação: {id}
Valor: R${value},00
Usuário: @{user}
""", parse_mode="HTML")


def notify_new_user(id, name, username):
  bot.send_message(idAdmin, f"""
  👤 Novo usuário no BOT

ID: {id}
name: R${name},00
Username: @{username}
""", parse_mode="HTML")


def notify_purchase(type, value, username, info):
  bot.send_message(idAdmin, f"""
  💲 Venda realizada com sucesso!

Tipo: {type}
Valor: R${value},00
username: @{username}

Informações da venda:
{info}
""", parse_mode="HTML")
  

# Funções

def gen_id():
  return random.randint(0, 50000)



# Comandos

@bot.message_handler(commands=['start'])
def start(message):
  saldoUser = exists_user(message.from_user)

  if is_admin(message.from_user.id):
      bot.send_message(message.chat.id, f"""
*Seja bem vindo a Supremo Store 💳*
                       
✅ CCS testadas na hora pelo bot!!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!

💬 Dúvidas? @supremodrop

_➤ Informações:_
*├ ID:* `{message.from_user.id}`
*└💰 Saldo:* `R${saldoUser}`
""", reply_markup=inicioAdmin, parse_mode="MARKDOWN")
  else:
      bot.send_message(message.chat.id, f"""
*Seja bem vindo a Supremo Store 💳*
                       
✅ CCS testadas na hora pelo bot!!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!

💬 Dúvidas? @supremodrop

_➤ Informações:_
*├ ID:* `{message.from_user.id}`
*└💰 Saldo:* `R${saldoUser}`
""", reply_markup=inicio, parse_mode="MARKDOWN")
      

@bot.message_handler(func=lambda call: call.data == "menu")
def back(message):
  saldoUser = exists_user(message.from_user)

  if is_admin(message.from_user.id):
      bot.send_message(message.chat.id, f"""
*Seja bem vindo a Supremo Store 💳*
                       
✅ CCS testadas na hora pelo bot!!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!

💬 Dúvidas? @supremodrop

_➤ Informações:_
*├ ID:* `{message.from_user.id}`
*└💰 Saldo:* `R${saldoUser}`
""", reply_markup=inicioAdmin, parse_mode="MARKDOWN")
  else:
      bot.send_message(message.chat.id, f"""
*Seja bem vindo a Supremo Store 💳*
                       
✅ CCS testadas na hora pelo bot!!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!

💬 Dúvidas? @supremodrop

_➤ Informações:_
*├ ID:* `{message.from_user.id}`
*└💰 Saldo:* `R${saldoUser}`
""", reply_markup=inicio, parse_mode="MARKDOWN")


@bot.callback_query_handler(func=lambda call: call.data == "admin")
def admin(call):
  global registerNow

  registerNow = False

  if is_admin(call.message.chat.id) == True:
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
⚙️ <b>PAINEL ADMINISTRATIVO</b>

<b>Comandos do Admin:</b>

""", reply_markup=adminOptions, parse_mode="HTML")
      

@bot.message_handler(commands=['info'])
def info(message):
  if is_admin(message.from_user.id) == True:
    if message.text == "/info":
      bot.send_message(message.chat.id, """
* 👤 Veja as informações de um usuário
         
Modo de uso:* `/info ID`""", parse_mode="MARKDOWN")
    else:
      chat_id = message.text.split("/info ")[1]
      user = data_user(chat_id)

      if (user):
        bot.send_message(message.chat.id, f"""
🔍 <b>USUÁRIO ENCONTRADO</b>

- NOME: {user["name"]}
- USERNAME: {user["username"]}
- ID: {chat_id}
- REGISTRO EM: {user["register"]}

<b>CARTEIRA:</b>
- SALDO: {user["balance"]}

<b>COMPRAS:</b>
- CC's Normais: {len(user["historic_cc"])}
- CC's Full: {len(user["historic_full"])}
- Mix: {len(user["historic_mix"])}

<b>RECARGAS:</b>
- PIX: {user["historic_pix"]}
- MANUAL: {user["historic_manual"]}""", parse_mode="HTML")
      else:
        bot.send_message(message.chat.id, "Usuário não encontrado.")
        
        
@bot.message_handler(commands=['send'])
def send(message):
  if is_admin(message.from_user.id) == True:
    if message.text == "/send":
      bot.send_message(message.chat.id, """
      *📣 Envie uma mensagem para todos os usuários registrados no bot.

Ex:* _/send + a mensagem que deseja enviar_""", parse_mode="MARKDOWN")
    else:
      MSG = message.text.split("/send ")[1]
      bot.send_message(message.chat.id, "Enviando mensagem 📥")
      
      findUsers = coll_users.find({})
      for user in findUsers:
        s=requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user['chat_id']}&text={MSG}&parse_mode=MARKDOWN")


@bot.message_handler(commands=['gift'])
def gift(message):
  if is_admin(message.from_user.id) == True:
    if message.text == "/gift":
      bot.send_message(message.chat.id, """
*💵 Gere um gift card para o usuário resgatar.*

*Ex:* `/gerar` _+ valor que deseja adicionar_""", parse_mode="MARKDOWN")
    else:
      value = int(message.text.split("/gift ")[1])

      gift = ''

      while True:
        for _ in range(4):
          words = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
          gift += words + '_'

        findGift = coll_gifts.find_one({"codigo_gift": gift[:-1]})

        if findGift:
          continue
        else:
          break

      coll_gifts.insert_one({"cod_gift": gift[:-1], "value": value, "used": False})
      bot.send_message(message.chat.id, f"""
✅ GIFT DE R${value} GERADO!

`/resgatar {gift[:-1]}`
""", parse_mode="MARKDOWN")


@bot.message_handler(commands=['resgatar'])
def rescue(message):
  if message.text == "/resgatar":
    bot.send_message(message.chat.id, """
🏷 *De o comando /resgatar + o gift a ser resgatado.*
""", parse_mode="MARKDOWN")
    
  else:
    gift = message.text.split("/resgatar ")[1]

    try:  
      findGift = coll_gifts.find_one({"cod_gift": gift, "used": False})

      if findGift:
        findUser = coll_users.find_one({"chat_id": message.chat.id})

        updateUser = coll_users.find_one_and_update(
          {"chat_id": message.chat.id},
          {"$set": {"balance": int(findUser["balance"]) + int(findGift["value"])}}
        )

        if updateUser:
          used = coll_gifts.find_one_and_update({"cod_gift": gift}, {"$set": {"used": True}})

          findUser = coll_users.find_one({"chat_id": message.chat.id})

          bot.send_message(message.chat.id, f"""
💳 Gift Resgatado com sucesso!

Valor: R${findGift["value"]}
ID: {message.from_user.id}
Usuário: {message.from_user.username}

Saldo atual: R${findUser["balance"]}
""", parse_mode="HTML")
        else:
          bot.send_message(message.chat.id, "*NÃO É POSSÍVEL RESGATAR NO MOMENTO.*", parse_mode="MARKDOWN")
          
      else:
        bot.send_message(message.chat.id,"❗️*GIFT CARD INVÁLIDO OU JÁ RESGATADO.*", parse_mode="MARKDOWN")
    except:
        bot.send_message(message.chat.id,"*NÃO É POSSÍVEL RESGATAR NO MOMENTO.*", parse_mode="MARKDOWN")


@bot.message_handler(commands=['saldo'])
def decrease(message):
  if is_admin(message.from_user.id) == True:
    if message.text == "/saldo":
      bot.send_message(message.chat.id, """
      *Alterar saldo do usuário*

Modo de usar: `/saldo` ID de usuário | Novo valor
""", parse_mode="MARKDOWN")
    else:
      data = message.text.split("/saldo ")[1]
      user = data.split("|")[0]
      value = data.split("|")[1]

      try:
        updateUser = coll_users.find_one_and_update(
          {"chat_id": int(user)},
          {"$set": {"balance": int(value)}}
        )
        
        if updateUser:
          bot.send_message(message.chat.id, "Saldo alterado!")
        else:
          bot.send_message(message.chat.id, "Usuário não existente.")
      except:
        bot.send_message(message.chat.id, "Não foi possível diminui o saldo do usuário.")


@bot.message_handler(commands=['pix'])
def pix(message):
  if message.text == "/pix":
    bot.send_message(message.chat.id, "*Digite /pix + o valor que deseja.*", parse_mode="MARKDOWN")
  else:
    payment = coll_config.find_one({"type": "mercadopago"})

    if len(payment["public"]) > 1:
      value = message.text.split("/pix ")[1]
      pix = gen_payment(int(value), payment['token'])[0]

      headers = {"Authorization": f"Bearer {payment['token']}"}
      request = requests.get(f'https://api.mercadopago.com/v1/payments/{pix}', headers=headers)
      response = request.json()
      qr = response['point_of_interaction']['transaction_data']['qr_code']
      msg = bot.send_message(message.chat.id, f"""
*✅ PAGAMENTO GERADO

ℹ️  ID DO PAGAMENTO:* `{pix}`
*ℹ️  PIX COPIA E COLA:* `{qr}`
*ℹ️  A COMPRA IRÁ EXPIRAR EM 5 MINUTOS.
ℹ️  DEPOIS DO PAGAMENTO SEU SALDO SERÁ ADICIONADO AUTOMÁTICAMENTE.*""", parse_mode="MARKDOWN")
        
      if status(pix, payment['token']) == True:
        findUser = coll_users.find_one({"chat_id": message.chat.id})

        updateUser = coll_users.find_one_and_update({"chat_id": message.chat.id}, {"$set": {"balance": int(findUser["balance"]) + int(value)}})

        if updateUser:
          bot.send_message(message.chat.id, "*✅ PAGAMENTO APROVADO!!! SEU SALDO JÁ ESTÁ DISPONÍVEL.*", parse_mode="MARKDOWN")
          notify_recharge(pix, value, message.from_user.username)

        else:
          bot.send_message(message.chat.id, "*Seu pagamento foi aprovado, mas não foi possível adicionar o saldo. Entre em contato com o suporte.*")
      else:
        bot.send_message(message.chat.id, "*Pagamento expirado.*", parse_mode="MARKDOWN")
    else:
      bot.send_message(message.chat.id, "Nenhuma chave cadastrada pelo administrador.")


@bot.message_handler(commands=['manual'])
def manual(message):
  payment = coll_config.find_one({"type": "manual"})

  if (len(payment["key"]) > 1):
    msg = bot.send_message(message.chat.id, f"""
*✅ REALIZE O SEU PAGAMENTO:

*ℹ️  NOME DA CONTA:* `{payment["name"]}`
*ℹ️  PIX:* `{payment["key"]}`

ℹ️  DEPOIS DO PAGAMENTO, ENVIE O COMPROVANTE PARA @{user}*""", parse_mode="MARKDOWN")
  else:
    bot.send_message(message.chat.id, "Nenhuma chave cadastrada pelo administrador.")



@bot.callback_query_handler(func=lambda call: call.data == "estoque")
def listarEstoque(call):
  if is_admin(call.message.chat.id):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📄 Listar estoque:", reply_markup=estoqueOpts)
  else:
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Não foi possível listar o estoque!")


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_comprar(call):
  saldoUser = exists_user(call.from_user)

  if is_admin(call.from_user.id):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*Seja bem vindo a Supremo Store 💳*
                       
✅ CCS testadas na hora pelo bot!!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!

💬 Dúvidas? @supremodrop

_➤ Informações:_
*├ ID:* `{call.from_user.id}`
*└💰 Saldo:* `R${saldoUser}`
""", reply_markup=inicioAdmin, parse_mode="MARKDOWN")
  else:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*Seja bem vindo a Supremo Store 💳*
                       
✅ CCS testadas na hora pelo bot!!
💰 Faça recargas rapidamente pelo /pix!
💳 CC's virgens diretamente do painel!

💬 Dúvidas? @supremodrop

_➤ Informações:_
*├ ID:* `{call.from_user.id}`
*└💰 Saldo:* `R${saldoUser}`
""", reply_markup=inicio, parse_mode="MARKDOWN")

                
@bot.callback_query_handler(func=lambda call: call.data == "recarregar")
def recharge(call):
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
*💵 Adição de Saldo*
    
Selecione uma opção abaixo:
""", parse_mode="MARKDOWN",reply_markup=i)


@bot.callback_query_handler(func=lambda call: call.data == "perfil")
def profile(call):
  user = data_user(call.message.chat.id)

  if user:
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
📃 <b>Informações</b>

<b>Meu perfil:</b>
✦ NOME: {call.from_user.first_name}
✦ ID: {call.from_user.id}
✦ USUÁRIO: @{call.from_user.username}
✦ RESGISTRADO EM: {user["register"]}

<b>Compras totais:</b>
✦ 💳 CC's Normais: {len(user["historic_cc"])}
✦ 💳 CC's Full: {len(user["historic_full"])}
✦ 🎲 Mix's: {len(user["historic_mix"])}

<b>Carteira:</b>
✦ SALDO: R${user["balance"]}
✦ RECARGAS VIA PIX: {len(user["historic_pix"])}
✦ RECARGAS Manuais: {len(user["historic_manual"])}

<b>Selecione um dos botões abaixo para ver o seu histórico:</b>""", parse_mode="HTML", reply_markup=perfilOpts)
  else:
    bot.send_message(call.from_user.id, "Cadastro não encontrado")


def payment_auto(message):
  if is_admin(message.chat.id):
    try:
      app = message.text.split(":")[0]
      token = message.text.split(":")[1]

      updateConfig = coll_config.find_one_and_update({"type": f"mercadopago"}, {"$set": {"public": app, "token": token}})

      if updateConfig:
        bot.send_message(message.chat.id, "✅ Dados atualizados com sucesso")
      else:
        bot.send_message(message.chat.id, "❌ Não foi possível atualizar os dados")
    except:
      bot.send_message(message.chat.id, "Dados incorretos")


def payment_manual(message):
  if is_admin(message.chat.id):
    try:
      name = message.text.split(":")[0]
      key = message.text.split(":")[1]

      updateConfig = coll_config.find_one_and_update({"type": f"manual"}, {"$set": {"name": name, "key": key}})

      if updateConfig:
        bot.send_message(message.chat.id, "✅ Dados atualizados com sucesso")
      else:
        bot.send_message(message.chat.id, "❌ Não foi possível atualizar os dados")
    except:
      bot.send_message(message.chat.id, "Dados incorretos")
    

@bot.callback_query_handler(func=lambda call: call.data == "pagamentos")
def payments(call):
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Selecione uma opção para configurar o pagamento:", reply_markup=pagamentosOpts)


@bot.callback_query_handler(func=lambda call: call.data == "pag-automatico")
def auto(call):
  msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''Digite os dados no seguinte formato:
  
MERCADO_PUBLIC:MERCADO_TOKEN

Exemplo:
APP_USR-b150cad6-8ecf:APP_USR-65292187238133...

''')

  bot.register_next_step_handler(msg, payment_auto)


@bot.callback_query_handler(func=lambda call: call.data == "pag-manual")
def manual(call):
  msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''Digite os dados no seguinte formato:
  
NOME DA CONTA:CHAVE PIX

''')

  bot.register_next_step_handler(msg, payment_manual)


@bot.callback_query_handler(func=lambda call: call.data == "usuarios")
def users(call):
  users = coll_users.find({})
  count = coll_users.count_documents({})

  name = "usuarios.txt"

  with open(name, 'w', encoding='utf-8') as arq:
    arq.write(f"👤 Total de usuários: {count}\n \n")

    for user in users:
      arq.write(f"{user['chat_id']} - @{user['username']} - {user['nome']} - Saldo: R${user['saldo']} \n \n")

  bot.send_document(chat_id=call.message.chat.id, document=open(name, 'rb'))

  os.remove(name)


@bot.callback_query_handler(func=lambda call: call.data.startswith("historico"))
def historic(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})

  type_call = call.data.split("-")[1]

  if type_call == "pix":
    user = coll_users.find_one({"chat_id": call.message.chat.id})
    updateType = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"type_historic": "pix"}})

    historic = user["historic_pix"]
    historic = historic[::-1]

    if len(historic) >= 1:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💠 Histórico de recargas Pix: Mostrando {int(user["number_pix"]) + 1} de {int(len(historic))}

<b>✦ Data: {historic[int(user["number_pix"])]["data"]}</b>
Valor da recarga: R${historic[int(user["number_pix"])]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      
  elif type_call == "manual":
    user = coll_users.find_one({"chat_id": call.message.chat.id})

    updateType = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"type_historic": "manual"}})
    historic = user["historic_manual"]
    historic = historic[::-1]

    if len(historic) >= 1:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💸 Histórico de recargas manuais: Mostrando {int(user["number_manual"]) + 1} de {int(len(historic))}

<b>✦ Data: {historic[int(user["number_manual"])]["data"]}</b>
Valor da recarga: R${historic[int(user["number_manual"])]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      
  elif type_call == "cc":
    user = coll_users.find_one({"chat_id": call.message.chat.id})

    updateType = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"type_historic": "cc"}})
    historic = user["historic_cc"]
    historic = historic[::-1]

    if len(historic) >= 1:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's: Mostrando {int(user["number_cc"]) + 1} de {int(len(historic))}

<b>✦ Data: {historic[int(user["number_cc"])]["data"]}</b>
Valor da recarga: R${historic[int(user["number_cc"])]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)

  elif type_call == "mix":
    user = coll_users.find_one({"chat_id": call.message.chat.id})

    updateType = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"type_historic": "mix"}})
    historic = user["historic_mix"]
    historic = historic[::-1]

    if len(historic) >= 1:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
🎲 Histórico de Mix: Mostrando {int(user["number_mix"]) + 1} de {int(len(historic))}

<b>✦ Data: {historic[int(user["number_mix"])]["data"]}</b>
Valor da recarga: R${historic[int(user["number_mix"])]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      
  elif type_call == "full":
    user = coll_users.find_one({"chat_id": call.message.chat.id})

    updateType = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"type_historic": "full"}})
    historic = user["historic_full"]
    historic = historic[::-1]

    if len(historic) >= 1:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's: Mostrando {int(user["number_full"]) + 1} de {int(len(historic))}

<b>✦ Data: {historic[int(user["number_full"])]["data"]}</b>
Valor da recarga: R${historic[int(user["number_full"])]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)


@bot.callback_query_handler(func=lambda call: call.data.startswith("voltar"))
def back(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})

  if user["type_historic"] == "pix":
    if int(user["number_pix"]) >= 1:
      if len(user["historic_pix"]) >= 1:
        if not int(user["number_pix"]) < 1:
          update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_pix": int(user["number_pix"]) - 1}})

          user = coll_users.find_one({"chat_id": call.message.chat.id})
        
          if user["historic_pix"] == 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💠 Histórico de recargas Pix: Mostrando {int(user["number_pix"]) + 1} de {int(len(user["historic_pix"]))}

<b>✦ Data: {user["historic_pix"][user["number_pix"]]["data"]}</b>
Valor da recarga: R${user["historic_pix"][user["number_pix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

    """, parse_mode="HTML", reply_markup=voltarAvancar)
          else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💠 Histórico de recargas Pix: Mostrando {int(user["number_pix"]) + 1} de {int(len(user["historic_pix"]))}

<b>✦ Data: {user["historic_pix"][user["number_pix"]]["data"]}</b>
Valor da recarga: R${user["historic_pix"][user["number_pix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

  """, parse_mode="HTML", reply_markup=voltarAvancar)
            
  elif user["type_historic"] == "manual":
    if int(user["number_manual"]) >= 1:
      if len(user["historic_manual"]) >= 1:
        if not int(user["number_manual"]) < 1:
          update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_manual": int(user["number_manual"]) - 1}})

          user = coll_users.find_one({"chat_id": call.message.chat.id})
        
          if user["historic_manual"] == 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💸 Histórico de recargas manuais: Mostrando {int(user["number_manual"]) + 1} de {int(len(user["historic_manual"]))}

<b>✦ Data: {user["historic_manual"][user["number_manual"]]["data"]}</b>
Valor da recarga: R${user["historic_manual"][user["number_manual"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

    """, parse_mode="HTML", reply_markup=voltarAvancar)
          else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💸 Histórico de recargas manuais: Mostrando {int(user["number_manual"]) + 1} de {int(len(user["historic_manual"]))}

<b>✦ Data: {user["historic_manual"][user["number_manual"]]["data"]}</b>
Valor da recarga: R${user["historic_manual"][user["number_manual"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

  """, parse_mode="HTML", reply_markup=voltarAvancar)
            
  elif user["type_historic"] == "cc":
    if int(user["number_cc"]) >= 1:
      if len(user["historic_cc"]) >= 1:
        if not int(user["number_cc"]) < 1:
          update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_cc": int(user["number_cc"]) - 1}})

          user = coll_users.find_one({"chat_id": call.message.chat.id})
        
          if user["historic_cc"] == 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's: Mostrando {int(user["number_cc"]) + 1} de {int(len(user["historic_cc"]))}

<b>✦ Data: {user["historic_cc"][user["number_cc"]]["data"]}</b>
Valor da recarga: R${user["historic_cc"][user["number_cc"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

    """, parse_mode="HTML", reply_markup=voltarAvancar)
          else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's: Mostrando {int(user["number_cc"]) + 1} de {int(len(user["historic_cc"]))}

<b>✦ Data: {user["historic_cc"][user["number_cc"]]["data"]}</b>
Valor da recarga: R${user["historic_cc"][user["number_cc"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

  """, parse_mode="HTML", reply_markup=voltarAvancar)
            
  elif user["type_historic"] == "mix":
    if int(user["number_mix"]) >= 1:
      if len(user["historic_mix"]) >= 1:
        if not int(user["number_mix"]) < 1:
          update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_mix": int(user["number_mix"]) - 1}})

          user = coll_users.find_one({"chat_id": call.message.chat.id})
        
          if user["historic_mix"] == 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
🎲 Histórico de Mix: Mostrando {int(user["number_mix"]) + 1} de {int(len(user["historic_mix"]))}

<b>✦ Data: {user["historic_mix"][user["number_mix"]]["data"]}</b>
Valor da recarga: R${user["historic_mix"][user["number_mix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

    """, parse_mode="HTML", reply_markup=voltarAvancar)
          else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
🎲 Histórico de Mix: Mostrando {int(user["number_mix"]) + 1} de {int(len(user["historic_mix"]))}

<b>✦ Data: {user["historic_mix"][user["number_mix"]]["data"]}</b>
Valor da recarga: R${user["historic_mix"][user["number_mix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

  """, parse_mode="HTML", reply_markup=voltarAvancar)

  elif user["type_historic"] == "full":
    if int(user["number_full"]) >= 1:
      if len(user["historic_full"]) >= 1:
        if not int(user["number_full"]) < 1:
          update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_full": int(user["number_full"]) - 1}})

          user = coll_users.find_one({"chat_id": call.message.chat.id})
        
          if user["historic_full"] == 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's Full: Mostrando {int(user["number_full"]) + 1} de {int(len(user["historic_full"]))}

<b>✦ Data: {user["historic_full"][user["number_full"]]["data"]}</b>
Valor da recarga: R${user["historic_full"][user["number_full"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

    """, parse_mode="HTML", reply_markup=voltarAvancar)
          else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's Full: Mostrando {int(user["number_full"]) + 1} de {int(len(user["historic_full"]))}

<b>✦ Data: {user["historic_full"][user["number_full"]]["data"]}</b>
Valor da recarga: R${user["historic_full"][user["number_full"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

  """, parse_mode="HTML", reply_markup=voltarAvancar)


@bot.callback_query_handler(func=lambda call: call.data.startswith("avancar"))
def advance(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})

  if user["type_historic"] == "pix":
    if int(user["number_pix"]) + 1 < len(user["historic_pix"]):
      update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_pix": int(user["number_pix"]) + 1}})
      user = coll_users.find_one({"chat_id": call.message.chat.id})

      historic = user["historic_pix"]
      historic = historic[::-1]
    
      if user["historic_pix"] == 1:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💠 Histórico de recargas Pix: Mostrando {int(user["number_pix"]) + 2} de {int(len(user["historic_pix"]))}

<b>✦ Data: {historic[user["number_pix"]]["data"]}</b>
Valor da recarga: R${historic[user["number_pix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💠 Histórico de recargas Pix: Mostrando {int(user["number_pix"]) + 1} de {int(len(user["historic_pix"]))}

<b>✦ Data: {historic[user["number_pix"]]["data"]}</b>
Valor da recarga: R${historic[user["number_pix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)

  elif user["type_historic"] == "manual":
    if int(user["number_manual"]) + 1 < len(user["historic_manual"]):
      update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_manual": int(user["number_manual"]) + 1}})
      user = coll_users.find_one({"chat_id": call.message.chat.id})

      historic = user["historic_manual"]
      historic = historic[::-1]
    
      if user["historic_manual"] == 1:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💸 Histórico de recargas manuais: Mostrando {int(user["number_manual"]) + 2} de {int(len(user["historic_manual"]))}

<b>✦ Data: {historic[user["number_manual"]]["data"]}</b>
Valor da recarga: R${historic[user["number_manual"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💸 Histórico de recargas manuais: Mostrando {int(user["number_manual"]) + 1} de {int(len(user["historic_manual"]))}

<b>✦ Data: {historic[user["number_manual"]]["data"]}</b>
Valor da recarga: R${historic[user["number_manual"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)

  elif user["type_historic"] == "cc":
    if int(user["number_cc"]) + 1 < len(user["historic_cc"]):
      update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_cc": int(user["number_cc"]) - 1}})
      user = coll_users.find_one({"chat_id": call.message.chat.id})

      historic = user["historic_cc"]
      historic = historic[::-1]
    
      if user["historic_cc"] == 1:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's: Mostrando {int(user["number_cc"]) + 2} de {int(len(user["historic_cc"]))}

<b>✦ Data: {historic[user["number_cc"]]["data"]}</b>
Valor da recarga: R${historic[user["number_cc"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's: Mostrando {int(user["number_cc"]) + 1} de {int(len(user["historic_cc"]))}

<b>✦ Data: {historic[user["number_cc"]]["data"]}</b>
Valor da recarga: R${historic[user["number_cc"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)

  elif user["type_historic"] == "mix":
    if int(user["number_mix"]) + 1 < len(user["historic_mix"]):
      update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_mix": int(user["number_mix"]) - 1}})
      user = coll_users.find_one({"chat_id": call.message.chat.id})

      historic = user["historic_mix"]
      historic = historic[::-1]
    
      if user["historic_mix"] == 1:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
🎲 Histórico de Mix: Mostrando {int(user["number_mix"]) + 2} de {int(len(user["historic_mix"]))}

<b>✦ Data: {historic[user["number_mix"]]["data"]}</b>
Valor da recarga: R${historic[user["number_mix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
🎲 Histórico de Mix: Mostrando {int(user["number_mix"]) + 1} de {int(len(user["historic_mix"]))}

<b>✦ Data: {historic[user["number_mix"]]["data"]}</b>
Valor da recarga: R${historic[user["number_mix"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)

  elif user["type_historic"] == "full":
    if int(user["number_full"]) + 1 < len(user["historic_full"]):
      update = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_full": int(user["number_full"]) - 1}})
      user = coll_users.find_one({"chat_id": call.message.chat.id})

      historic = user["historic_full"]
      historic = historic[::-1]
    
      if user["historic_full"] == 1:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's Full: Mostrando {int(user["number_full"]) + 2} de {int(len(user["historic_full"]))}

<b>✦ Data: {historic[user["number_full"]]["data"]}</b>
Valor da recarga: R${historic[user["number_full"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)
      else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 Histórico de CC's Full: Mostrando {int(user["number_full"]) + 1} de {int(len(user["historic_full"]))}

<b>✦ Data: {historic[user["number_full"]]["data"]}</b>
Valor da recarga: R${historic[user["number_full"]]["value"]}

<b>Você pode baixar o histórico completo também:</b>

""", parse_mode="HTML", reply_markup=voltarAvancar)


@bot.callback_query_handler(func=lambda call: call.data == "del-manual")
def delete_manual(call):
  delete_manual = coll_config.find_one_and_update({"type": f"manual"}, {"$set": {"name": "", "key": ""}})

  if (delete_manual):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Informações deletadas do pagamento manual.')
  else:
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='❌ Informações deletadas do pagamento manual.')


@bot.callback_query_handler(func=lambda call: call.data == "del-auto")
def delete_auto(call):
  delete_auto = coll_config.find_one_and_update({"type": f"mercadopago"}, {"$set": {"public": "", "token": ""}})

  if (delete_auto):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅ Informações deletadas do pagamento automático.')
  else:
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='❌ Informações deletadas do pagamento automático.')


def add_normal(message):
  global registerNow

  try:
    repeats = []

    file_id = message.document.file_id
    path = file_id + ".txt"
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    bot.send_message(message.chat.id, "Adicionando todas as contas. Aguarde.")

    with open(path, 'wb') as new_file:
      new_file.write(downloaded_file)

    with open(path, 'r') as arq:
      content = arq.readlines()

    with open('./data/persons.json') as arq:
      data = json.load(arq)

    for cc in content:
      person = random.choice(data)

      cc = cc.replace("\n", "").split("|") if "|" in cc else cc.replace("\n", "").split("/")

      if len(cc) > 2:
        number = cc[0]

        if number in repeats:
          continue

        bin_cc_value = cc[0][0:6]
        month = cc[1]
        year = cc[2]
        cvc = cc[3]
        level = cc[4]
        bank = cc[5]
        flag = cc[6]
        type_cc = cc[7]
        country = cc[8]
        date = datetime.today().strftime("%d/%m/%Y")

        exist = coll_values.find_one({"level": level.lower().strip()})

        if not exist:
          coll_values.insert_one({"level": level.lower().strip(), "value": 20})

        coll_normal.insert_one({"number": number, "bin": bin_cc_value, "month": month, "year": year, "cvc": cvc, "level": level, "bank": bank, "flag": flag, "type": type_cc, "country": country, "date": date, "name": person["nome"], "cpf": person["cpf"]})
        repeats.append(number)
      else:
        continue
      
    registerNow = False
    bot.send_message(message.chat.id, f"✅ {len(repeats)} Cartões normais adicionados com sucesso!")
  except:
    registerNow = False
    bot.send_message(message.chat.id, "Não foi possível adicionar", reply_markup=adminOptions)


def add_full(message):
  global registerNow

  try:
    repeats = []

    file_id = message.document.file_id
    path = file_id + ".txt"
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    bot.send_message(message.chat.id, "Adicionando todas as contas. Aguarde.")

    with open(path, 'wb') as new_file:
      new_file.write(downloaded_file)

    with open(path, 'r') as arq:
      content = arq.readlines()

    with open('./data/persons.json') as arq:
      data = json.load(arq)

    for cc in content:
      person = random.choice(data)

      cc = cc.replace("\n", "").split("|") if "|" in cc else cc.replace("\n", "").split("/")

      if (len(cc)) > 2:
        number = cc[0]

        if number in repeats:
          continue

        bin_cc_value = cc[0][0:6]
        month = cc[1]
        year = cc[2]
        cvc = cc[3]
        level = cc[4]
        bank = cc[5]
        flag = cc[6]
        type_cc = cc[7]
        country = cc[8]
        date = datetime.today().strftime("%d/%m/%Y")

        exist = coll_values.find_one({"level": level.lower().strip()})

        if not exist:
          coll_values.insert_one({"level": level.lower().strip(), "value": 20})

        coll_full.insert_one({"number": number, "bin": bin_cc_value, "month": month, "year": year, "cvc": cvc, "level": level, "bank": bank, "flag": flag, "type": type_cc, "country": country, "date": date, "name": person["nome"], "cpf": person["cpf"]})
        repeats.append(number)
      else:
        continue
      
    registerNow = False
    bot.send_message(message.chat.id, f"✅ {len(repeats)} Cartões full adicionados com sucesso!")
  except:
    registerNow = False
    bot.send_message(message.chat.id, "Não foi possível adicionar", reply_markup=adminOptions)


def add_mix(message):
  global registerNow

  try:
    repeats = []

    file_id = message.document.file_id
    path = file_id + ".txt"
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    bot.send_message(message.chat.id, "Adicionando todas as contas. Aguarde.")

    with open(path, 'wb') as new_file:
      new_file.write(downloaded_file)

    with open(path, 'r') as arq:
      content = arq.readlines()

    with open('./data/persons.json') as arq:
      data = json.load(arq)

    for cc in content:
      person = random.choice(data)

      cc = cc.replace("\n", "").split("|") if "|" in cc else cc.replace("\n", "").split("/")

      if len(cc) > 2:
        number = cc[0]

        if number in repeats:
          continue

        bin_cc_value = cc[0][0:6]
        month = cc[1]
        year = cc[2]
        cvc = cc[3]
        level = cc[4]
        bank = cc[5]
        flag = cc[6]
        type_cc = cc[7]
        country = cc[8]
        date = datetime.today().strftime("%d/%m/%Y")

        exist = coll_values.find_one({"level": level.lower().strip()})

        if not exist:
          coll_values.insert_one({"level": level.lower().strip(), "value": 20})

        coll_mix.insert_one({"number": number, "bin": bin_cc_value, "month": month, "year": year, "cvc": cvc, "level": level, "bank": bank, "flag": flag, "type": type_cc, "country": country, "date": date, "name": person["nome"], "cpf": person["cpf"]})
        repeats.append(number)
      else:
        continue

    registerNow = False
    bot.send_message(message.chat.id, f"✅ {len(repeats)} Cartões Mix adicionados com sucesso!")
  except:
    registerNow = False
    bot.send_message(message.chat.id, "Não foi possível adicionar", reply_markup=adminOptions)


@bot.callback_query_handler(func=lambda call: call.data == "add-normal")
def normal(call):
  global registerNow

  if registerNow == False:
    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''💳 *Para adicionar CC's Normais, envie um TXT no formato:*

*O bot realizará as separações por nível, e NÃO vai adicionar repetidas!*

(Não esqueça dos separadores: "|" ou "/")

numero|data|cvv|nível|banco|bandeira|tipo|pais

Exemplo:
5448910352962343|07|2028|565|BLACK|ITAU UNIBANCO S.A.|MASTERCARD|CREDIT|BRAZIL

*Aguardando TXT..*

''', parse_mode="MARKDOWN", reply_markup=back_admin)
    
  bot.register_next_step_handler(msg, add_normal)


@bot.callback_query_handler(func=lambda call: call.data == "add-full")
def full(call):
  global registerNow

  if registerNow == False:
    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''💳 *Para adicionar CC's Full, envie um TXT no formato:*

*O bot realizará as separações por nível, e NÃO vai adicionar repetidas!*

(Não esqueça dos separadores: "|" ou "/")

numero|data|cvv|nível|banco|bandeira|tipo|pais

Exemplo:
5448910352962343|07|2028|565|BLACK|ITAU UNIBANCO S.A.|MASTERCARD|CREDIT|BRAZIL|NOME|CPF

*Aguardando TXT..*

''', parse_mode="MARKDOWN", reply_markup=back_admin)
    
  bot.register_next_step_handler(msg, add_full)


@bot.callback_query_handler(func=lambda call: call.data == "add-mix")
def mix(call):
  global registerNow

  if registerNow == False:
    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''🎲 *Para adicionar CC's Mix, envie um TXT no formato:*

*O bot realizará as separações por nível, e NÃO vai adicionar repetidas!*

(Não esqueça dos separadores: "|" ou "/")

numero|data|cvv|nível|banco|bandeira|tipo|pais

Exemplo:
5448910352962343|07|2028|565|BLACK|ITAU UNIBANCO S.A.|MASTERCARD|CREDIT|BRAZIL

*Aguardando TXT..*

''', parse_mode="MARKDOWN", reply_markup=back_admin)
    
  bot.register_next_step_handler(msg, add_mix)


@bot.callback_query_handler(func=lambda call: call.data == "cc_normal")
def buy_cc(call):
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Buscando CC's")

  select = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"select_cc": "normal"}})

  normal = coll_normal.find({})

  markup = InlineKeyboardMarkup()
  markup.row_width = 1

  try:
    repeats = []
    levels = []
    buttons = []
    number = 0

    for cc in normal:
      replace_cc = cc["level"]

      replace_cc = replace_cc.lower().strip()

      number += 1

      if replace_cc in repeats:
        continue
      else:
        find = coll_values.find_one({"level": replace_cc})
        
        repeats.append(replace_cc)
        levels.append(f'{replace_cc} - R${find["value"]}')
        
    if len(levels) == 0:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Nenhuma CC disponível.", reply_markup=back)
    else:
      text = "*Escolha um nível para continuar sua compra:\n\n*"

      for cc_markup in levels:
        button = InlineKeyboardButton(f'{cc_markup.upper()}', callback_data=f'buy-{cc_markup.strip()}')
        text += f"{cc_markup.upper()}\n"
        markup.add(button)

      text += f"\n{number} cartões disponíveis"
      
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode="MARKDOWN", reply_markup=markup)
  except:
    bot.send_message(call.message.chat.id, "Não foi possível listar os cartões.", reply_markup=back)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buy"))
def buy_cc(call):
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Buscando informação")

  try:
    level = call.data.split("-")[1]

    select = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"select_level": level.upper()}})

    if select["select_cc"] == "normal":
      cards = coll_normal.find({"level": level.upper().strip()})

      markup = InlineKeyboardMarkup()
      markup.row_width = 1

      flags = []
      buttons = []

      for cc in cards:
        replace_flag = cc["flag"]

        replace_flag = replace_flag.lower().strip()

        if replace_flag in flags:
          continue
        else:
          flags.append(replace_flag)
          buttons.append(f'{replace_flag}')
      
      text = "*Escolha a bandeira para continuar sua compra:\n\n*"

      for flag in flags:
        button = InlineKeyboardButton(f'{flag.upper()}', callback_data=f'flag-{flag}')
        markup.add(button)
      
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode="MARKDOWN", reply_markup=markup)
  except:
    bot.send_message(call.message.chat.id, "Não foi possível listar as opções do cartão.", reply_markup=back)


@bot.callback_query_handler(func=lambda call: call.data.startswith("flag"))
def buy(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})

  flag = call.data.split("-")[1]

  if user["select_cc"] == "normal":
    cards = list(coll_normal.find({"flag": flag.upper().strip(), "level": user["select_level"].strip()}))

    value = coll_values.find_one({"level": user["select_level"].lower().strip()})

    if len(cards) > 0:
      select = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"select_flag": flag.strip(), "quantity": len(cards), "cc_confirm": cards[0]["number"]}})

      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
Mostrando {int(user["number_card"]) + 1} de {len(cards)} cartões disponíveis:

💳 Cartão: {cards[0]["number"][:-10] + "******"}
📆 Mês / Ano: {cards[0]["month"]}/{cards[0]["year"]}
🔐 CVV: ***

🏳️ Bandeira: {flag.upper().strip()}
💠 Nível: {cards[0]["level"]}
⚜ Tipo: {cards[0]["type"]}
🏛 Banco: {cards[0]["bank"]}
🌍 Pais: {cards[0]["country"]}

💵 Preço: R${value["value"]}
💰 Seu saldo: R${user["balance"]}

  """, parse_mode="HTML", reply_markup=voltarAvancarCc)
    else:
      bot.send_message(call.message.chat.id, "Não há CC's.")
      

@bot.callback_query_handler(func=lambda call: call.data.startswith("return-cc"))
def return_cc(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})

  if user["select_cc"] == "normal":
    if not user["number_card"] < 0:
      if not user["number_card"] == 0:
        cards = list(coll_normal.find({"flag": user["select_flag"].upper().strip(), "level": user["select_level"].strip()}))
        number = user["number_card"] + 1

        if len(cards) > 0:
          select = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_card": int(user["number_card"]) - 1, "cc_confirm": cards[number]["number"]}})

          user = coll_users.find_one({"chat_id": call.message.chat.id})

          value = coll_values.find_one({"level": user["select_level"].lower().strip()})

          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
Mostrando {int(user["number_card"]) + 1} de {len(cards)} cartões disponíveis:

💳 Cartão: {cards[user["number_card"]]["number"][:-10] + "******"}
📆 Mês / Ano: {cards[user["number_card"]]["month"]}/{cards[user["number_card"]]["year"]}
🔐 CVV: ***

🏳️ Bandeira: {user["select_flag"].upper().strip()}
💠 Nível: {cards[user["number_card"]]["level"]}
⚜ Tipo: {cards[user["number_card"]]["type"]}
🏛 Banco: {cards[user["number_card"]]["bank"]}
🌍 Pais: {cards[user["number_card"]]["country"]}

💵 Preço: R${value["value"]}
💰 Seu saldo: R${user["balance"]}

    """, parse_mode="HTML", reply_markup=voltarAvancarCc)
        else:
          bot.send_message(call.message.chat.id, "Não há CC's.")
      

@bot.callback_query_handler(func=lambda call: call.data.startswith("advance-cc"))
def advance_cc(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})

  if user["select_cc"] == "normal":
    if not user["number_card"] == user["quantity"]:
      cards = list(coll_normal.find({"flag": user["select_flag"].upper().strip(), "level": user["select_level"].strip()}))
      number = user["number_card"] + 1

      if len(cards) > 0:
        select = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"number_card": int(user["number_card"]) + 1, "cc_confirm": cards[number]["number"]}})

        user = coll_users.find_one({"chat_id": call.message.chat.id})

        value = coll_values.find_one({"level": user["select_level"].lower().strip()})

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
Mostrando {int(user["number_card"]) + 1} de {len(cards)} cartões disponíveis:

💳 Cartão: {cards[user["number_card"]]["number"][:-10] + "******"}
📆 Mês / Ano: {cards[user["number_card"]]["month"]}/{cards[user["number_card"]]["year"]}
🔐 CVV: ***

🏳️ Bandeira: {user["select_flag"].upper().strip()}
💠 Nível: {cards[user["number_card"]]["level"]}
⚜ Tipo: {cards[user["number_card"]]["type"]}
🏛 Banco: {cards[user["number_card"]]["bank"]}
🌍 Pais: {cards[user["number_card"]]["country"]}

💵 Preço: R${value["value"]}
💰 Seu saldo: R${user["balance"]}

    """, parse_mode="HTML", reply_markup=voltarAvancarCc)
      else:
          bot.send_message(call.message.chat.id, "Não há CC's.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm-buy"))
def confirm(call):
  user = coll_users.find_one({"chat_id": call.message.chat.id})
  
  if user["select_cc"] == "normal":
    cc = coll_normal.find_one({"number": user["cc_confirm"], "level": user["select_level"].strip(), "flag": user["select_flag"].upper()})
    value = coll_values.find_one({"level": user["select_level"].lower().strip()})

    if cc:
      if int(user["balance"]) >= int(value["value"]):
        user = coll_users.find_one({"chat_id": call.message.chat.id})

        delete = coll_normal.find_one_and_delete({"number": user["cc_confirm"], "level": user["select_level"].strip(), "flag": user["select_flag"].upper()})

        if delete:
          notify_purchase("CC normal", value["value"], user["username"], cc["number"])

          balance = coll_users.find_one_and_update({"chat_id": call.message.chat.id}, {"$set": {"balance": int(user["balance"]) - int(value["value"])}})

          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""✅ <b>Compra realizada com sucesso!</b>

💳 Cartão: {cc["number"]}
📆 Mês / Ano: {cc["month"]}/{cc["year"]}
🔐 CVV: {cc["cvc"]}

Dados auxiliares:
👤 Nome: {cc["name"]}
🪪 CPF: {cc["cpf"]}

🏳️ Bandeira: {user["select_flag"].upper().strip()}
💠 Nível: {cc["level"]}
⚜ Tipo: {cc["type"]}
🏛 Banco: {cc["bank"]}
🌍 Pais: {cc["country"]}

💰 Saldo: R${user["balance"]}""", parse_mode="HTML")
  else:
    bot.send_message(call.message.chat.id, "Não disponível.")



bot.infinity_polling()