"""
Module for code execution
"""


class Environment:
    def __init__(self):
        self._scope_stack = [Scope()]

    def push_scope(self):
        self._scope_stack.append(Scope())

    def pop_scope(self):
        if len(self._scope_stack) == 1:
            raise ValueError("TODO")

        self._scope_stack.pop()

    def add_var(self, identifier):
        self._scope_stack[-1].set_var(identifier)

    def set_var(self, identifier, value):
        for scope in reversed(self._scope_stack):
            if scope.exists_var(identifier):
                scope.set_var(identifier, value)
                return

        raise ValueError("TODO")

    def get_var(self, identifier):
        for scope in reversed(self._scope_stack):
            if scope.exists_var(identifier):
                return scope.get_var(identifier)

        raise ValueError("TODO")

    def set_fun(self, identifier, node):
        self._scope_stack[-1].set_fun(identifier, node)

    def get_fun(self, identifier):
        for scope in reversed(self._scope_stack):
            if scope.exists_fun(identifier):
                return scope.get_fun(identifier)

        raise ValueError("TODO")


class Scope:
    def __init__(self):
        self._variables = {}
        self._functions = {}

    def exists_var(self, identifier):
        return identifier in self._variables

    def set_var(self, identifier, value=None):
        self._variables[identifier] = value

    def get_var(self, identifier):
        return self._variables[identifier]

    def exists_fun(self, identifier):
        return identifier in self._functions

    def set_fun(self, identifier, node):
        self._functions[identifier] = node

    def get_fun(self, identifier):
        return self._functions[identifier]
