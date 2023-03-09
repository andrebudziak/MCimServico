import pandas as pd
from datetime import date
from datetime import timedelta
import logging
import time

def insert_Cliente(con,ord_cli):
    comando ="select e.id_entidade,e.nome,e.cnpj_cpf from entidade e"
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
        
    cl_full = pd.DataFrame(ord_cli,columns=['customer_id','email','firstname','lastname','middlename','city','country_id','fax','postcode','region','street','nome'])
    if cl_full['email'].isnull:
        cl_full['email'] = '0'
    if cl_full['fax'].isnull:
        cl_full['fax'] = '0'        
    if cl_full['middlename'].isnull:
        cl_full['middlename'] = '0'
    if cl_full['lastname'].isnull:
        cl_full['lastname'] = '0'
    cl_full['nome'] = cl_full['firstname'].str.upper()+' '+ cl_full['middlename'].str.upper() +' '+ cl_full['lastname'].str.upper()
    
    p_sis = pd.DataFrame(result_set,columns=['id_entidade','nome','cnpj_cpf'])

    nome = p_sis['nome']
    lista_final = cl_full.loc[~cl_full['nome'].isin(nome)]    
    
    bnome = (cl_full['nome']).to_string(index=False)
    comando ="select e.id_entidade,e.nome,e.cnpj_cpf from entidade e where e.nome='"+bnome.strip()+"'"
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    p_sis = pd.DataFrame(result_set,columns=['id_entidade','nome','cnpj_cpf'])
    
    if not lista_final.empty:
        for index, row in lista_final.iterrows():
            
            logging.info("Pegando id cliente : "+ str(time.ctime()))
            comando ="select (id_entidade + 1) as id_entidade from gerador"
            cur = con.cursor()
            cur.execute(comando)
            result_set = cur.fetchall()
            pGer = pd.DataFrame(result_set,columns=['id_entidade'])
            newId = (pGer['id_entidade']).to_string(index=False)
            newId = newId.strip()
            newId = str(newId)
            
            nome = row['nome']
            if row['city'] is None:
                cidade='0'
            else:
                cidade = row['city']
            if row['fax'] is None:
                fax='0'
            else:
                fax = row['fax']
            if row['email'] is None:
                email ='0'
            else:
                email = row['email']
            if row['postcode'] is None:
                cep ='0'
            else:
                cep = row['postcode']                
            if row['street'] is None:
                rua = '0'
            else:
                rua = row['street']
            
            comando ="INSERT INTO ENTIDADE (ID_ENTIDADE, NOME, FANTASIA, CIDADE, CEP, FONE1, RUA, EMAIL,ID_TIPO_CADASTRO,ATIVO,ID_EMPRESA,CONSUMIDORFINAL) "
            comando +="VALUES("+ newId +",'"+nome+"','"+nome+"','"+cidade+"','"+cep+"','"+fax+"','"+rua+"','"+email+"',1,'S',0,'N')"
            cur = con.cursor()
            cur.execute(comando)
            con.commit()
            logging.info("Incluindo cliente : "+ str(row['nome']) + " "+ str(time.ctime()))
            
            logging.info("Atualizando id cliente : "+ str(time.ctime()))
            comando ="update gerador set id_entidade ="+ str(newId)
            cur = con.cursor()
            cur.execute(comando)
            con.commit()
            return str(newId)
    else:
        return (p_sis['id_entidade']).to_string(index=False)
         
