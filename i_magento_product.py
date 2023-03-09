import pandas as pd
import re
import string
import logging
         
def insert_Product(client,con):
    comando ="select p.ID_PRODUTO,p.COD_FABRICANTE,p.apelido,p.DESCRICAO,p.UNIDADE,p.PATH_IMAGEM,g.descricao as Grupo, "
    comando +="p.TIPO,p.ID_FORNECEDOR,p.ID_MATERIAL,p.ATIVO,p.ID_SUBGRUPO,p.OBS,p.PESOLIQ,p.COD_BARRAS, "
    comando +="p.DESC_MARCA,p.PESOBRUTO,pe.ID_EMPRESA,pe.QTD,pe.CUSTO,pe.VENDA,pe.CUSTOPRAZO,pe.SERIAL, "
    comando +="pe.LOTE,pe.DATA_VALIDADE,pe.CUSTO_MEDIO,pe.VALOR_COMPRA,pe.VALOR_VENDA,pe.PRECO_COMPRA "
    comando +="from produto p inner join prodestoque pe on pe.id_produto = p.id_produto and pe.serial = '-'"
    comando +="left join prodgrupo g on g.id_prodgrupo = p.id_prodgrupo where pe.id_empresa=1 and p.ativo='S' "
    comando +="and p.cod_fabricante is not null and p.SINCRONIZAR_WEB ='S' "
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    
    prod_list = client.product.list()
    p_sis = pd.DataFrame(result_set)
    p_mag = pd.DataFrame(prod_list,columns = ['product_id', 'sku','category_ids'])
    
    lista_final = p_sis.loc[(~p_sis[1].isin(list(p_mag['sku']))) , [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]]
    
    if not lista_final.empty:
        for index, row in lista_final.iterrows():
            weight = row[16]
            if weight == None:
                weight = 1
        
            sku = row[1]
            if sku == 'SEM GTIN':
                sku = 'FAB'+str(row[0])
        
            descricao = row[3]
        
            chars = re.escape(string.punctuation)
            url = re.sub(r'['+chars+']', '',descricao)
            url = url.replace(" ","_")
            price = row[20]
            short = descricao.split(" ")[0]
        
            data={
                "product_id": "Null",
                "sku": sku,
                "set": "4",
                "type": "simple",
                "categories": ["2"],
                "websites": ["1"],
                "type_id": "simple",
                "name": descricao,
                "description": descricao,
                "short_description": short,
                "weight": str(weight),
                "old_id": None,
                "news_from_date": None,
                "news_to_date": None,
                "status": "1",
                "url_key": url,
                "url_path": url+".html",
                "visibility": "4",
                "category_ids": ["2"],
                "required_options": "0",
                "has_options": "0",
                "image_label": None,
                "small_image_label": None,
                "thumbnail_label": None,
                "country_of_manufacture": None,
                "price": str(price),
                "group_price": [],
                "special_price": None,
                "special_from_date": None,
                "special_to_date": None,
                "tier_price": [],
                "minimal_price": None,
                "msrp_enabled": "2",
                "msrp_display_actual_price_type": "4",
                "msrp": None,
                "tax_class_id": "0",
                "meta_title": None,
                "meta_keyword": None,
                "meta_description": None,
                "is_recurring": "0",
                "recurring_profile": None,
                "custom_design": None,
                "custom_design_from": None,
                "custom_design_to": None,
                "custom_layout_update": None,
                    "page_layout": None,
                    "options_container": "container1",
                    "gift_message_available": None
                    }
        
            logging.info("Incluindo produto: "+ str(sku))
            client.product.create(product_type="simple",attribute_set_id="4",sku=sku,data=data)        
        return True
    else:
        return False
    
    
def update_Product_Category(client,con):
    comando ="select p.ID_PRODUTO,p.COD_FABRICANTE,p.apelido,p.DESCRICAO,p.id_prodgrupo,g.descricao as Grupo "
    comando +="from produto p inner join prodestoque pe on pe.id_produto = p.id_produto and pe.serial = '-'"
    comando +="left join prodgrupo g on g.id_prodgrupo = p.id_prodgrupo where pe.id_empresa=1 and p.ativo='S' "
    comando +="and p.cod_fabricante is not null and p.SINCRONIZAR_WEB ='S' "
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    
    prod_list = client.product.list()
    catalog_tree = client.category.tree(2)
    listc = pd.DataFrame(catalog_tree["children"],columns = ['category_id', 'name'])
    
    p_sis = pd.DataFrame(result_set,columns=['ID_PRODUTO','COD_FABRICANTE','apelido','DESCRICAO','id_prodgrupo','Grupo'])
    p_mag = pd.DataFrame(prod_list,columns = ['product_id', 'sku','category_ids','cat_id'])
    
    cat_id = p_mag.category_ids.astype(str).str.replace('\[|\]|\'', '')
    p_mag['cat_id'] = cat_id
    sku = p_mag['sku']
    lista_f = pd.DataFrame(p_sis.loc[(p_sis['COD_FABRICANTE'].isin(sku))],columns=['ID_PRODUTO','COD_FABRICANTE','apelido','DESCRICAO','id_prodgrupo','Grupo'])
    lista_final = pd.DataFrame(lista_f.loc[lista_f['id_prodgrupo'] != p_mag['cat_id']],columns=['ID_PRODUTO','COD_FABRICANTE','apelido','DESCRICAO','id_prodgrupo','Grupo'])
    if not lista_final.empty:
        for index, row in lista_final.iterrows():
            sku = row[1]
            if sku == 'SEM GTIN':
                sku = 'FAB'+str(row[0])
        
            list_cat = listc[listc['name'] == row[5]]    
            prod_tmp = p_mag[p_mag['sku'] == sku]
            product_id = prod_tmp['product_id']
        
            data={"product_id": product_id.values[0],
                  "categories": list(list_cat['category_id'])
                  }
            client.product.update(product=product_id.values[0],data=data) 
            logging.info("Atualizando categoria produto : "+ str(sku))

