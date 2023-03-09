import pandas as pd
import logging
         
def insert_Cliente(client,con):
    comando ="select e.id_entidade,e.nome,e.cnpj_cpf from entidade e"
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    
    cli=pd.DataFrame(client.customer.list(),columns=['customer_id','email','firstname','gender','lastname','middlename'])

    for index,lc in cli.iterrows():
        cli_list_adress = pd.DataFrame(client.customer_address.list(lc['customer_id']),columns=['firstname','lastname','middlename','city','country_id','fax','postcode','region','street'])
        
    cli_list_full = pd.concat([cli,cli_list_adress])
    cli_list_full = cli_list_full.drop_duplicates(keep = 'first') 
    cli_list_full.reset_index(inplace=True)
    cl_full = pd.DataFrame(cli_list_full,columns=['customer_id','email','firstname','lastname','middlename','city','country_id','fax','postcode','region','street','nome'])
    cl_full['nome'] = cl_full['firstname'].str.upper()+' '+ cl_full['middlename'].str.upper() +' '+ cl_full['lastname'].str.upper()
    cl_full['city'] = cli_list_adress['city']
    cl_full['country_id'] = cli_list_adress['country_id']
    cl_full['fax'] = cli_list_adress['fax']
    cl_full['postcode'] = cli_list_adress['postcode']
    cl_full['region'] = cli_list_adress['region']
    cl_full['street'] = cli_list_adress['street']
    cl_full = cl_full[cl_full['customer_id'].notna()]
    
    p_sis = pd.DataFrame(result_set,columns=['id_entidade','nome','cnpj_cpf'])

    nome = p_sis['nome']
    lista_final = cl_full.loc[~cl_full['nome'].isin(nome)]
    
    for index, row in lista_final.iterrows():
        if not pd.isnull(row['postcode']):
            comando ="INSERT INTO ENTIDADE (ID_ENTIDADE, NOME,FANTASIA, CIDADE, CEP, FONE1, RUA, EMAIL,ID_TIPO_CADASTRO,ATIVO,ID_EMPRESA,CONSUMIDORFINAL) "
            comando +="VALUES(0,'"+row['nome']+"','"+row['nome']+"','"+row['city']+"','"+row['postcode']+"','"+row['fax']+"','"+row['street']+"','"+row['email']+"',1,'S',0,'N')"
            cur = con.cursor()
            cur.execute(comando)
            con.commit()
            logging.info("Incluindo cliente : "+ str(row['nome']))
