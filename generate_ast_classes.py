"""
This file is used to generate AST.py instead of writing it out by hand.

It generates both and ABC and the respective subclasses aswell as a visitor to visit them all.
"""
from __future__ import annotations

import ast
import subprocess

__all__: list[str] = []

from typing import Optional, cast

visitor_names = set()


def new_node(
    module: ast.Module,
    name: str,
    fields: Optional[list[tuple[str, str]]] = None,
    parent: str = "AST",
    generate_init: bool = True,
    abstract_visit: bool = False,
    generate_visit: bool = True,
) -> None:
    """
    Generate a new AST node.

    :param module: the required ast.Module
    :param name: Name of the AST Node
    :param fields: required fields with type annotations
    :param parent: the parent class for the AST Node
    :param generate_init: weather we should generate a constructor for this
    :param abstract_visit: If the visitor should be an abstractmethod
    :param generate_visit: if we should generate a visitor at all
    :return: None
    """
    if fields is None:
        fields = []
    body: list[ast.AnnAssign | ast.FunctionDef] = [
        ast.AnnAssign(
            target=ast.Name(id=f_name, ctx=ast.Store()),
            annotation=ast.Name(id=f_type, ctx=ast.Load()),
            simple=1,
        )
        for f_name, f_type in fields
    ]

    if generate_visit:
        visitor_names.add(name)

    if generate_init:
        body.append(
            ast.FunctionDef(
                name="__init__",
                args=ast.arguments(
                    posonlyargs=[],
                    args=[ast.arg(arg="self")]
                    + [
                        ast.arg(
                            arg=f_name, annotation=ast.Name(id=f_type, ctx=ast.Load())
                        )
                        for f_name, f_type in fields
                    ],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                ),
                body=[
                    ast.Assign(
                        targets=[
                            ast.Attribute(
                                value=ast.Name(id="self", ctx=ast.Store()),
                                attr=f_name,
                                ctx=ast.Store(),
                            )
                        ],
                        value=ast.Name(id=f_name, ctx=ast.Load()),
                        lineno=0,
                    )
                    for f_name, _ in fields
                ],
                decorator_list=[],
                lineno=0,
            )
        )

    if generate_visit:
        body.append(
            ast.FunctionDef(
                name="accept",
                args=ast.arguments(
                    posonlyargs=[],
                    args=[
                        ast.arg(arg="self"),
                        ast.arg(arg="visitor", annotation=ast.Name(id="ASTVisitor")),
                    ],
                    vararg=ast.arg(
                        arg="args", annotation=ast.Name(id="Any", ctx=ast.Load())
                    ),
                    kwonlyargs=[],
                    kw_defaults=[],
                    kwarg=ast.arg(
                        arg="kwargs", annotation=ast.Name(id="Any", ctx=ast.Load())
                    ),
                    defaults=[],
                ),
                body=[
                    ast.Return(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="visitor", ctx=ast.Load()),
                                attr=f"visit_{name}",
                                ctx=ast.Load(),
                            ),
                            args=[
                                ast.Name(id="self", ctx=ast.Load()),
                                ast.Starred(
                                    value=ast.Name(id="args", ctx=ast.Load()),
                                    ctx=ast.Load(),
                                ),
                            ],
                            keywords=[
                                ast.keyword(value=ast.Name(id="kwargs", ctx=ast.Load()))
                            ],
                        )
                    )
                ],
                decorator_list=[ast.Name(id="abstractmethod", ctx=ast.Load())]
                if abstract_visit
                else [],
                lineno=0,
                returns=ast.Name(id="Any", ctx=ast.Load()),
            )
        )

    module.body.append(
        ast.ClassDef(
            name=name,
            bases=[ast.Name(id=parent, ctx=ast.Load())],
            keywords=[],
            body=body if body else [cast(ast.AnnAssign, ast.Pass())],
            decorator_list=[],
        )
    )


def generate_visitor(module: ast.Module) -> None:
    """
    Generate a visitor class for all already generated Nodes.

    :param module: The ast.module to generate the visitor in
    :return: None
    """
    module.body.append(
        ast.ClassDef(
            name="ASTVisitor",
            bases=[ast.Name(id="ABC", ctx=ast.Load())],
            keywords=[],
            body=[
                ast.FunctionDef(
                    name=f"visit_{cls}",
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[
                            ast.arg(arg="self"),
                            ast.arg(
                                arg="node",
                                annotation=ast.Name(id="AST", ctx=ast.Load()),
                            ),
                        ],
                        vararg=ast.arg(
                            arg="args", annotation=ast.Name(id="Any", ctx=ast.Load())
                        ),
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=ast.arg(
                            arg="kwargs", annotation=ast.Name(id="Any", ctx=ast.Load())
                        ),
                        defaults=[],
                    ),
                    body=[ast.Pass()],
                    decorator_list=[ast.Name(id="abstractmethod", ctx=ast.Load())],
                    lineno=0,
                    returns=ast.Name(id="Any", ctx=ast.Load()),
                )
                for cls in visitor_names
            ],
            decorator_list=[],
        )
    )


file_module = ast.Module(
    body=[
        ast.ImportFrom(
            module="__future__",
            names=[ast.alias(name="annotations")],
            level=0,
        ),
        ast.ImportFrom(
            module="abc",
            names=[ast.alias(name="ABC"), ast.alias(name="abstractmethod")],
            level=0,
        ),
        ast.ImportFrom(
            module="typing",
            names=[ast.alias(name="Optional"), ast.alias(name="Any")],
            level=0,
        ),
    ],
    type_ignores=[],
)


def main() -> None:
    """
    Orchestrate the generating of AST.py and actually list of the ast nodes to be generated.

    :return: None
    """
    new_node(file_module, "AST", parent="ABC", generate_init=False, abstract_visit=True)
    # new_node(file_module, "Expr", parent="AST", generate_init=False, generate_visit=False)
    new_node(file_module, "Module", [("body", "list[AST]")])
    new_node(file_module, "Block", [("label", "Optional[str]"), ("body", "list[AST]")])
    new_node(file_module, "If", [("label", "Optional[str]"), ("body", "list[AST]")])
    new_node(file_module, "While", [("label", "Optional[str]"), ("body", "list[AST]")])
    new_node(file_module, "Do", [("label", "Optional[str]"), ("body", "list[AST]")])

    generate_visitor(file_module)

    with open("AST.py", "w") as f:
        f.write("# noqa: D1\n")
        f.write(ast.unparse(file_module))

    subprocess.call(["black", "AST.py"])


if __name__ == "__main__":
    main()