def insert_Pedido(client,con,empresa):
    
    cli_order=pd.DataFrame(client.order.list())
    
    for index,lc in cli_order.iterrows():
        if lc['status'] == 'pending' and lc['state'] == 'new':                       
            quote_id = lc['quote_id']
            store_id = lc['store_id']
            cli_order_info = client.order.info(lc['increment_id'])
            
            cli_cart=pd.DataFrame(client.cart_payment.list(quote_id,store_id))
            if cli_cart['title'].values == 'Dinheiro':
                forma_pagamento = ' À VISTA'
            if cli_cart['title'].values == 'Cartão de Crédito':
                forma_pagamento = '6X'
           
            comando ="select id_prazo from prazo where descricao = '"+forma_pagamento+"'"
            cur = con.cursor()
            cur.execute(comando)
            result_set = cur.fetchall()
            id_prazo = pd.DataFrame(result_set,columns=['id_prazo'])
            id_prazo = (id_prazo['id_prazo']).to_string(index=False)
            id_prazo = id_prazo.strip()

            prod = pd.DataFrame(cli_order_info['items'])
            payment = pd.DataFrame([cli_order_info['payment']],columns=['amount_ordered','base_amount_ordered','base_shipping_amount','method','shipping_amount'])
            address = pd.DataFrame([cli_order_info['shipping_address']],
                                   columns=['address_id','address_type','city','company','country_id','customer_address_id',
                                            'customer_id','email','fax','firstname','lastname','middlename','parent_id',
                                            'postcode','prefix','quote_address_id','region','region_id','street','suffix',
                                            'telephone','vat_id','vat_is_valid','vat_request_date','vat_request_id','vat_request_success'])
                
            id_entidade = insert_Cliente(con,address)
            id_entidade = id_entidade.strip()
            
            comando ="select e.id_entidade from entidade e inner join usuario u on u.id_usuario = e.id_entidade where u.apelido = 'MASTER'"
            cur = con.cursor()
            cur.execute(comando)
            result_set = cur.fetchall()
            p_sis = pd.DataFrame(result_set,columns=['id_entidade'])
            id_vendedor = (p_sis['id_entidade']).to_string(index=False)     
            id_vendedor = id_vendedor.strip()      
           
            comando ="select m.id_movimento,m.cod_site from movimentom m where m.tipo='VBA' and m.fechado <> 'S' and m.estorno <> 'S' and m.cod_site='"+lc['increment_id']+"'"
        
            cur = con.cursor()
            cur.execute(comando)
            result_set = cur.fetchall()
            codigo = lc['increment_id']
            p_sis = pd.DataFrame(result_set)
            if p_sis.empty:
                data_atual = date.today()
                data = data_atual.strftime('%d.%m.%Y')
                valid_mov = data_atual + timedelta(days=31)
                validade_mov = valid_mov.strftime('%d.%m.%Y')
                if not cli_order_info['shipping_amount'] is None:
                    frete = cli_order_info['shipping_amount']
                else:
                    frete ='0'
                if not cli_order_info['weight'] is None:
                    peso = cli_order_info['weight']
                else:
                    peso = '0'
                if not cli_order_info['grand_total'] is None:
                    total = cli_order_info['grand_total']
                else:
                    total = '0'
                if not cli_order_info['subtotal'] is None:
                    sub_total = cli_order_info['subtotal']
                else:
                    sub_total = '0'
                if not cli_order_info['tax_invoiced'] is None:
                    outros = cli_order_info['tax_invoiced']
                else:
                    outros = '0'
                if not cli_order_info['total_qty_ordered'] is None:
                    qtd_total = cli_order_info['total_qty_ordered']
                else:
                    qtd_total = '0'            
                if not cli_order_info['discount_amount'] is None:
                    descvlr = cli_order_info['discount_amount']
                else:
                    descvlr = '0'
                if descvlr != '0.0000':
                    desc = total / descvlr
                else:
                    desc = '0'
                
                comando = "INSERT INTO MOVIMENTOM(ID_MOVIMENTO,TIPO,ID_EMPRESA,DATA,ID_ENTIDADE,ID_VENDEDOR,DESCONTO,OUTROS,FRETE,ESTORNO,DESCVLR,FECHADO,"
                comando +="PESOBRUTO,PESOLIQ,VALIDADEMOV,ID_USUARIO,QTDNF,TOTAL_PROD,ID_USU_CRIADOR,DATA_CRIA,TOTAL,COD_SITE,ID_PRAZO)VALUES("
                comando +="GEN_ID(GEN_MOVIMENTO,1),'VBA',"+empresa+",'"+data+"',"+id_entidade+","+id_vendedor+","+desc+","+outros+","+frete+",'N',"+descvlr+","
                comando +="'N',"+peso+","+peso+",'"+validade_mov+"',"+id_vendedor+","+qtd_total+","+sub_total+","+id_vendedor+",'"+data+"',"+total+",'"+codigo+"',"+id_prazo+")"
                cur = con.cursor()
                cur.execute(comando)
                logging.info("Inserindo pedido:"+codigo +" "+ str(time.ctime()))
                prod_item = prod.loc[prod['product_type'] == 'simple']
                for index,lc in prod_item.iterrows():
                    sequencia = lc['item_id']
                    id_produto = lc['product_id']
                    descricao = lc['name']
                    if not lc['weight'] is None:
                        peso = lc['weight']
                    else:
                        peso = '0'
                    if not lc['qty_ordered'] is None:
                        qtd = lc['qty_ordered']
                    else:
                        qtd = '0'
                    if not lc['price'] is None:
                        custo = lc['price']
                    else:
                        custo = '0'
                    if lc['tax_amount'] is None:
                        outros = lc['tax_amount']
                    else:
                        outros = '0'
                    if not lc['discount_amount'] is None:
                        desconto = lc['discount_amount']
                    else:
                        desconto = '0'
                    if not lc['row_total'] is None:
                        totalliq = lc['row_total']
                    else:
                        totalliq ='0'
                    if not lc['row_total_incl_tax'] is None:
                        total = lc['row_total_incl_tax']
                    else:
                        total = '0'                
    
                    comando_d ="INSERT INTO MOVIMENTOD(SEQUENCIA,QTD,ID_MOVIMENTO,TIPO,ID_EMPRESA,ID_PRODESTOQUE,CUSTO,VENDA,"
                    comando_d+="DESCPROD,DESCONTO,ID_VENDEDOR,VLR_TOTALLIQ)VALUES("
                    comando_d+=""+sequencia+","+qtd+",GEN_ID(GEN_MOVIMENTO,0),'VBA',"+empresa+","+id_produto+","+custo+","
                    comando_d+=""+custo+",'"+descricao+"',"+desconto+","+id_vendedor+","+totalliq+")"
                    cur = con.cursor()
                    cur.execute(comando_d)
                    
                    logging.info("Inserindo item pedido produto:"+id_produto +" "+str(time.ctime()))
                con.commit()

        
        
        
    
