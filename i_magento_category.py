import pandas as pd
import logging

class Category:

    def __init__(self,low,high,name,is_active,position,available_sort_by,custom_design,custom_apply_to_products,
                 custom_design_from,custom_design_to,custom_layout_update,default_sort_by,description,
                 display_mode,is_anchor,landing_page,meta_description,meta_keywords,meta_title,page_layout,
                 url_key,include_in_menu,filter_price_range,custom_use_parent_settings):
        self.low = low
        self.high = high
        self.name = name
        self.is_active = is_active
        self.position = position
        self.available_sort_by = available_sort_by
        self.custom_design = custom_design
        self.custom_apply_to_products = custom_apply_to_products
        self.custom_design_from = custom_design_from
        self.custom_design_to = custom_design_to
        self.custom_layout_update = custom_layout_update
        self.default_sort_by = default_sort_by
        self.description = description
        self.display_mode = display_mode
        self.is_anchor = is_anchor
        self.landing_page = landing_page
        self.meta_description = meta_description
        self.meta_keywords = meta_keywords
        self.meta_title = meta_title
        self.page_layout = page_layout
        self.url_key = url_key
        self.include_in_menu = include_in_menu
        self.filter_price_range = filter_price_range
        self.custom_use_parent_settings = custom_use_parent_settings          

    def __getitem__(self, item):
        if item >= len(self):
            raise IndexError("Category is out of range")
        return self.low + item

    def __len__(self):
        return self.high - self.low       

def proc_Category(client,con):
    catalog_tree = client.category.tree(2)

    comando ="select distinct g.id_prodgrupo,g.descricao "
    comando +="from produto p inner join prodestoque pe on pe.id_produto = p.id_produto and pe.serial = '-' "
    comando +="left join prodgrupo g on g.id_prodgrupo = p.id_prodgrupo where pe.id_empresa=1 and p.ativo='S' "
    comando +="and p.cod_fabricante is not null and p.SINCRONIZAR_WEB = 'S' "
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    
    c_sis = pd.DataFrame(result_set)
    c_mag = pd.DataFrame(catalog_tree['children'],columns = ['category_id', 'name'])
    lista_final = c_sis.loc[(~c_sis[1].isin(list(c_mag['name']))) , [0,1]]
    
    ava_sort = client.category_attribute.options(67)
    def_sort = client.category_attribute.options(68)
    
    for rn in lista_final[1]:
        new_cat = Category(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,1,None,None)
        new_cat.low=0
        new_cat.high=1
        new_cat.name=rn
        new_cat.is_active=1
        new_cat.available_sort_by = ava_sort
        new_cat.default_sort_by = def_sort[1]
        client.category.create(2,new_cat)   
        logging.info("Incluindo categoria : "+ str(rn))
