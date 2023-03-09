import atualiza
import i_magento
import threading, time
import fdb
import configparser
import pandas as pd
import sys
import keyboard
import logging

cfg = configparser.RawConfigParser()
cfg.read('Caminho.ini')

caminho = cfg.get('configuracao', 'servidor') +':'+cfg.get('configuracao', 'caminho')
empresa = cfg.get('configuracao', 'empresa')


def inicia_iMagento():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename='servico.log', filemode='w',format=format, level=logging.INFO,datefmt="%H:%M:%S")
    
    print("Pressione ESC para sair")
    while True:
        try:
            t1 = threading.Thread(target=integra_magento_fl(empresa))
            t2 = threading.Thread(target=integra_magento_fc(empresa))

            threads = []
            threads.append(t1)
            threads.append(t2)             

            t1.start()
            t2.start()
            
            for t in threads:
                t.join()            
            
            logging.info("Sincronizacao completa! "+str(time.ctime()))
            
            if keyboard.is_pressed('esc'):
                logging.info("Finalizando programa...")
                t1.stop()
                t2.stop()
                sys.exit(0)
        except:
            break                   

def integra_magento_fl(empresa):
    logging.info("Conectando na base: "+str(time.ctime()))

    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')

    comando ="select MAGENTO_PRODUTO,MAGENTO_ESTOQUE,MAGENTO_PEDIDO,MAGENTO_CLIENTE from parametro where id_empresa="+empresa
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    p_sis = pd.DataFrame(result_set)
    con.close()
    for index, row in p_sis.iterrows():
        if row[0] == "S":
            logging.info('inserir produto: '+str(time.ctime()))
            if i_magento.InserirProduto():
                i_magento.AtualizaCategoriaProduto()

        if row[3] == "S":
            logging.info('inserir cliente: '+str(time.ctime()))            
            i_magento.InserirCliente()
    time.sleep(900)

        

def integra_magento_fc(empresa):
    logging.info("Conectando na base: "+str(time.ctime()))
    con = fdb.connect(dsn=caminho, user='sysdba', password='masterkey',charset='ISO8859_1')

    comando ="select MAGENTO_PRODUTO,MAGENTO_ESTOQUE,MAGENTO_PEDIDO,MAGENTO_CLIENTE from parametro where id_empresa="+empresa
    
    cur = con.cursor()
    cur.execute(comando)
    result_set = cur.fetchall()
    p_sis = pd.DataFrame(result_set)
    con.close()
    for index, row in p_sis.iterrows():
 
        if row[1] == "S":
            logging.info('atualizar estoque: '+str(time.ctime()))
            #i_magento.AtualizaEstoqueProduto()
            
        if row[2] == "S":
            logging.info('inserir pedido: '+str(time.ctime()))            
            i_magento.InserirPedido(empresa)
    time.sleep(900)


def main():       
    if len(sys.argv) > 1 :
        if sys.argv[1] == "-A":
            logging.info("Inicializando a atualizacao "+sys.argv[2])
            atualiza.atualizar(sys.argv[2])
        if sys.argv[1] == "-V":
            logging.info(atualiza.versao(sys.argv[2]))
            return atualiza.versao(sys.argv[2])
        if sys.argv[1] == "-M" and sys.argv[2] == "-P" and sys.argv[3] == "-I" :
            logging.info("Incluir produtos Magento")
            i_magento.InserirProduto()
        if sys.argv[1] == "-M" and sys.argv[2] == "-P" and sys.argv[3] == "-E" :
            logging.info("Atualizando estoque produtos Magento")
            i_magento.AtualizaEstoqueProduto()
        if sys.argv[1] == "-M" and sys.argv[2] == "-P" and sys.argv[3] == "-C" :
            logging.info("Atualizando categorias produtos Magento")
            i_magento.AtualizaCategoriaProduto()