def update_Product_Inventory(client,con):
    comando ="select p.ID_PRODUTO,p.COD_FABRICANTE,p.apelido,p.DESCRICAO,p.UNIDADE,p.PATH_IMAGEM,g.descricao as Grupo, "
    comando +="p.TIPO,p.ID_FORNECEDOR,p.ID_MATERIAL,p.ATIVO,p.ID_SUBGRUPO,p.OBS,p.PESOLIQ,p.COD_BARRAS, "
    comando +="p.DESC_MARCA,p.PESOBRUTO,pe.ID_EMPRESA,pe.QTD,pe.CUSTO,pe.VENDA,pe.CUSTOPRAZO,pe.SERIAL, "
    comando +="pe.LOTE,pe.DATA_VALIDADE,pe.CUSTO_MEDIO,pe.VALOR_COMPRA,pe.VALOR_VENDA,pe.PRECO_COMPRA "
    comando +="from produto p inner join prodestoque pe on pe.id_produto = p.id_produto and pe.serial = '-'"
    comando +="left join prodgrupo g on g.id_prodgrupo = p.id_prodgrupo where pe.id_empresa=1 and p.ativo='S' "
    comando +="and p.cod_fabricante is not null and p.SINCRONIZAR_WEB ='S'  "
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    prod_list = client.product.list()
    
    p_sis = pd.DataFrame(result_set)
    p_mag = pd.DataFrame(prod_list,columns = ['product_id', 'sku','category_ids'])
    
    lista_final = p_sis.loc[(p_sis[1].isin(list(p_mag['sku']))) , [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]]
    
    if not lista_final.empty:
        for index, row in lista_final.iterrows():
            sku = row[1]
            if sku == 'SEM GTIN':
                sku = 'FAB'+str(row[0])
                
            prod_tmp = p_mag[p_mag['sku'] == sku]
            product_id = prod_tmp['product_id']
            qtd = row[18]
                
            data={
                "qty": str(qtd),
                "is_in_stock": "1"
                }        
                
            client.inventory.update(product=product_id.values[0],data=data) 
            logging.info("Atualizando estoque : "+ str(sku))
    
def delete_Product(client,con):
    comando ="select p.ID_PRODUTO,p.COD_FABRICANTE,p.apelido,p.DESCRICAO,p.UNIDADE,p.PATH_IMAGEM,g.descricao as Grupo, "
    comando +="p.TIPO,p.ID_FORNECEDOR,p.ID_MATERIAL,p.ATIVO,p.ID_SUBGRUPO,p.OBS,p.PESOLIQ,p.COD_BARRAS, "
    comando +="p.DESC_MARCA,p.PESOBRUTO,pe.ID_EMPRESA,pe.QTD,pe.CUSTO,pe.VENDA,pe.CUSTOPRAZO,pe.SERIAL, "
    comando +="pe.LOTE,pe.DATA_VALIDADE,pe.CUSTO_MEDIO,pe.VALOR_COMPRA,pe.VALOR_VENDA,pe.PRECO_COMPRA "
    comando +="from produto p inner join prodestoque pe on pe.id_produto = p.id_produto and pe.serial = '-'"
    comando +="left join prodgrupo g on g.id_prodgrupo = p.id_prodgrupo where pe.id_empresa=1 and p.ativo='S' "
    comando +="and cod_fabricante is not null and disponivel_web ='S' "
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    
    prod_list = client.product.list()
    p_sis = pd.DataFrame(result_set)
    p_mag = pd.DataFrame(prod_list,columns = ['product_id', 'sku','category_ids'])
    
    lista_final = p_sis.loc[(p_sis[1].isin(list(p_mag['sku']))) , [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]]
    if not lista_final.empty:
        for index, row in lista_final.iterrows():       
            sku = row[1]
            if sku == 'SEM GTIN':
                sku = 'FAB'+str(row[0])
        
            client.product.delete(sku)   
            logging.info("Excluindo produto: "+ str(sku))

