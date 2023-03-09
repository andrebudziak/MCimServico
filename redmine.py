import pandas as pd
from redminelib import Redmine
from matplotlib import pyplot as plt
import numpy as np

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} )".format(pct, absolute)

data = []

redmine = Redmine('https://redmine.mastercim.info/', key='28b658658ad8aba3be5bb7c2e5cb7fbca49bc24f')

def rel_atendimento():
    issues = redmine.issue.all(project_id='suporte_tecnico',sort='category:desc')
    df_marks = pd.DataFrame(data,columns={'author','created_on','description','id','project','status','subject','cliente','qtd'})
    i = 0
    for issue in issues:    
      if issue.status.name == 'Fechada':
          i = 1
          custom = issue.custom_fields._resources
          cli = ''
          for l in custom:
              if l['name'] == 'Cliente':
                  cli = l['value']
          dt_cria = "{}/{}/{}".format(issue.created_on.day,issue.created_on.month,issue.created_on.year)
          new_row = {'author':str(issue.author), 'created_on':dt_cria, 'description':issue.description, 'id':issue.id,'project':issue.project,'status':issue.status,'subject':issue.subject,'cliente':cli,'qtd':i}      
          df_marks = df_marks.append(new_row, ignore_index=True)   
    
    
    #df_marks.to_csv (r'C:\Andre\Projeto\Servico.python\cliente.csv', header=True)
    #clientes
    atecli = df_marks["cliente"].value_counts().nlargest(30)
    
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(aspect="equal"))
    
    wedges, texts, autotexts = ax.pie(atecli, autopct=lambda pct: func(pct, atecli),
                                      textprops=dict(color="w"))
    
    ax.legend(wedges, atecli.index,
              title="Clientes",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.setp(autotexts, size=8, weight="bold")
    
    ax.set_title("Atendimentos por Cliente 30 Mais Atendidos")    
    
    plt.savefig('static/atepcliente.png')
    
    #data
    ateclidata = df_marks.groupby('cliente')['created_on'].value_counts().nlargest(30)
    ateclidata.plot(kind='barh', title='Maior incidencia dia por cliente top 30', zorder=2)
    plt.savefig('static/incidenciacliente.png')
    
    
    #atendente
    # gca stands for 'get current axis'
    ax = plt.gca()
    ateusu =  df_marks.groupby('author')['qtd'].sum().to_frame().reset_index()
    ateusu.plot.bar(title='Atendimento por Atendente',x='author',y='qtd')
    
    ateusup =  df_marks.groupby(['author','created_on'])['qtd'].sum().to_frame().reset_index()
    ateusup.plot.scatter(title='Atendimento por Atendente Periodo',x='qtd',y='author',colormap='viridis')
    plt.savefig('static/atendenteperiodo.png')

def rel_ospendente():
    issues = redmine.issue.all(project_id='suporte_tecnico',sort='category:desc')
    df_marks = pd.DataFrame(data,columns={'author','created_on','description','id','project','status','subject','cliente','qtd'})
    i = 0
    for issue in issues:    
      if issue.status.name == 'Fechada':
          i = 1
          custom = issue.custom_fields._resources
          cli = ''
          for l in custom:
              if l['name'] == 'Cliente':
                  cli = l['value']
          dt_cria = "{}/{}/{}".format(issue.created_on.day,issue.created_on.month,issue.created_on.year)
          new_row = {'author':str(issue.author), 'created_on':dt_cria, 'description':issue.description, 'id':issue.id,'project':issue.project,'status':issue.status,'subject':issue.subject,'cliente':cli,'qtd':i}      
          df_marks = df_marks.append(new_row, ignore_index=True)   
    



