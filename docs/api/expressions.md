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

## Arithmetic Expressions

::: mongo_aggro.AddExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SubtractExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MultiplyExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DivideExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AbsExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ModExpr
    options:
      show_root_heading: true
      heading_level: 3

## Conditional Expressions

::: mongo_aggro.CondExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IfNullExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SwitchExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SwitchBranch
    options:
      show_root_heading: true
      heading_level: 3

## String Expressions

::: mongo_aggro.ConcatExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SplitExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToLowerExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToUpperExpr
    options:
      show_root_heading: true
      heading_level: 3

## Array Expressions

::: mongo_aggro.ArraySizeExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SliceExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.FilterExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MapExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ReduceExpr
    options:
      show_root_heading: true
      heading_level: 3

## Date Expressions

::: mongo_aggro.DateAddExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateSubtractExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateDiffExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateToStringExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateFromStringExpr
    options:
      show_root_heading: true
      heading_level: 3

## Type Conversion Expressions

::: mongo_aggro.ToDateExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToStringExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToIntExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToDoubleExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToBoolExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToObjectIdExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ConvertExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.TypeExpr
    options:
      show_root_heading: true
      heading_level: 3
