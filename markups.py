from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import *
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
aguardando = InlineKeyboardMarkup()
aguardando.row_width = 2
aguardando.add(InlineKeyboardButton("🔁 AGUARDANDO PAGAMENTO", callback_data="."))

inicio = InlineKeyboardMarkup()
inicio.row_width = 2
inicio.add(
  InlineKeyboardButton('💳 Comprar CCs', callback_data='cc_normal'),
  InlineKeyboardButton('👤 Meu perfil', callback_data='perfil'),
  InlineKeyboardButton('💵 Recarregar', callback_data='recarregar'),
  InlineKeyboardButton('⚙️ Suporte', url='https://t.me/supremodrop'))

inicioAdmin = InlineKeyboardMarkup()
inicioAdmin.row_width = 2
inicioAdmin.add(
  InlineKeyboardButton('💳 Comprar CCs', callback_data='cc_normal'),
  InlineKeyboardButton('👤 Meu perfil', callback_data='perfil'),
  InlineKeyboardButton('💵 Recarregar', callback_data='recarregar'),
  InlineKeyboardButton('⚙️ Suporte', url='https://t.me/supremodrop'))
inicioAdmin.row_width = 1
inicioAdmin.add(InlineKeyboardButton('⭐ Admin', callback_data='admin'))


perfilOpts = InlineKeyboardMarkup()
perfilOpts.row_width = 2
perfilOpts.add(
  InlineKeyboardButton('💠 Recargas via Pix', callback_data='historico-pix'),
  InlineKeyboardButton('💸 Recargas Manuais', callback_data='historico-manual'),
  InlineKeyboardButton("💳 Histórico de CC's", callback_data='historico-cc'),
  InlineKeyboardButton("💳 Hist. CC's Full", callback_data='historico-full'),
  InlineKeyboardButton("🎲 Histórico de Mix's", callback_data='historico-mix'),
  InlineKeyboardButton('🛠️ Dev', callback_data='sobre'),
  InlineKeyboardButton('🔙 Voltar', callback_data='back'))


voltarAvancar = InlineKeyboardMarkup()
voltarAvancar.row_width = 2
voltarAvancar.add(
  InlineKeyboardButton('◀ Voltar', callback_data='voltar'),
  InlineKeyboardButton('Avançar ▶', callback_data='avancar'),
  InlineKeyboardButton('🔙 Menu', callback_data='perfil'))


voltarAvancarCc = InlineKeyboardMarkup()
voltarAvancarCc.row_width = 1
voltarAvancarCc.add(
  InlineKeyboardButton('💵 Comprar', callback_data='confirm-buy'))

voltarAvancarCc.row_width = 2
voltarAvancarCc.add(
  InlineKeyboardButton('◀ Voltar', callback_data='return-cc'),
  InlineKeyboardButton('Avançar ▶', callback_data='advance-cc'))

voltarAvancarCc.row_width = 1
voltarAvancarCc.add(
  InlineKeyboardButton('🔙 Menu', callback_data='perfil'))


baixarHistorico = InlineKeyboardMarkup()
baixarHistorico.row_width = 2
baixarHistorico.add(
  InlineKeyboardButton('⬇ Baixar histórico', callback_data='baixar'),
  InlineKeyboardButton('🔙 Voltar', callback_data='back'))


compraOpts = InlineKeyboardMarkup()
compraOpts.row_width = 2
compraOpts.add(
  InlineKeyboardButton(f'Comprar conta', callback_data='comprar-conta'),
  InlineKeyboardButton(f'Comprar tela', callback_data='comprar-tela'),
  InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
)


compraOpts2 = InlineKeyboardMarkup()
compraOpts2.row_width = 2
compraOpts2.add(
  InlineKeyboardButton(f'Comprar conta', callback_data='comprar-conta'),
  InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
)


compraOpts3 = InlineKeyboardMarkup()
compraOpts3.row_width = 2
compraOpts3.add(
  InlineKeyboardButton(f'Comprar tela', callback_data='comprar-tela'),
  InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
)


