import sys

sys.path.insert(0, "/Projeto/MCimServico")

import app as application

if __name__ == "__main__":    
    app =application.create_app()
    app.run(debug=True)