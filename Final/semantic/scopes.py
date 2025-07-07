# semantic/utils.py
# Utilidades para manejo de pila de ámbitos (scopes) y tabla de símbolos


class ScopeStack:
    def __init__(self):
        # Cada scope es un dict con 'symbols', 'name', 'tipo', 'id'
        self.stack = [{"symbols": {}, "name": "global", "tipo": "global", "id": 0}]
        self._counters = {"global": 1}  # Contador por tipo de scope

    def enter_scope(self, tipo="anonimo"):
        # Asigna id incremental por tipo
        count = self._counters.get(tipo, 0) + 1
        self._counters[tipo] = count
        name = f"{tipo}_{count}" if tipo != "global" else "global"
        self.stack.append({"symbols": {}, "name": name, "tipo": tipo, "id": count})

    # Métodos de conveniencia
    def enter_scope_if(self):
        self.enter_scope("if")
    def enter_scope_while(self):
        self.enter_scope("while")
    def enter_scope_for(self):
        self.enter_scope("for")
    def enter_scope_func(self, funcname=None):
        tipo = f"func_{funcname}" if funcname else "func"
        self.enter_scope(tipo)


    def exit_scope(self):
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            raise Exception("No se puede salir del ámbito global")


    def declare(self, name, tipo):
        if name in self.stack[-1]["symbols"]:
            raise Exception(f"Variable '{name}' ya declarada en el ámbito '{self.stack[-1]['name']}' (tipo: {self.stack[-1]['tipo']}, id: {self.stack[-1]['id']})")
        self.stack[-1]["symbols"][name] = tipo


    def is_declared(self, name):
        return any(name in scope["symbols"] for scope in reversed(self.stack))


    def get_type(self, name):
        for scope in reversed(self.stack):
            if name in scope["symbols"]:
                return scope["symbols"][name]
        return None


    def current_scope_name(self):
        return self.stack[-1]["name"]

    def current_scope_type(self):
        return self.stack[-1]["tipo"]

    def current_scope_id(self):
        return self.stack[-1]["id"]
