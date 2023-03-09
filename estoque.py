class Estoque(API):
    def list(self):
        return self.call('stockItems.list', [])