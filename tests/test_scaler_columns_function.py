import findspark

findspark.init()


from pyspark.ml.linalg import Vectors
from lib.scaler_columns_function import scaler_columns
from pyspark_test import assert_pyspark_df_equal
from lib.pyspark_startup import init


def test_scaler_columns():
    spark = init()
    test_dataset = spark.createDataFrame(
        [(0.0, 2435, 4, 55), (1.0, 34, 10, 1974), (2.0, 4, 0, 345)],
        ["inp1", "inp2", "inp3", "inp4"],
    )

    result = scaler_columns(test_dataset, ["inp1", "inp3"], drop_cols=True)
    exp_result = spark.createDataFrame(
        [
            (2435, 55, Vectors.dense([0.0]), Vectors.dense([0.4])),
            (34, 1974, Vectors.dense([0.5]), Vectors.dense([1.0])),
            (4, 345, Vectors.dense([1.0]), Vectors.dense([0.0])),
        ],
        ["inp2", "inp4", "inp1_scaled", "inp3_scaled"],
    )

    assert_pyspark_df_equal(result, exp_result)
