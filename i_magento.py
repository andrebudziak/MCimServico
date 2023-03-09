import magento
import i_magento_category as cat
import i_magento_product as prod
import i_magento_cliente as cli 
import i_magento_pedido as ped
import fdb
import configparser

cfg = configparser.RawConfigParser()
cfg.read('Caminho.ini')
caminho = cfg.get('configuracao', 'servidor') +':'+cfg.get('configuracao', 'caminho')

#'http://acasadaobra.com.br/index.php/api/v2_soap?wsdl=1&type=soap' endereco soap v2
#'http://acasadaobra.com.br/index.php/api/soap/?wsdl' endereco soap v1

def InserirCliente():
    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')
    url = 'http://acasadaobra.com.br'
    apiuser = 'mastercim'
    apipass = 'f640912cd6c2b91004693dccd1b2dd5b'
    # Create an instance of API
    client = magento.API(url, apiuser, apipass)    
    #cat.proc_Category(client,con)
    cli.insert_Cliente(client,con)
    con.close()

def InserirProduto():
    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')
    url = 'http://acasadaobra.com.br'
    apiuser = 'mastercim'
    apipass = 'f640912cd6c2b91004693dccd1b2dd5b'
    # Create an instance of API
    client = magento.API(url, apiuser, apipass)    
    cat.proc_Category(client,con)
    prod.insert_Product(client,con)
    con.close()
    
def AtualizaEstoqueProduto():
    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')
    url = 'http://acasadaobra.com.br'
    apiuser = 'mastercim'
    apipass = 'f640912cd6c2b91004693dccd1b2dd5b'
    # Create an instance of API
    client = magento.API(url, apiuser, apipass)    
    #cat.proc_Category(client,con)
    prod.update_Product_Inventory(client,con)
    con.close()

def AtualizaCategoriaProduto():
    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')
    url = 'http://acasadaobra.com.br'
    apiuser = 'mastercim'
    apipass = 'f640912cd6c2b91004693dccd1b2dd5b'
    # Create an instance of API
    client = magento.API(url, apiuser, apipass)    
    #cat.proc_Category(client,con)
    prod.update_Product_Category(client,con)
    con.close()
    
def InserirPedido(empresa):
    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')
    url = 'http://acasadaobra.com.br'
    apiuser = 'mastercim'
    apipass = 'f640912cd6c2b91004693dccd1b2dd5b'
    # Create an instance of API
    client = magento.API(url, apiuser, apipass)    
    ped.insert_Pedido(client,con,empresa)
    con.close()
