# noqa: D1
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class AST(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor, *args: Any, **kwargs: Any) -> Any:
        return visitor.visit_AST(self, *args, **kwargs)


class Module(AST):
    body: list[AST]

    def __init__(self, body: list[AST]):
        self.body = body

    def accept(self, visitor: ASTVisitor, *args: Any, **kwargs: Any) -> Any:
        return visitor.visit_Module(self, *args, **kwargs)


class Block(AST):
    label: Optional[str]
    body: list[AST]

    def __init__(self, label: Optional[str], body: list[AST]):
        self.label = label
        self.body = body

    def accept(self, visitor: ASTVisitor, *args: Any, **kwargs: Any) -> Any:
        return visitor.visit_Block(self, *args, **kwargs)


class If(AST):
    label: Optional[str]
    body: list[AST]

    def __init__(self, label: Optional[str], body: list[AST]):
        self.label = label
        self.body = body

    def accept(self, visitor: ASTVisitor, *args: Any, **kwargs: Any) -> Any:
        return visitor.visit_If(self, *args, **kwargs)


class While(AST):
    label: Optional[str]
    body: list[AST]

    def __init__(self, label: Optional[str], body: list[AST]):
        self.label = label
        self.body = body

    def accept(self, visitor: ASTVisitor, *args: Any, **kwargs: Any) -> Any:
        return visitor.visit_While(self, *args, **kwargs)


class Do(AST):
    label: Optional[str]
    body: list[AST]

    def __init__(self, label: Optional[str], body: list[AST]):
        self.label = label
        self.body = body

    def accept(self, visitor: ASTVisitor, *args: Any, **kwargs: Any) -> Any:
        return visitor.visit_Do(self, *args, **kwargs)


class ASTVisitor(ABC):
    @abstractmethod
    def visit_Do(self, node: AST, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def visit_Module(self, node: AST, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def visit_While(self, node: AST, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def visit_AST(self, node: AST, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def visit_If(self, node: AST, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def visit_Block(self, node: AST, *args: Any, **kwargs: Any) -> Any:
        pass
