import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import io, base64

class VisualizationExpert:
    def line_chart(self, df, x, y, title="Line Chart"):
        fig = px.line(df, x=x, y=y, title=title, markers=True)
        return fig.to_json()   # JSON output

    def bar_chart(self, df, x, y, title="Bar Chart"):
        fig = px.bar(df, x=x, y=y, title=title)
        return fig.to_json()

    def world_map(self, df, lat_col, lon_col, color_col=None, title="World Map"):
        fig = px.scatter_geo(
            df,
            lat=lat_col,
            lon=lon_col,
            color=color_col,
            projection="natural earth",
            title=title
        )
        return fig.to_json()

    def static_plot(self, df, x, y, title="Static Plot"):
        plt.figure(figsize=(6,4))
        sns.lineplot(data=df, x=x, y=y, marker="o")
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close()

        return img_b64


# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    # Example ARGO-like dataset
    data = {
        "time": ["2025-01", "2025-02", "2025-03"],
        "temperature": [20.5, 21.0, 19.8],
        "salinity": [35.1, 35.4, 34.9],
        "latitude": [12.3, -8.5, 45.2],
        "longitude": [77.5, 150.2, -30.1]
    }

    df = pd.DataFrame(data)
    viz = VisualizationExpert()

    line_chart_json = viz.line_chart(df, "time", "temperature", "Sea Temperature Over Time")
    bar_chart_json = viz.bar_chart(df, "time", "salinity", "Salinity Levels")
    map_json = viz.world_map(df, "latitude", "longitude", color_col="temperature", title="ARGO Buoy Temperature Map")
    img_b64 = viz.static_plot(df, "time", "temperature", "Static Temperature Plot")

    print("✅ Line Chart JSON Length:", len(line_chart_json))
    print("✅ Bar Chart JSON Length:", len(bar_chart_json))
    print("✅ Map JSON Length:", len(map_json))
    print("✅ Static Plot Base64 (first 50 chars):", img_b64[:50])
