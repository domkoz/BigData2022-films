from pyspark.sql.functions import col, when

def add_epoch_column(df: DataFrame, periods = [1901,1918,1926,1939,1954,1970,1985,1994,2009]) -> DataFrame:

  assert df.filter(df.rok_wydania_produkcji == "\\N").count() == 0
  assert dict(df.dtypes)["rok_wydania_produkcji"] == "int"

  df_periods = df.withColumn('period',
                             when(col('rok_wydania_produkcji') <= periods[0], "1")
                             .when(col('rok_wydania_produkcji') <= periods[1], "2")
                             .when(col('rok_wydania_produkcji') <= periods[2], "3")
                             .when(col('rok_wydania_produkcji') <= periods[3], "4")
                             .when(col('rok_wydania_produkcji') <= periods[4], "5")
                             .when(col('rok_wydania_produkcji') <= periods[5], "6")
                             .when(col('rok_wydania_produkcji') <= periods[6], "7")
                             .when(col('rok_wydania_produkcji') <= periods[7], "8")
                             .when(col('rok_wydania_produkcji') <= periods[8], "9")
                             .otherwise("10"))
   
  return df_periods
