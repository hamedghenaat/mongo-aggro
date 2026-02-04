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

::: mongo_aggro.ToLongExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ToDecimalExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IsNumberExpr
    options:
      show_root_heading: true
      heading_level: 3

## Set Expressions

::: mongo_aggro.SetUnionExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SetIntersectionExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SetDifferenceExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SetEqualsExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SetIsSubsetExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AnyElementTrueExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AllElementsTrueExpr
    options:
      show_root_heading: true
      heading_level: 3

## Object Expressions

::: mongo_aggro.MergeObjectsExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ObjectToArrayExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ArrayToObjectExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.GetFieldExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SetFieldExpr
    options:
      show_root_heading: true
      heading_level: 3

## Variable Expressions

::: mongo_aggro.LetExpr
    options:
      show_root_heading: true
      heading_level: 3

## Miscellaneous Expressions

::: mongo_aggro.LiteralExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RandExpr
    options:
      show_root_heading: true
      heading_level: 3

## Additional Array Expressions

::: mongo_aggro.ArrayElemAtExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ConcatArraysExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.InArrayExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IndexOfArrayExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IsArrayExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ReverseArrayExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SortArrayExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RangeExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.FirstNExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LastNExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MaxNExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MinNExpr
    options:
      show_root_heading: true
      heading_level: 3

## Additional String Expressions

::: mongo_aggro.TrimExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LTrimExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RTrimExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ReplaceOneExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ReplaceAllExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RegexMatchExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RegexFindExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RegexFindAllExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SubstrCPExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.StrLenCPExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.StrCaseCmpExpr
    options:
      show_root_heading: true
      heading_level: 3

## Additional Arithmetic Expressions

::: mongo_aggro.CeilExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.FloorExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RoundExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.TruncExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SqrtExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.PowExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ExpExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LnExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.Log10Expr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LogExpr
    options:
      show_root_heading: true
      heading_level: 3

## Trigonometry Expressions

::: mongo_aggro.SinExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.CosExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.TanExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AsinExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AcosExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AtanExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.Atan2Expr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SinhExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.CoshExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.TanhExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AsinhExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AcoshExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.AtanhExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DegreesToRadiansExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.RadiansToDegreesExpr
    options:
      show_root_heading: true
      heading_level: 3

## Bitwise Expressions

::: mongo_aggro.BitAndExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.BitOrExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.BitXorExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.BitNotExpr
    options:
      show_root_heading: true
      heading_level: 3

## Data Size Expressions

::: mongo_aggro.BsonSizeExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.BinarySizeExpr
    options:
      show_root_heading: true
      heading_level: 3

## Date Part Expressions

::: mongo_aggro.YearExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MonthExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DayOfMonthExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DayOfWeekExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DayOfYearExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.HourExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MinuteExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.SecondExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.MillisecondExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.WeekExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IsoWeekExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IsoWeekYearExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IsoDayOfWeekExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateFromPartsExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateToPartsExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DateTruncExpr
    options:
      show_root_heading: true
      heading_level: 3

## Window Expressions

These operators are used with the `$setWindowFields` stage.

::: mongo_aggro.RankExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DenseRankExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DocumentNumberExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ShiftExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.ExpMovingAvgExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.DerivativeExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.IntegralExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.CovariancePopExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.CovarianceSampExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LinearFillExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.LocfExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.TopExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.BottomExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.TopNWindowExpr
    options:
      show_root_heading: true
      heading_level: 3

::: mongo_aggro.BottomNWindowExpr
    options:
      show_root_heading: true
      heading_level: 3
