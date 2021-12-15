import numpy as np
from rest_framework import views


class PandasAPIView(views.APIView):

    # Timestamp column should be set as index
    def dataframe_to_response(self, df, series_columns=None):
        response = {"timestamp": [], "series": []}

        if df.empty and series_columns:
            return response

        df = df.sort_index()

        response["timestamp"] = self.timestamps_to_response(df)

        if series_columns:
            df = df[series_columns]

        for col in df:
            response["series"].append(self._series_to_response(df[col]))

        return response

    def _series_to_response(self, series):
        if series.empty:
            return {"key": None, "values": []}
        values = series.values.tolist()
        return {"key": "%s" % series.name, "values": values}

    def timestamps_to_response(self, df):
        return (df.index.astype(np.int64) // 10 ** 6).values.tolist()

    def empty(self, series_columns=None):
        response = {"timestamp": [], "series": []}

        for col in series_columns:
            response["series"].append({"key": col, "values": []})
        return response
