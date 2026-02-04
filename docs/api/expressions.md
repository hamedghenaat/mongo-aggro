# Expression Operators API

This page documents the expression operators for building MongoDB
aggregation expressions with Python operator syntax.

## Field Reference

::: mongo_aggro.Field
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.F
    options:
      show_root_heading: true
      heading_level: 3

## Expression Base

::: mongo_aggro.ExpressionBase
    options:
      show_root_heading: true
      heading_level: 3

## Comparison Expressions

These expressions are created using Python comparison operators on Field
objects.

::: mongo_aggro.EqExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.NeExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.GtExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.GteExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LtExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LteExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.CmpExpr
    options:
      show_root_heading: true
      heading_level: 3

## Logical Expressions

These expressions combine comparison expressions using `&`, `|`, and `~`.

::: mongo_aggro.AndExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.OrExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.NotExpr
    options:
      show_root_heading: true
      heading_level: 3