confirmarCompra = InlineKeyboardMarkup()
confirmarCompra.row_width = 1
confirmarCompra.add(
  InlineKeyboardButton(f'💠 Confirmar compra', callback_data='confirmar-compra'),
  InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
)


adminOptions = InlineKeyboardMarkup()
adminOptions.row_width = 2
adminOptions.add(
  InlineKeyboardButton(f"💳 Adicionar CC's Normais", callback_data='add-normal'),
  InlineKeyboardButton(f"💳 Adicionar CC's Full", callback_data='add-full'),
  InlineKeyboardButton(f'🎲 Adicionar Mix', callback_data='add-mix'),
  InlineKeyboardButton(f'💸 Alterar valores', callback_data='change-value'))

adminOptions.row_width = 1
adminOptions.add(
  InlineKeyboardButton(f'.', callback_data='.'))

adminOptions.row_width = 2
adminOptions.add(
  InlineKeyboardButton(f'👥 Informação do usuário', callback_data='usuarios'),
  InlineKeyboardButton(f'📄 Alterar saldo', callback_data='estoque'),
  InlineKeyboardButton(f'👥 Listar usuários', callback_data='usuarios'),
  InlineKeyboardButton(f'📄 Listar estoque', callback_data='estoque'),
)

adminOptions.row_width = 1
adminOptions.add(
  InlineKeyboardButton(f'.', callback_data='.'))

adminOptions.row_width = 2
adminOptions.add(
  InlineKeyboardButton(f'👥 Configurar pag. auto', callback_data='pag-auto'),
  InlineKeyboardButton(f'📄 Deletar pag. auto', callback_data='estoque'),
  InlineKeyboardButton(f'👥 Habilitar pagamento', callback_data='usuarios'),
  InlineKeyboardButton(f'📄 Apagar pag auto | manual', callback_data='estoque')
)

adminOptions.row_width = 1
adminOptions.add(
  InlineKeyboardButton(f'.', callback_data='.'))

adminOptions.row_width = 2
adminOptions.add(
  InlineKeyboardButton(f'🎁 Gerar GIFT', callback_data='usuarios'),
  InlineKeyboardButton(f'👥 Enviar SPAM', callback_data='estoque'),
)

adminOptions.row_width = 1
adminOptions.add(
  InlineKeyboardButton(f'🔙 Voltar', callback_data='menu'))

pagamentosOpts = InlineKeyboardMarkup()
pagamentosOpts.row_width = 2
pagamentosOpts.add(
    InlineKeyboardButton(f'Adicionar pagamento automático', callback_data='pag-automatico'),
    InlineKeyboardButton(f'Adicionar pagamento manual', callback_data='pag-manual'),
    InlineKeyboardButton(f'Excluir conta Automático', callback_data='del-auto'),
    InlineKeyboardButton(f'Excluir conta Manual', callback_data='del-manual'),
    InlineKeyboardButton(f'Definir pagamento Automático', callback_data='definir-pag-auto'),
    InlineKeyboardButton(f'Definir pagamento Manual', callback_data='definir-pag-manual'),
    InlineKeyboardButton('🔙 Voltar', callback_data='back_comprar')
  )

back_admin = InlineKeyboardMarkup()
back_admin.row_width = 1
back_admin.add(
  InlineKeyboardButton('🔙 Voltar', callback_data='admin'))
        
comprar2 = InlineKeyboardMarkup()
comprar2.row_width = 2
comprar2.add(
    InlineKeyboardButton("💳 CC's Full", callback_data="cc_full"),
    InlineKeyboardButton("💳 CC's Normal", callback_data="cc_normal"),
    InlineKeyboardButton('🎲 Mix', callback_data='cc_mix'),
    InlineKeyboardButton('🔎 Busca por banco', callback_data='search_bank'),
    InlineKeyboardButton('🔢 Busca por BIN', callback_data='search_bin'),
    InlineKeyboardButton('🌏 Busca por Países', callback_data='search_paises'))


i = InlineKeyboardMarkup()
i.row_width = 1
i.add(
    InlineKeyboardButton('🔙 Voltar', callback_data='back_comprar'))