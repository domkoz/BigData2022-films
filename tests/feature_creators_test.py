import findspark

findspark.init()

import pytest
import pyspark

from pyspark.sql import SparkSession, DataFrame
from pyspark_test import assert_pyspark_df_equal
from lib.feature_creators import add_epoch_column
from lib.pyspark_startup import init


def test_add_epoch_column():
    spark = init()
    df = spark.createDataFrame(
        [
            (1, 1900),
            (2, 1917),
            (3, 1920),
            (4, 1938),
            (5, 1953),
            (6, 1960),
            (7, 1984),
            (8, 1993),
            (9, 2008),
            (10, 2022),
        ],
        "id int, rok_wydania_produkcji int",
    )

    expect_df = spark.createDataFrame(
        [
            (1, 1900, "1"),
            (2, 1917, "2"),
            (3, 1920, "3"),
            (4, 1938, "4"),
            (5, 1953, "5"),
            (6, 1960, "6"),
            (7, 1984, "7"),
            (8, 1993, "8"),
            (9, 2008, "9"),
            (10, 2022, "10"),
        ],
        "id int, rok_wydania_produkcji int, epoka_rok_wydania_produkcji string",
    )

    result = add_epoch_column(df)
    assert_pyspark_df_equal(result, expect_df)


def test_add_epoch_start_end_year_epoch():
    spark = init()
    df = spark.createDataFrame(
        [
            (1, 1900, 1900),
            (2, 1917, 1919),
            (3, 1920, 1921),
            (4, 1938, 1939),
            (5, 1953, 1980),
            (6, 1960, 1965),
            (7, 1984, 1986),
            (8, 1993, 1996),
            (9, 2008, 2020),
            (10, 2022, 2023),
        ],
        "id int, rok_wydania_produkcji int, rok_zakonczenia_produkcji int",
    )

    expect_df = spark.createDataFrame(
        [
            (1, 1900, 1900, "1", "1"),
            (2, 1917, 1919, "2", "3"),
            (3, 1920, 1921, "3", "3"),
            (4, 1938, 1939, "4", "4"),
            (5, 1953, 1980, "5", "7"),
            (6, 1960, 1965, "6", "6"),
            (7, 1984, 1986, "7", "8"),
            (8, 1993, 1996, "8", "9"),
            (9, 2008, 2020, "9", "10"),
            (10, 2022, 2023, "10", "10"),
        ],
        "id int, rok_wydania_produkcji int, rok_zakonczenia_produkcji int, epoka_rok_wydania_produkcji string, epoka_rok_zakonczenia_produkcji string",
    )

    result = add_epoch_column(df, add_end_year_epoch=True)
    assert_pyspark_df_equal(result, expect_df)


def test_add_epoch_drop_columns():
    spark = init()
    df = spark.createDataFrame(
        [
            (1, 1900, 1900),
            (2, 1917, 1919),
            (3, 1920, 1921),
            (4, 1938, 1939),
            (5, 1953, 1980),
            (6, 1960, 1965),
            (7, 1984, 1986),
            (8, 1993, 1996),
            (9, 2008, 2020),
            (10, 2022, 2023),
        ],
        "id int, rok_wydania_produkcji int, rok_zakonczenia_produkcji int",
    )

    expect_df = spark.createDataFrame(
        [
            (1, "1", "1"),
            (2, "2", "3"),
            (3, "3", "3"),
            (4, "4", "4"),
            (5, "5", "7"),
            (6, "6", "6"),
            (7, "7", "8"),
            (8, "8", "9"),
            (9, "9", "10"),
            (10, "10", "10"),
        ],
        "id int, epoka_rok_wydania_produkcji string, epoka_rok_zakonczenia_produkcji string",
    )

    result = add_epoch_column(
        df,
        add_end_year_epoch=True,
        drop_rok_wydania_produkcji=True,
        drop_rok_zakonczenia_produkcji=True,
    )
    assert_pyspark_df_equal(result, expect_df)
